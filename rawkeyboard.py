import ctypes
from rawdevice import RawWinDevice, list_devices
from wintypes import SHORT

class Data(ctypes.Structure):
    _fields_ = [('index', ctypes.c_uint16), ('press', ctypes.c_bool), ('id', SHORT)]

class RawKeyboard(RawWinDevice):
    ctype = Data
    usage = 0x06

    def __init__(self, keys=['a', 's', 'd', 'f'], **kwargs):
        self.keys = keys
        self._vals = []
        # reverse lookup
        for refk in keys:
            for k, v in win_keys.items():
                if v == refk:
                    self._vals.append(k)
        kbs = list_devices('keyboard')
        self._handles = [x['handle'] for x in kbs]
        super().__init__(**kwargs)
    
    def _device_specific(self):
        kb = self._rinput.data.keyboard
        hDev = self._rinput.header.hDevice
        # (potentially) handle hot plugging
        try:
            _hidx = self._handles.index(hDev)
        except ValueError:
            _hidx = len(self._handles)
            self._handles.append(hDev)
        try:
            idx = self._vals.index(kb.VKey)
        # key not in valid set
        except ValueError:
            return None
        return self.ctype(index=idx, press=not kb.Flags, id=_hidx)

#https://github.com/Psychtoolbox-3/Psychtoolbox-3/blob/fab0b49fd38ec477e3b4573f23dbd7766b0a89aa/Psychtoolbox/PsychBasic/KbName.m       
#https://github.com/psychopy/psychopy/blob/76b07c9aa1e14726f9edf631739ac3682a51d9da/psychopy/hardware/keyboard.py#L437
# shift keys seem funny
win_keys = {
    49: '1', 50: '2', 51: '3', 52: '4', 53: '5',
    54: '6', 55: '7', 56: '8', 57: '9', 48: '0',
    65: 'a', 66: 'b', 67: 'c', 68: 'd', 69: 'e', 70: 'f',
    71: 'g', 72: 'h', 73: 'i', 74: 'j', 75: 'k', 76: 'l',
    77: 'm', 78: 'n', 79: 'o', 80: 'p', 81: 'q', 82: 'r',
    83: 's', 84: 't', 85: 'u', 86: 'v', 87: 'w', 88: 'x',
    89: 'y', 90: 'z',
    97: 'num_1', 98: 'num_2', 99: 'num_3',
    100: 'num_4', 101: 'num_5', 102: 'num_6', 103: 'num_7',
    104: 'num_8', 105: 'num_9', 96: 'num_0',
    112: 'f1', 113: 'f2', 114: 'f3', 115: 'f4', 116: 'f5',
    117: 'f6', 118: 'f7', 119: 'f8', 120: 'f9', 121: 'f10',
    122: 'f11', 123: 'f12',
    145: 'scrollock', 19: 'pause', 36: 'home', 35: 'end',
    45: 'insert', 33: 'pageup', 46: 'delete', 34: 'pagedown',
    37: 'left', 40: 'down', 38: 'up', 39: 'right', 27: 'escape',
    144: 'numlock', 111: 'num_divide', 106: 'num_multiply',
    8: 'backspace', 109: 'num_subtract', 107: 'num_add',
    13: 'return', 222: 'pound', 161: 'lshift', 163: 'rctrl',
    92: 'rwindows', 32: 'space', 164: 'lalt', 165: 'ralt',
    91: 'lwindows', 93: 'menu', 162: 'lctrl', 160: 'lshift',
    20: 'capslock', 9: 'tab', 223: 'quoteleft', 220: 'backslash',
    188: 'comma', 190: 'period', 191: 'slash', 186: 'semicolon',
    192: 'apostrophe', 219: 'bracketleft', 221: 'bracketright',
    189: 'minus', 187: 'equal'
}

if __name__ == '__main__':
    import time
    from toon.input.mpdevice import MpDevice
    dev = MpDevice(RawKeyboard())
    with dev:
        start = time.time()
        while time.time() - start < 20:
            dat = dev.read()
            if dat:
                print(dat.time, dat.data)  # access joints via dat[-1]['thumb']['mcp']
            time.sleep(0.016)  # pretend to have a screen
