import psychtoolbox as ptb
from time import time, sleep

print(ptb.GetSecs())

if __name__ == '__main__':
    
    print('sleeping-- plug in test device.')
    sleep(5)
    print('done sleeping-- good luck')

    hid = ptb.PsychHID
    devs = hid('Devices')

    ms = next(d for d in devs if d['usageValue'] == 2)
    print(ms)
    #idx = ms['index'] - 1
    idx = 0
    hid('KbQueueCreate', idx)

    hid('KbQueueStart', idx)

    ptbtimes = []

    t0 = time()
    total_time = 60 * 2
    hid('KbQueueFlush', idx)
    while time() - t0 < total_time:
        [evt, navail] = hid('KbQueueGetEvent', idx)
        if evt:
            #print('ptb: %s' % evt)
            ptbtimes.append(evt['Time'])
        sleep(0.02)

    hid('KbQueueStop', idx)
    hid('KbQueueRelease', idx)
    import matplotlib.pyplot as plt
    import numpy as np
    ptbtimes = np.array(ptbtimes)
    if len(ptbtimes) % 2 != 0:
        ptbtimes = ptbtimes[1:]

    ptbdff = np.diff(ptbtimes[::2])

    plt.plot(ptbdff)
    plt.show()
    print('Press period consistency:')
    print('ptbmean: %f, ptbsd: %f' % (np.mean(ptbdff), np.std(ptbdff)))
    plt.hist(ptbdff, bins=25, alpha=0.5, color='r')
    plt.show()


    ptbtmp = ptbtimes[1::2] - ptbtimes[::2]

    #
    print('Press/release consistency:')
    print('ptbmean: %f, ptbsd: %f' % (np.mean(ptbtmp), np.std(ptbtmp)))
    plt.hist(ptbtmp, bins=30, alpha=0.5, color='r')

    plt.show()
