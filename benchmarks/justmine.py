
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

    mytimes = []
    total_time = 60 * 2
    with mydev:
        t0 = time()
        while time() - t0 < total_time:
            res = mydev.read()
            if res:
                #print('mine: %s' % res.time)
                mytimes.append(res.time)
            sleep(0.02)

    import matplotlib.pyplot as plt
    import numpy as np
    
    mytimes = np.hstack(mytimes)
    mylen = len(mytimes)
    if mylen % 2 != 0:
        mytimes = mytimes[1:]
    mydff = np.diff(mytimes[::2])

    plt.plot(mydff)
    plt.show()
    print('Press period consistency:')
    print('mymean: %f, mysd: %f' % (np.mean(mydff), np.std(mydff)))
    plt.hist(mydff, bins=25, alpha=0.5, color='b')
    plt.show()

    mytmp = mytimes[1::2] - mytimes[::2]
    #
    print('Press/release consistency:')
    print('mymean: %f, mysd: %f' % (np.mean(mytmp), np.std(mytmp)))
    plt.hist(mytmp, bins=30, alpha=0.5, color='b')

    plt.show()