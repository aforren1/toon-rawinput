import ctypes
from wintypes import LONG, SHORT
from winconstants import (RI_MOUSE_LEFT_BUTTON_DOWN, RI_MOUSE_LEFT_BUTTON_UP,
                          RI_MOUSE_RIGHT_BUTTON_DOWN, RI_MOUSE_RIGHT_BUTTON_UP,
                          RI_MOUSE_MIDDLE_BUTTON_DOWN, RI_MOUSE_MIDDLE_BUTTON_UP,
                          WHEEL_DELTA)
from rawdevice import RawWinDevice, list_devices

class MouseState(ctypes.Structure):
    _fields_ = [('dx', LONG), ('dy', LONG), ('lb', SHORT), 
                ('rb', SHORT), ('mb', SHORT), ('wheel', SHORT),
                ('id', SHORT)]

class RawMouse(RawWinDevice):
    ctype = MouseState
    usage = 0x02

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        mice = list_devices('mouse')
        self._handles = [x['handle'] for x in mice]

    def _device_specific(self):
        d = self.ctype()
        hDev = self._rinput.header.hDevice
        try:
            _hidx = self._handles.index(hDev)
        except ValueError:
            _hidx = len(self._handles)
            self._handles.append(hDev)
        d.id = _hidx
        ms = self._rinput.data.mouse
        d.dx = ms.lLastX
        d.dy = ms.lLastY
        # left button up/down (0 if no state change)
        ld = ms.usButtonFlags & RI_MOUSE_LEFT_BUTTON_DOWN > 0
        lu = ms.usButtonFlags & RI_MOUSE_LEFT_BUTTON_UP > 0
        d.lb = 0
        if ld:
            d.lb = 1
        elif lu:
            d.lb = -1
        # right button up/down
        rd = ms.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_DOWN > 0
        ru = ms.usButtonFlags & RI_MOUSE_RIGHT_BUTTON_UP > 0
        d.rb = 0
        if rd:
            d.rb = 1
        elif ru:
            d.rb = -1
        # middle button
        md = ms.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_DOWN > 0
        mu = ms.usButtonFlags & RI_MOUSE_MIDDLE_BUTTON_UP > 0
        d.mb = 0
        if md:
            d.mb = 1
        elif mu:
            d.mb = -1
        # TODO: no way it has to be like this
        d.wheel = SHORT(int(SHORT(ms.usButtonData).value / float(WHEEL_DELTA)))
        return d

if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    dev = MpDevice(RawMouse())
    times = []
    datae = []
    with dev:
        start = time.time()
        while time.time() - start < 10:
            res = dev.read()
            if res:
                ti, data = res
                times.append(ti)
                datae.append(data)
                print(data)  # access joints via dat[-1]['thumb']['mcp']
            #time.sleep(0.016)  # pretend to have a screen

    import numpy as np
    import matplotlib.pyplot as plt

    x = np.diff(np.hstack(times))
    plt.plot(x)
    plt.show()