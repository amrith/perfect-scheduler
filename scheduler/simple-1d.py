#!/usr/bin/python
#

import random

#
# a test of an algorithm to determine virtual machine placement.
#

class Object:
    def __init__(self, ix, size):
        if type(ix) is int:
            self._ix = ix
        else:
            raise(Exception("ix should be an integer."))

        if type(size) is int:
            self._size = size
        else:
            raise(Exception("size should be an integer."))

    def __repr__(self):
        return("Object %s of size %s" % (self._ix, self._size))

    def size(self):
        return(self._size)


class Box:
    def __init__(self, ix, limit):
        self._objects = []

        if type(ix) is int:
            self._ix = ix
        else:
            raise(Exception("ix should be an integer."))

        if type(limit) is int:
            self._limit = limit
        else:
            raise(Exception("limit should be an integer."))

    def __repr__(self):
        return("Box %s: Size %s, Used %s, Objects: %s" % (
                self._ix,
                self._limit,
                self.totalsize(),
                self.count()))

    def count(self):
        return len(self._objects)

    def limit(self):
        return (self._limit)

    def totalsize(self):
        sz = 0
        for o in self._objects:
            sz += o.size()

        return(sz)

    def fits(self, object):
        return (self.totalsize() + object.size() <= self._limit)

    def free(self):
        return (self._limit - self.totalsize())

    def place(self, object):
        assert(self.fits(object))
        self._objects.append(object)


class Boxes:
    def __init__(self):
        self._list = []

    def boxlist(self):
        return(self._list)

    def add(self, box):
        self._list.append(box)

    def biggest(self):
        sz = 0
        box = None
        for b in self._list:
            a = b.limit() - b.totalsize()
            if box is None or a > sz:
                sz = a
                box = b

        return(box, sz)

    def place_fullest(self, object):
        p = None
        sz = 0

        for b in self._list:
            if b.fits(object):
                if p is None or b.totalsize() > sz:
                    p = b
                    sz = b.totalsize()

        if p is not None:
            p.place(object)
        else:
            raise(Exception(
                    "No place to place object of size %s." % object.size()))

    def place_emptiest(self, object):
        p = None
        sz = 0

        for b in self._list:
            if b.fits(object):
                if p is None or b.free() > sz:
                    p = b
                    sz = b.free()

        if p is not None:
            p.place(object)
        else:
            raise(Exception(
                    "No place to place object of size %s." % object.size()))


def main(bx, bl, algo):
    boxes = Boxes()
    for ix in range(1, bx):
        b = Box(ix, bl)
        boxes.add(b)

    tsz = 0
    ix = 1
    while True:
        osz = random.randint(1, 32)
        o = Object(ix, osz)
        ix += 1
        tsz += osz
        try:
            if algo == 0:
                boxes.place_fullest(o)
            elif algo == 1:
                boxes.place_emptiest(o)
            else:
                raise(Exception("Unknown algorithm"))
        except:
            break

    u = 0
    c = 0

    for b in boxes.boxlist():
        if b.totalsize() > 0:
            u += (float(b.totalsize()) / b.limit())
            c += 1

    return(ix, tsz, boxes.biggest()[1], (100*u/c))


if __name__ == "__main__":
    niter = 1000
    f = open('runs.csv', 'w')

    for ix in range(1, niter):
        random.seed(ix)
        fullest = main(20, 50, 0)
        random.seed(ix)
        emptiest = main(20, 50, 1)

        f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
                ix, fullest[0], fullest[1], fullest[2], fullest[3],
                emptiest[0], emptiest[1], emptiest[2], emptiest[3]))

    f.close()





