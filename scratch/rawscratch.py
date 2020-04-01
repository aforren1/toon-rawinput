#https://docs.microsoft.com/en-us/windows/win32/inputdev/using-raw-input
from ctypes import windll
from toon_rawinput.wintypes import *
from toon_rawinput.winconstants import *
import sys
from timeit import default_timer
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

wndclass = WNDCLASS()
classname = 'MouseWindow'
wndclass.lpszClassName = classname
wndclass.cbSize = sizeof(wndclass)
wndclass.lpfnWndProc = WNDPROC(u32.DefWindowProcW)
wndclass.hInstance = 0

if u32.RegisterClassW(wndclass):
    hwnd = u32.CreateWindowExW(0, wndclass.lpszClassName, '', 
                               0, 0, 0, 0, 0, HWND_MESSAGE, 
                               None, wndclass.hInstance, None)
    print(hwnd)
else:
    sys.exit(1)

raw_mouse = RAWINPUTDEVICE(0x01, 0x06, RIDEV_NOLEGACY|RIDEV_INPUTSINK, hwnd)
res = u32.RegisterRawInputDevices(byref(raw_mouse), 1, sizeof(RAWINPUTDEVICE))

if not res:
    print('eurgh')
    u32.DestroyWindow(hwnd)
    u32.UnregisterClassW(wndclass.lpszClassName, 0)
    sys.exit(1)

t0 = default_timer()

class MouseState(ctypes.Structure):
    _fields_ = [('dx', LONG), ('dy', LONG), ('lb', SHORT), 
                ('rb', SHORT), ('mb', SHORT), ('wheel', SHORT)]

win_keys = {
    49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
    54: '6', 55: '7', 56: '8', 57: '9', 48: '0',
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f',
    71: 'g', 72: 'h', 73: 'i', 74: 'j', 75: 'k', 76: 'l',
    77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r',
    83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x',
    89: 'y', 90: 'z',
    97: 'num_1', 98: 'num_2', 99: 'num_3',
    100: 'num_4', 101: 'num_5', 102: 'num_6', 103: 'num_7',
    104: 'num_8', 105: 'num_9', 96: 'num_0',
    112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4', 116: 'f5',
    117: 'f6', 118: 'f7', 119: 'f8', 120: 'f9', 121: 'f10',
    122: 'f11', 123: 'f12',
    145: 'scrollock', 19: 'pause', 36: 'home', 35: 'end',
    45: 'insert', 33: 'pageup', 46: 'delete', 34: 'pagedown',
    37: 'left', 40: 'down', 38: 'up', 39: 'right', 27: 'escape',
    144: 'numlock', 111: 'num_divide', 106: 'num_multiply',
    8: 'backspace', 109: 'num_subtract', 107: 'num_add',
    13: 'return', 222: 'pound', 161: 'lshift', 163: 'rctrl',
    92: 'rwindows', 32: 'space', 164: 'lalt', 165: 'ralt',
    91: 'lwindows', 93: 'menu', 162: 'lctrl', 160: 'lshift',
    20: 'capslock', 9: 'tab', 223: 'quoteleft', 220: 'backslash',
    188: 'comma', 190: 'period', 191: 'slash', 186: 'semicolon',
    192: 'apostrophe', 219: 'bracketleft', 221: 'bracketright',
    189: 'minus', 187: 'equal'
}

try:
    while True:
        msg = MSG()
        inp = RAWINPUT()
        size = UINT(sizeof(inp))
        msdat = inp.data.mouse
        kbdat = inp.data.keyboard
        #while u32.PeekMessageW(byref(msg), 0, 0, 0, PM_REMOVE):
        while u32.GetMessageW(byref(msg), 0, 0, 0):
            t1 = default_timer()
            #print(t1 - t0)
            t0 = t1
            u32.TranslateMessage(byref(msg))
            hRawInput = cast(msg.lParam, HRAWINPUT)
            u32.GetRawInputData(hRawInput, RID_INPUT, byref(inp), byref(size), sizeof(RAWINPUTHEADER))
            # shouldn't be any crosstalk...
            #if inp.header.dwType == RIM_TYPEMOUSE:
            try:
                print(win_keys[kbdat.VKey], not kbdat.Flags, kbdat.MakeCode)
            except KeyError:
                print('problem: %s' % kbdat.VKey)
            # mst = MouseState()
            # mst.dx = msdat.lLastX
            # mst.dy = msdat.lLastY
            # lb_down = msdat.usButtonFlags & RI_MOUSE_LEFT_BUTTON_DOWN > 0
            # lb_up = msdat.usButtonFlags & RI_MOUSE_LEFT_BUTTON_UP > 0
            # mst.lb = 0
            # if lb_down:
            #     mst.lb = 1
            # elif lb_up:
            #     mst.lb = -1
            # rb_down = msdat.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_DOWN > 0
            # rb_up = msdat.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_UP > 0
            # mst.rb = 0
            # if rb_down:
            #     mst.rb = 1
            # elif rb_up:
            #     mst.rb = -1            
            # mb_down = msdat.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_DOWN > 0
            # mb_up = msdat.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_UP > 0
            # mst.mb = 0
            # if mb_down:
            #     mst.mb = 1
            # elif mb_up:
            #     mst.mb = -1  
            # mst.wheel = SHORT(int(SHORT(msdat.usButtonData).value / float(WHEEL_DELTA)))
            # print(mst.dx, mst.dy, mst.lb, mst.rb, mst.mb, mst.wheel)
            # u32.DispatchMessageW(byref(msg))
except KeyboardInterrupt:
    u32.DestroyWindow(hwnd)
    u32.UnregisterClassW(wndclass.lpszClassName, 0)

