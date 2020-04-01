from psychopy.iohub import launchHubServer
from psychopy.core import getTime
from time import sleep

if __name__ == '__main__':
    # Start the ioHub process. 'io' can now be used during the
    # experiment to access iohub devices and read iohub device events.
    io = launchHubServer()

    keyboard = io.devices.keyboard

    # Check for and print any Keyboard events received for 5 seconds.
    print('sleeping-- plug in test device.')
    sleep(5)
    print('done sleeping-- good luck')

    times = []
    stime = getTime()
    tmp = 60.0*2
    while getTime()-stime < tmp:
        for e in keyboard.getEvents():
            times.append(e.time)

    # Stop the ioHub Server
    io.quit()

    import matplotlib.pyplot as plt
    import numpy as np

    ptbtimes = np.array(times)
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
