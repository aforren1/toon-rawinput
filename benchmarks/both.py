import psychtoolbox as ptb
from time import time, sleep

print(ptb.GetSecs())

if __name__ == '__main__':
    from toon.input import MpDevice
    from toon_rawinput.keyboard import Keyboard
    from toon_rawinput.mouse import Mouse

    print('sleeping-- plug in test device.')
    sleep(5)
    print('done sleeping-- good luck')
    mydev = MpDevice(Keyboard(clock=ptb.GetSecs))
    hid = ptb.PsychHID
    devs = hid('Devices')

    ms = next(d for d in devs if d['usageValue'] == 2)
    print(ms)
    #idx = ms['index'] - 1
    idx = 0
    hid('KbQueueCreate', idx)
    hid('KbQueueStart', idx)

    ptbtimes = []
    mytimes = []
    total_time = 60 * 10
    with mydev:
        t0 = time()
        hid('KbQueueFlush', idx)
        while time() - t0 < total_time:
            [evt, navail] = hid('KbQueueGetEvent', idx)
            res = mydev.read()
            if res:
                #print('mine: %s' % res.time)
                mytimes.append(res.time)
            if evt:
                #print('ptb: %s' % evt)
                ptbtimes.append(evt['Time'])
            sleep(0.02)

    hid('KbQueueStop', idx)
    hid('KbQueueRelease', idx)

    import matplotlib.pyplot as plt
    import numpy as np
    
    mytimes = np.hstack(mytimes)
    mylen = len(mytimes)

    ptbtimes = np.array(ptbtimes)
    ptblen = len(ptbtimes)

    if mylen < ptblen:
        ptbtimes = ptbtimes[-mylen:]

    if mylen % 2 != 0:
        mytimes = mytimes[1:]
        ptbtimes = ptbtimes[1:]

    print('mylen: %s, ptblen: %s' % (mylen, ptblen))

    save_data = np.vstack((mytimes, ptbtimes)).T
    np.savetxt('both.csv', save_data, delimiter=',', header='rawinput,ptb', comments='')
    # mydff = np.diff(mytimes[::2])
    # ptbdff = np.diff(ptbtimes[::2])
    # plt.plot(ptbdff, color='r', alpha=0.8)
    # plt.plot(mydff, color='b', alpha=0.8)
    # plt.show()
    # print('Press period consistency:')
    # print('mymean: %f, mysd: %f, ptbmean: %f, ptbsd: %f' % (np.mean(mydff), np.std(mydff),
    #                                                         np.mean(ptbdff), np.std(ptbdff)))
    # plt.hist(ptbdff, bins=25, alpha=0.5, color='r')    
    # plt.hist(mydff, bins=25, alpha=0.5, color='b')
    # plt.show()

    # # earlier/later? negative = ptb later, pos = mine later
    # plt.hist(mytimes[::2] - ptbtimes[::2], bins=25)
    # plt.show()

    # mytmp = mytimes[1::2] - mytimes[::2]
    # ptbtmp = ptbtimes[1::2] - ptbtimes[::2]

    # #
    # print('Press/release consistency:')
    # print('mymean: %f, mysd: %f, ptbmean: %f, ptbsd: %f' % (np.mean(mytmp), np.std(mytmp),
    #                                                         np.mean(ptbtmp), np.std(ptbtmp)))
    # plt.hist(ptbtmp, bins=30, alpha=0.5, color='r')
    # plt.hist(mytmp, bins=30, alpha=0.5, color='b')

    # plt.show()

