from rawdevice import RawWinDevice
import ctypes

# another abstract class-- the HID is the one
# who knows the usage_page, usage, and how to unpack the
# packet
# we should try to tell ahead of time how big the packet will be
class RawHID(RawWinDevice):
    ctype = ctypes.c_ubyte
    shape = (64,)

    def _device_specific(self):
        hd = self._rinput.data.hid
        data = hd.bRawData.contents

# future note: Teensy usage page is 0xffab, usage is 0x0200
