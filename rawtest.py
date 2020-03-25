if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    from rawkeyboard import RawKeyboard
    from rawmouse import RawMouse

    dev1 = MpDevice(RawKeyboard())
    dev2 = MpDevice(RawMouse())
    with dev1, dev2:
        start = time.time()
        while time.time() - start < 20:
            res1 = dev1.read()
            res2 = dev2.read()
            if res1:
                print(res1.time, res1.data)
            if res2:
                print(res2.time, res2.data)        
            time.sleep(0.016)  # pretend to have a screen
