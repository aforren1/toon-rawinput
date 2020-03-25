# reduced wintypes, original copyright below:
# ----------------------------------------------------------------------------
# pyglet
# Copyright (c) 2006-2008 Alex Holkner
# Copyright (c) 2008-2020 pyglet contributors
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions
# are met:
#
#  * Redistributions of source code must retain the above copyright
#    notice, this list of conditions and the following disclaimer.
#  * Redistributions in binary form must reproduce the above copyright
#    notice, this list of conditions and the following disclaimer in
#    the documentation and/or other materials provided with the
#    distribution.
#  * Neither the name of pyglet nor the names of its
#    contributors may be used to endorse or promote products
#    derived from this software without specific prior written
#    permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS
# FOR A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE
# COPYRIGHT OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT,
# INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING,
# BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES;
# LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT
# LIABILITY, OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN
# ANY WAY OUT OF THE USE OF THIS SOFTWARE, EVEN IF ADVISED OF THE
# POSSIBILITY OF SUCH DAMAGE.
# ----------------------------------------------------------------------------

import sys
import ctypes
from ctypes import *
from ctypes.wintypes import *


_int_types = (c_int16, c_int32)
if hasattr(ctypes, 'c_int64'):
    # Some builds of ctypes apparently do not have c_int64
    # defined; it's a pretty good bet that these builds do not
    # have 64-bit pointers.
    _int_types += (c_int64,)
for t in _int_types:
    if sizeof(t) == sizeof(c_size_t):
        c_ptrdiff_t = t
del t
del _int_types


# PUINT is defined only from >= python 3.2
if sys.version_info < (3, 2)[:2]:
    PUINT = POINTER(UINT)


class c_void(Structure):
    # c_void_p is a buggy return type, converting to int, so
    # POINTER(None) == c_void_p is actually written as
    # POINTER(c_void), so it can be treated as a real pointer.
    _fields_ = [('dummy', c_int)]


def POINTER_(obj):
    p = ctypes.POINTER(obj)

    # Convert None to a real NULL pointer to work around bugs
    # in how ctypes handles None on 64-bit platforms
    if not isinstance(p.from_param, classmethod):
        def from_param(cls, x):
            if x is None:
                return cls()
            else:
                return x
        p.from_param = classmethod(from_param)

    return p


c_void_p = POINTER_(c_void)
INT = c_int
LPVOID = c_void_p
HCURSOR = HANDLE
LRESULT = LPARAM
COLORREF = DWORD
PVOID = c_void_p
WCHAR = c_wchar
BCHAR = c_wchar
LPRECT = POINTER(RECT)
LPPOINT = POINTER(POINT)
LPMSG = POINTER(MSG)
UINT_PTR = HANDLE
LONG_PTR = HANDLE
HDROP = HANDLE
LPTSTR = LPWSTR
LPSTREAM = c_void_p

LF_FACESIZE = 32
CCHDEVICENAME = 32
CCHFORMNAME = 32

WNDPROC = WINFUNCTYPE(LRESULT, HWND, UINT, WPARAM, LPARAM)
TIMERPROC = WINFUNCTYPE(None, HWND, UINT, POINTER(UINT), DWORD)
TIMERAPCPROC = WINFUNCTYPE(None, PVOID, DWORD, DWORD)
MONITORENUMPROC = WINFUNCTYPE(BOOL, HMONITOR, HDC, LPRECT, LPARAM)

class WNDCLASS(Structure):
    _fields_ = [
        ('style', UINT),
        ('lpfnWndProc', WNDPROC),
        ('cbClsExtra', c_int),
        ('cbWndExtra', c_int),
        ('hInstance', HINSTANCE),
        ('hIcon', HICON),
        ('hCursor', HCURSOR),
        ('hbrBackground', HBRUSH),
        ('lpszMenuName', c_char_p),
        ('lpszClassName', c_wchar_p)
    ]

class RAWINPUTDEVICE(Structure):
    _fields_ = [
        ('usUsagePage', USHORT),
        ('usUsage', USHORT),
        ('dwFlags', DWORD),
        ('hwndTarget', HWND)
    ]


PCRAWINPUTDEVICE = POINTER(RAWINPUTDEVICE)
HRAWINPUT = HANDLE


class RAWINPUTHEADER(Structure):
    _fields_ = [
        ('dwType', DWORD),
        ('dwSize', DWORD),
        ('hDevice', HANDLE),
        ('wParam', WPARAM),
    ]


class _Buttons(Structure):
    _fields_ = [
        ('usButtonFlags', USHORT),
        ('usButtonData', USHORT),
    ]


class _U(Union):
    _anonymous_ = ('_buttons',)
    _fields_ = [
        ('ulButtons', ULONG),
        ('_buttons', _Buttons),
    ]


class RAWMOUSE(Structure):
    _anonymous_ = ('u',)
    _fields_ = [
        ('usFlags', USHORT),
        ('u', _U),
        ('ulRawButtons', ULONG),
        ('lLastX', LONG),
        ('lLastY', LONG),
        ('ulExtraInformation', ULONG),
    ]


class RAWKEYBOARD(Structure):
    _fields_ = [
        ('MakeCode', USHORT),
        ('Flags', USHORT),
        ('Reserved', USHORT),
        ('VKey', USHORT),
        ('Message', UINT),
        ('ExtraInformation', ULONG),
    ]


class RAWHID(Structure):
    _fields_ = [
        ('dwSizeHid', DWORD),
        ('dwCount', DWORD),
        ('bRawData', POINTER(BYTE)),
    ]


class _RAWINPUTDEVICEUNION(Union):
    _fields_ = [
        ('mouse', RAWMOUSE),
        ('keyboard', RAWKEYBOARD),
        ('hid', RAWHID),
    ]


class RAWINPUT(Structure):
    _fields_ = [
        ('header', RAWINPUTHEADER),
        ('data', _RAWINPUTDEVICEUNION),
    ]

class RAWINPUTDEVICELIST(Structure):
    _fields_ = [
        ('hDevice', HANDLE),
        ('dwType', DWORD)
    ]

PRAWINPUTDEVICELIST = POINTER(RAWINPUTDEVICELIST)

class RID_DEVICE_INFO_MOUSE(Structure):
    _fields_ = [
        ('dwId', DWORD),
        ('dwNumberOfButtons', DWORD),
        ('fHasHorizontalWheel', BOOL)
    ]

class RID_DEVICE_INFO_KEYBOARD(Structure):
    _fields_ = [
        ('dwType', DWORD),
        ('dwSubType', DWORD),
        ('dwKeyboardMode', DWORD),
        ('dwNumberOfFunctionKeys', DWORD),
        ('dwNumberOfIndicators', DWORD),
        ('dwNumberOfKeysTotal', DWORD)
    ]

class RID_DEVICE_INFO_HID(Structure):
    _fields_ = [
        ('dwVendorId', DWORD),
        ('dwProductId', DWORD),
        ('dwVersionNumber', DWORD),
        ('usUsagePage', USHORT),
        ('usUsage', USHORT)
    ]

class _UINFO(Union):
    _fields_ = [
        ('mouse', RID_DEVICE_INFO_MOUSE),
        ('keyboard', RID_DEVICE_INFO_KEYBOARD),
        ('hid', RID_DEVICE_INFO_HID)
    ]

class RID_DEVICE_INFO(Structure):
    _anonymous_ = ('x',)
    _fields_ = [
        ('cbSize', DWORD),
        ('dwType', DWORD),
        ('x', _UINFO)
    ]
