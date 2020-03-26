from toon.input import BaseDevice
from ctypes import windll
from wintypes import *

from winconstants import (HWND_MESSAGE, RIDEV_NOLEGACY,
                          RIDEV_INPUTSINK, RID_INPUT,
                          RIDI_DEVICENAME, RIDI_DEVICEINFO,
                          RIDI_PREPARSEDDATA, RIM_TYPEHID,
                          RIM_TYPEKEYBOARD, RIM_TYPEMOUSE,
                          PM_REMOVE)
import ctypes.wintypes as cwt

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
u32 = windll.user32
k32 = windll.kernel32

# https://github.com/pyglet/pyglet/blob/b49b6a7052fe21ad64e53456bc23c289a9ccb757/pyglet/libs/win32/__init__.py#L268
u32.RegisterRawInputDevices.restype = BOOL
u32.RegisterRawInputDevices.argtypes = [PCRAWINPUTDEVICE, UINT, UINT]
u32.GetRawInputData.restype = UINT
u32.GetRawInputData.argtypes = [HRAWINPUT, UINT, LPVOID, PUINT, UINT]
u32.ChangeWindowMessageFilterEx.restype = BOOL
u32.ChangeWindowMessageFilterEx.argtypes = [HWND, UINT, DWORD, c_void_p]

# https://github.com/pyglet/pyglet/blob/b49b6a7052fe21ad64e53456bc23c289a9ccb757/pyglet/libs/win32/__init__.py#L220
u32.RegisterClassW.restype = ATOM
u32.RegisterClassW.argtypes = [POINTER(WNDCLASS)]
u32.CreateWindowExW.restype = HWND
u32.CreateWindowExW.argtypes = [DWORD, c_wchar_p, c_wchar_p, DWORD, c_int, c_int, c_int, c_int, HWND, HMENU, HINSTANCE, LPVOID]
u32.DefWindowProcW.restype = LRESULT
u32.DefWindowProcW.argtypes = [HWND, UINT, WPARAM, LPARAM]
u32.DestroyWindow.restype = BOOL
u32.DestroyWindow.argtypes = [HWND]
u32.UnregisterClassW.restype = BOOL
u32.UnregisterClassW.argtypes = [c_wchar_p, HINSTANCE]
u32.PeekMessageW.restype = BOOL
u32.PeekMessageW.argtypes = [LPMSG, HWND, UINT, UINT, UINT]
u32.GetMessageW.restype = BOOL
u32.GetMessageW.argtypes = [LPMSG, HWND, UINT, UINT]
u32.TranslateMessage.restype = BOOL
u32.TranslateMessage.argtypes = [LPMSG]
u32.DispatchMessageW.restype = LRESULT
u32.DispatchMessageW.argtypes = [LPMSG]

u32.GetRawInputDeviceList.restype = UINT
u32.GetRawInputDeviceList.argtypes = [PRAWINPUTDEVICELIST, PUINT, UINT]
u32.GetRawInputDeviceInfoW.restype = UINT
u32.GetRawInputDeviceInfoW.argtypes = [HANDLE, UINT, LPVOID, PUINT]

def list_devices(dev_type='all'):
    nDevices = UINT()
    sz = sizeof(RAWINPUTDEVICELIST)
    res = u32.GetRawInputDeviceList(None, byref(nDevices), sz)
    if res != 0:
        raise ValueError('Something went wrong, error code: %i' % k32.GetLastError())
    devs = (RAWINPUTDEVICELIST*nDevices.value)()
    res = u32.GetRawInputDeviceList(ctypes.cast(devs, PRAWINPUTDEVICELIST), 
                                    byref(nDevices), sz)
    hids = []
    keyboards = []
    mice = []
    for i in range(res):
        devinfo = RID_DEVICE_INFO()
        devinfo.cbSize = sizeof(RID_DEVICE_INFO)
        sz = UINT(sizeof(devinfo))
        
        tmpstr = ctypes.create_unicode_buffer(100)
        sz2 = UINT(sizeof(tmpstr))
        
        res2 = u32.GetRawInputDeviceInfoW(devs[i].hDevice, RIDI_DEVICENAME,
                                        byref(tmpstr), sz2)
        
        res2 = u32.GetRawInputDeviceInfoW(devs[i].hDevice, RIDI_DEVICEINFO, 
                                        byref(devinfo), byref(sz))
        # num of bytes should be > 0
        if res2 > 0:
            packet = {'name': tmpstr.value, 'handle': devs[i].hDevice}
            if devinfo.dwType == RIM_TYPEHID:
                packet['info'] = devinfo.hid
                hids.append(packet)
            elif devinfo.dwType == RIM_TYPEKEYBOARD:
                packet['info'] = devinfo.keyboard
                keyboards.append(packet)
            else:
                packet['info'] = devinfo.mouse
                mice.append(packet)
            
    if dev_type == 'hid':
        return hids
    if dev_type == 'keyboard':
        return keyboards
    if dev_type == 'mouse':
        return mice
    return mice, keyboards, hids


class RawWinDevice(BaseDevice):
    sampling_frequency = 100
    ctype = int # dummy (fill in later)
    usage_page = 0x01
    usage = -1 # usage ID; so far, just 0x02 (mouse) or 0x06 (keyboard)

    # do nothing in init

    def enter(self):
        # make classname unique
        current_counter = cwt.LARGE_INTEGER()
        kernel32.QueryPerformanceCounter(ctypes.byref(current_counter))
        classname = 'RawWindow%s' % current_counter.value

        wndclass = WNDCLASS()
        wndclass.lpszClassName = classname
        wndclass.cbSize = sizeof(wndclass)
        wndclass.lpfnWndProc = WNDPROC(u32.DefWindowProcW)
        wndclass.hInstance = 0

        if u32.RegisterClassW(wndclass):
            hwnd = u32.CreateWindowExW(0, wndclass.lpszClassName, '', 
                                       0, 0, 0, 0, 0, HWND_MESSAGE, 
                                       None, wndclass.hInstance, None)
        else:
            raise ValueError('Window creation failed.')

        raw_dev = RAWINPUTDEVICE(self.usage_page, self.usage, RIDEV_NOLEGACY|RIDEV_INPUTSINK, hwnd)
        if not u32.RegisterRawInputDevices(byref(raw_dev), 1, sizeof(RAWINPUTDEVICE)):
            self.exit()
            raise ValueError('Could not register raw device.')

        self._hwnd = hwnd
        self._wndclass = wndclass
        self._msgs = (MSG*10)()
        self._rinput = RAWINPUT()
        self._rsize = UINT(sizeof(self._rinput))
    
    def read(self):
        if u32.GetMessageW(byref(self._msgs[0]), 0, 0, 0):
            time = self.clock()
            counter = 1
            while u32.PeekMessageW(byref(self._msgs[counter]), 0, 0, 0, PM_REMOVE):
                counter += 1
            res = []
            for i in range(counter):
                _msg = self._msgs[i]
                hRawInput = cast(_msg.lParam, HRAWINPUT)
                u32.GetRawInputData(hRawInput, RID_INPUT, byref(self._rinput), 
                                    byref(self._rsize), sizeof(RAWINPUTHEADER))
                data = self._device_specific() # can get data from self._rinput
                if data is not None:
                    res.append([time, data])
            if res:
                return res
        return None
    
    def _device_specific(self):
        return 0
    
    def exit(self):
        u32.DestroyWindow(self._hwnd)
        u32.UnregisterClassW(self._wndclass.lpszClassName, 0)
