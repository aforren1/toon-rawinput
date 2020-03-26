if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    from rawkeyboard import RawKeyboard
    from rawmouse import RawMouse

    dev1 = MpDevice(RawMouse())
    dev2 = MpDevice(RawKeyboard())
    t1 = []
    t2 = []
    with dev1, dev2:
        start = time.time()
        while time.time() - start < 20:
            res1 = dev1.read()
            res2 = dev2.read()
            if res1:
                print(res1.time, res1.data)
                t1.append(res1.time)
            if res2:
                print(res2.time, res2.data)
                t2.append(res2.time)
            time.sleep(0.016)  # pretend to have a screen
    
    # comparing two mice, e.g.
    # import numpy as np
    # import matplotlib.pyplot as plt

    # xx = np.hstack(t1) - np.hstack(t2)
    # plt.hist(xx, bins=50)
    # plt.show()
