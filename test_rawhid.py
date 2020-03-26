import struct
import hid

devs = hid.enumerate()

dev_info = next(d for d in devs if d['product_id'] == 0x486 and d['vendor_id'] == 0x16c0)

pth = dev_info['path']

dev = hid.device()
dev.open_path(pth)
dev.set_nonblocking(False)

data = dev.read(64)
try:
    while True:
        data = dev.read(64)
        if data:
            newdat = struct.unpack('B'*64, bytearray(data))
            print(newdat)
except KeyboardInterrupt:
    dev.close()
