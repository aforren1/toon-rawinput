from toon.input import BaseDevice
from ctypes import windll
from wintypes import *

from winconstants import (HWND_MESSAGE, RIDEV_NOLEGACY,
                          RIDEV_INPUTSINK, RID_INPUT)
import ctypes.wintypes as cwt

kernel32 = ctypes.WinDLL('kernel32', use_last_error=True)
u32 = windll.user32

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

class RawWinDevice(BaseDevice):
    sampling_frequency = 100
    ctype = int # dummy (fill in later)
    devtype = -1 # usage ID; so far, just 0x02 (mouse) or 0x06 (keyboard)

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

        raw_dev = RAWINPUTDEVICE(0x01, self.devtype, RIDEV_NOLEGACY|RIDEV_INPUTSINK, hwnd)
        if not u32.RegisterRawInputDevices(byref(raw_dev), 1, sizeof(RAWINPUTDEVICE)):
            self.exit()
            raise ValueError('Could not register raw device.')

        self._hwnd = hwnd
        self._wndclass = wndclass
        self._msg = MSG()
        self._rinput = RAWINPUT()
        self._rsize = UINT(sizeof(self._rinput))
    
    def read(self):
        # TODO: could do a better job with multiple simultaneous messages
        # by switching to PeekMessage and spinning until all consumed
        if u32.GetMessageW(byref(self._msg), 0, 0, 0):
            time = self.clock()
            u32.TranslateMessage(byref(self._msg))
            hRawInput = cast(self._msg.lParam, HRAWINPUT)
            u32.GetRawInputData(hRawInput, RID_INPUT, byref(self._rinput), 
                                byref(self._rsize), sizeof(RAWINPUTHEADER))
            
            data = self._device_specific() # can get data from self._rinput
            if data is None:
                return None
            return time, data
        return None
    
    def _device_specific(self):
        return 0
    
    def exit(self):
        u32.DestroyWindow(self._hwnd)
        u32.UnregisterClassW(self._wndclass.lpszClassName, 0)
