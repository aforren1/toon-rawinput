from .rawinput import RawInput, list_devices
import ctypes
import struct

# another abstract class-- the HID is the one
# who knows the usage_page, usage, and how to unpack the
# packet
# we should try to tell ahead of time how big the packet will be
# 65451/512 (which is raw HID) or 65481/4 (which is serial?)
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
        print(hd.dwSizeHid, hd.dwCount)
        if hd.dwCount > 0:
            data = hd.bRawData[0]
            print(hd.dwCount, data)

if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    dev = MpDevice(HID())
    with dev:
        start = time.time()
        while time.time() - start < 20:
            time.sleep(1)
            #dat = dev.read()
            #if dat:
            #    print(dat.time, dat.data)  # access joints via dat[-1]['thumb']['mcp']
            time.sleep(1)  # pretend to have a screen
