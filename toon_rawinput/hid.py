from .rawinput import RawInput, list_devices
import ctypes
import struct

# another abstract class-- the HID is the one
# who knows the usage_page, usage, and how to unpack the
# packet
# we should try to tell ahead of time how big the packet will be
# 65451/512 or 65481/4
class HID(RawInput):
    ctype = ctypes.c_ubyte
    shape = (64,)
    usage_page = 65451
    usage = 512

    def __init__(self, **kwargs):
        dvs = list_devices('hid')
        dvs = [d for d in dvs if d['info'].dwVendorId == 0x16c0 and d['info'].dwProductId == 0x486]
        self._handles = [x['handle'] for x in dvs]
        super().__init__(**kwargs)


    def _device_specific(self):
        hd = self._rinput.data.hid
        print(hd.dwSizeHid)
        if hd.dwSizeHid > 0:
            data = hd.bRawData.contents
            print(data)

if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    dev = MpDevice(HID())
    with dev:
        start = time.time()
        while time.time() - start < 20:
            dat = dev.read()
            if dat:
                print(dat.time, dat.data)  # access joints via dat[-1]['thumb']['mcp']
            time.sleep(0.016)  # pretend to have a screen
