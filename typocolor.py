#!/usr/bin/python

import sys
import Image
import numpy as np

def PIL_to_numpy(img_PIL):
    #return np.asarray(img_PIL).astype(np.uint8)
    return np.array(img_PIL.getdata()).reshape(img_PIL.size[::-1])

def get_line_limits(img):
    nonwhite = np.array([], dtype=np.int32)
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
    m_img = 255*np.ones(img.shape, dtype=np.uint8)
    even_indexes = 2*np.array(range(len(limits)/2 + 1))
    for i in even_indexes:
        try:
            mean = np.uint8(np.mean(img[limits[i]:limits[i+1]]))
            m_img[limits[i]:limits[i+1]] = mean
            #print limits[i], limits[i+1], mean
        except IndexError:
            pass
    return m_img

if __name__== "__main__":
    try:
        img_PIL = Image.open(sys.argv[1])
    except IOError as e:
        print 'Trouble reading the image. Error(%d): %s' % (e.errno, e.strerror)
        sys.exit(e.errno)
    except IndexError as e:
        print 'Must provide a filename as an argument.'
        sys.exit(e.errno)

    img = PIL_to_numpy(img_PIL)
    limits = get_line_limits(img)
    m_img = mean_image(img, limits)
    m_img_PIL = Image.fromarray(m_img)
    m_img_PIL.save('mean_' + sys.argv[1])

    img_PIL = img_PIL.convert("RGBA")
    m_img_PIL = m_img_PIL.convert("RGBA")
    overlay_PIL = Image.blend(m_img_PIL, img_PIL, 0.5)
    overlay_PIL.save('overlay_' + sys.argv[1])

