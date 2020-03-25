from mglg.graphics.shape2d import Circle

from mglg.graphics.win import Win

from rawmouse import RawMouse
from toon.input import MpDevice
from timeit import default_timer

if __name__ == '__main__':

    win = Win(vsync=1, screen=0)
    height = win.height
    cir = Circle(win, scale=0.1, fill_color = (0.2, 0.9, 0.7, 1))

    dev = MpDevice(RawMouse())

    with dev:
        t0 = default_timer()
        t1 = t0 + 30
        while t1 > default_timer():
            res = dev.read()
            if res:
                time, data = res
                left = data[data['id']==0]
                right = data[data['id']==1]
                if left.shape[0] > 0:
                    cir.position.x += float(left[-1]['dy']) / win.height
                if right.shape[0] > 0:
                    cir.position.y += float(right[-1]['dx'] / win.height)

            cir.draw()
            win.flip()