import psychtoolbox as ptb
from time import time

print(ptb.GetSecs())

if __name__ == '__main__':
    from toon.input import MpDevice
    from rawkeyboard import RawKeyboard
    from rawmouse import RawMouse
    mydev = MpDevice(RawKeyboard(clock=ptb.GetSecs))
    hid = ptb.PsychHID
    devs = hid('Devices')

    ms = next(d for d in devs if d['usageValue'] == 2)
    print(ms)
    #idx = ms['index'] - 1
    idx = 0
    hid('KbQueueCreate', idx)


    hid('KbQueueStart', idx)
    hid('KbQueueFlush', idx)

    ptbtimes = []
    mytimes = []
    with mydev:
        t0 = time()

        while time() - t0 < 30:
            [evt, navail] = hid('KbQueueGetEvent', idx)
            res = mydev.read()
            if res:
                print('mine: %s' % res.time)
                mytimes.append(res.time[0])
            if evt:
                print('ptb: %s' % evt)
                ptbtimes.append(evt['Time'])

    hid('KbQueueStop', idx)
    hid('KbQueueRelease', idx)

    dff = [x - y for x, y in zip(mytimes, ptbtimes)]
    import matplotlib.pyplot as plt
    import numpy as np

    plt.plot(np.diff(mytimes))
    plt.plot(np.diff(ptbtimes))
    plt.show()
    plt.hist(dff, bins=25)
    plt.show()
