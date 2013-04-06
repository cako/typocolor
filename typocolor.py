#!/usr/bin/python

import sys
import Image
import numpy as np
import matplotlib.pyplot as plt

def PIL_to_numpy(img_PIL):
    return np.array(img_PIL.getdata()).reshape(img_PIL.size[::-1])

def get_line_limits(img):
    nonwhite = np.array([])
    for i, line in enumerate(img):
        if min(line) < 125:
            nonwhite = np.append(nonwhite, i)

    limits = np.array([], dtype=np.int32)
    for i in range(len(nonwhite)):
        try:
            if (nonwhite[i] != nonwhite[i-1]+1 or
                nonwhite[i] != nonwhite[i+1] - 1):
                limits = np.append(limits, np.int32(nonwhite[i]))
        except IndexError:
            pass
    return limits

def mean_image(img, limits):
    m_img = 255*np.ones(img.shape)
    even_indexes = 2*np.array(range(len(limits)/2 + 1))
    for i in even_indexes:
        try:
            m_img[limits[i]:limits[i+1]] = np.mean(img[limits[i]:limits[i+1]])
            #print limits[i], limits[i+1], np.mean(img[limits[i]:limits[i+1]])
        except IndexError:
            pass
    return m_img

if __name__== "__main__":
    try:
        img_PIL = Image.open(sys.argv[1])
    except IOError as e:
        print 'Trouble reading the PDF. Error(%d): %s' % (e.errno, e.strerror)
        sys.exit(e.errno)
    except IndexError as e:
        print 'Must provide a filename as an argument.'
        sys.exit(e.errno)

    img = PIL_to_numpy(img_PIL)
    limits = get_line_limits(img)
    m_img = mean_image(img, limits)

    cbar = (np.min([ x for x in m_img.flatten() if x > 0]),
            np.max(m_img))

    fig = plt.figure()
    axs = plt.figure().add_subplot(1,1,1)
    axs.imshow(m_img, cmap='gray', vmin=cbar[0], vmax=cbar[1])
    plt.savefig('mean_' + sys.argv[1])

    fig = plt.figure()
    axs = plt.figure().add_subplot(1,1,1)
    axs.imshow(img, cmap='gray', vmin=cbar[0], vmax=cbar[1])
    plt.savefig('orig_' + sys.argv[1])

