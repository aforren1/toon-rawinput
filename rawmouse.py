import ctypes
from wintypes import LONG, SHORT
from winconstants import (RI_MOUSE_LEFT_BUTTON_DOWN, RI_MOUSE_LEFT_BUTTON_UP,
                          RI_MOUSE_RIGHT_BUTTON_DOWN, RI_MOUSE_RIGHT_BUTTON_UP,
                          RI_MOUSE_MIDDLE_BUTTON_DOWN, RI_MOUSE_MIDDLE_BUTTON_UP,
                          WHEEL_DELTA)
from rawdevice import RawWinDevice

class MouseState(ctypes.Structure):
    _fields_ = [('dx', LONG), ('dy', LONG), ('lb', SHORT), 
                ('rb', SHORT), ('mb', SHORT), ('wheel', SHORT)]

class RawMouse(RawWinDevice):
    ctype = MouseState
    devtype = 0x02

    def _device_specific(self):
        d = self.ctype()
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
    with dev:
        start = time.time()
        while time.time() - start < 20:
            dat = dev.read()
            if dat:
                times.append(dat.time)
                print(dat.data)  # access joints via dat[-1]['thumb']['mcp']
            #time.sleep(0.016)  # pretend to have a screen
    
    import numpy as np
    import matplotlib.pyplot as plt

    x = np.diff(np.hstack(times))
    plt.plot(x)
    plt.show()