from toon.input import BaseDevice
from ctypes import windll
from .wintypes import *

from .winconstants import (HWND_MESSAGE, RIDEV_NOLEGACY,
                          RIDEV_INPUTSINK, RID_INPUT,
                          RIDI_DEVICENAME, RIDI_DEVICEINFO,
                          RIDI_PREPARSEDDATA, RIM_TYPEHID,
                          RIM_TYPEKEYBOARD, RIM_TYPEMOUSE,
                          PM_REMOVE)
import ctypes.wintypes as cwt

u32 = windll.user32
k32 = windll.kernel32

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


class RawInput(BaseDevice):
    sampling_frequency = 100
    ctype = int # dummy (fill in later)
    usage_page = 0x01
    usage = -1 # usage ID; so far, just 0x02 (mouse) or 0x06 (keyboard)

    # do nothing in init

    def enter(self):
        # make classname unique
        current_counter = cwt.LARGE_INTEGER()
        k32.QueryPerformanceCounter(ctypes.byref(current_counter))
        classname = 'RawWindow%s' % current_counter.value

        wndclass = WNDCLASS()
        wndclass.lpszClassName = classname
        wndclass.lpfnWndProc = WNDPROC(u32.DefWindowProcW)
        wndclass.hInstance = 0

        if u32.RegisterClassW(byref(wndclass)):
            hwnd = u32.CreateWindowExW(0, wndclass.lpszClassName, '', 
                                       0, 0, 0, 0, 0, HWND_MESSAGE, 
                                       None, wndclass.hInstance, None)
        else:
            raise ValueError('Window creation failed.')
        self._hwnd = hwnd
        self._wndclass = wndclass
        flags = RIDEV_INPUTSINK
        # NOLEGACY makes raw HID unhappy
        if self.usage_page == 0x01 and self.usage in [0x02, 0x06]:
            flags = flags | RIDEV_NOLEGACY
        raw_dev = RAWINPUTDEVICE(self.usage_page, self.usage, flags, hwnd)
        if not u32.RegisterRawInputDevices(byref(raw_dev), 1, sizeof(RAWINPUTDEVICE)):
            self.exit()
            raise ValueError('Could not register raw device. Error code: %s' % k32.GetLastError())

        self._msg = MSG() # preallocate small number of MSGs for reuse
        self._rinput = RAWINPUT()
        self._rsize = UINT(sizeof(self._rinput))
    
    def read(self):
        # block until the first message
        val = u32.GetMessageW(byref(self._msg), 0, 0, 0)
        time = self.clock()
        if val > 0:
            time = self.clock() # take time ASAP
            # counter = 1
            # any other messages?
            # while u32.PeekMessageW(byref(self._msgs[counter]), 0, 0, 0, PM_REMOVE):
            #     counter += 1
            # res = []
            # retrieve the data from each message
            # Note that we didn't need [Translate/Dispatch]Message
            #for i in range(counter):
            _msg = self._msg
            hRawInput = cast(_msg.lParam, HRAWINPUT)
            u32.GetRawInputData(hRawInput, RID_INPUT, byref(self._rinput),
                                byref(self._rsize), sizeof(RAWINPUTHEADER))
            data = self._device_specific() # can get data from self._rinput
            if data is not None:
                return time, data
        return None
    
    def _device_specific(self):
        return 0
    
    def exit(self):
        u32.DestroyWindow(self._hwnd)
        u32.UnregisterClassW(self._wndclass.lpszClassName, 0)
