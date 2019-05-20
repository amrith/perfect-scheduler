#!/usr/bin/python
#

from datetime import datetime
import getopt
import random
import sys

#
# a test of an algorithm to determine virtual machine placement.
#

class Object:
    def __init__(self, ix, size):
        if type(ix) is int:
            self._ix = ix
        else:
            raise(Exception("ix should be an integer."))

        if type(size) is list:
            self._size = size
        else:
            raise(Exception("size should be a list."))

    def __repr__(self):
        return("Object %s of size %s" % (self._ix, self._size))

    # return the un-scaled size of the object. The caller (box.totalsize)
    # will scale it appropriately
    def size(self):
        return(self._size)


class Box:
    def __init__(self, ix, limit):
        self._objects = []
        self._tsz = [0.0] * len(limit)

        if type(ix) is int:
            self._ix = ix
        else:
            raise(Exception("ix should be an integer."))

        if type(limit) is list:
            self._limit = limit
        else:
            raise(Exception("limit should be a list."))

    def __repr__(self):
        return("Box %s: Size %s, Used %s, Objects: %s" % (
                self._ix,
                self._limit,
                self.totalsize(),
                self.count()))

    def count(self):
        return len(self._objects)

    def limit(self):
        return (1.0)

    def totalsize(self):
        tsz = 1.0
        for ix in range(0, len(self._limit)):
            tsz *= float(self._tsz[ix]) / float(self._limit[ix])

        return(tsz)

    def fits(self, object):
        osz = object.size()
        for ix in range(0, len(self._limit)):
            if self._tsz[ix] + osz[ix] > self._limit[ix]:
                return False

        return True

    def free(self):
        return (1.0 - self.totalsize())

    def place(self, object):
        assert(self.fits(object))
        self._objects.append(object)
        osz = object.size()
        for ix in range(0, len(self._limit)):
            self._tsz[ix] += osz[ix]


class Boxes:
    def __init__(self):
        self._list = []

    def boxlist(self):
        return(self._list)

    def add(self, box):
        self._list.append(box)


    def place_fullest(self, object):
        p = None
        fs = 0.0

        for b in self._list:
            if b.fits(object):
                if p is None or b.free() < fs:
                    p = b
                    fs = b.free()

        if p is not None:
            p.place(object)
        else:
            raise(Exception(
                    "No place to place object of size %s." % object.size()))

    def place_emptiest(self, object):
        p = None
        fs = 0.0

        for b in self._list:
            if b.fits(object):
                if p is None or b.free() > fs:
                    p = b
                    fs = b.free()

        if p is not None:
            p.place(object)
        else:
            raise(Exception(
                    "No place to place object of size %s." % object.size()))

    def place_random(self, object):
        possible = []
        for ix in range(0, len(self._list)):
            if self._list[ix].fits(object):
                possible.append(ix)

        if len(possible) == 0:
            raise(Exception("No place to put object of size %s." %
                            object.size()))
        else:
            # possible is a list of places where we can put this
            # now pick one at random.
            try:
                p = random.randint(0, len(possible)-1)
                b = self._list[possible[p]]
                b.place(object)
            except Exception as e:
                print(str(e))
                raise


def run (bx, bl, algo, objectlist):
    boxes = Boxes()
    for ix in range(1, bx):
        b = Box(ix, bl)
        boxes.add(b)

    tsz = 0
    ix = 1
    while True:
        o = Object(ix, objectlist[ix])
        ix += 1
        try:
            if algo == 0:
                boxes.place_fullest(o)
            elif algo == 1:
                boxes.place_emptiest(o)
            elif algo == 2:
                boxes.place_random(o)
            else:
                raise(Exception("Unknown algorithm"))
        except Exception as e:
            break

    u = 0
    c = 0

    for b in boxes.boxlist():
        tsz += b.totalsize()
        if b.totalsize() > 0:
            u += (float(b.totalsize()) / b.limit())
            c += 1

    return(ix, tsz, 0, (100*u/c))


def usage():
    print("Usage %s" % sys.argv[0])
    print("\t-h|--help         Get usage")
    print("\t-i|--iterations   Number of iterations (default: 1000)")
    print("\t-b|--boxes        Number of boxes (default: 100)")
    print("\t-s|--boxsize      Size of each box (default: 50)")
    print("\t--min             Minimum object size (default: 1)")
    print("\t--max             Maximum object size (default: 30)")


def makeobjectstream(niter, mn, mx, boxes, boxsize):
    streamlist = []
    for ix in range(0, niter):
        # reseed the random number to generate deterministic data
        random.seed(ix)

        stream = []
        total = [0.0] * len(mn)
        for iy in range(0, 1000):
            dims = []
            for iz in range(0, len(mn)):
                dims.append(random.randint(mn[iz], mx[iz]))

            stream.append(dims)

        streamlist.append(stream)

    return(streamlist)


def main(niter, boxes, boxsize, mi, mx, output):
    # we now make the list of object streams. The object stream is a
    # list of integers in the range [min, max] such that the sum of
    # these integers is equal to boxes * boxsize.
    objectstream = makeobjectstream(niter, mi, mx, boxes, boxsize)

    # we now reseed the random number generator with a non-deterministic
    # seed
    random.seed(datetime.now())
    results = []

    for ix in range(0, niter):
        fullest = run(boxes, boxsize, 0, objectstream[ix])
        emptiest = run(boxes, boxsize, 1, objectstream[ix])
        pr = run(boxes, boxsize, 2, objectstream[ix])
        results.append([ix, fullest[0], fullest[1], fullest[2], fullest[3],
                        emptiest[0], emptiest[1], emptiest[2], emptiest[3],
                        pr[0], pr[1], pr[2], pr[3]])
        if ix % 100 == 0:
            sys.stdout.write('.')
            sys.stdout.flush()

    sys.stdout.write('\n')
    sys.stdout.flush()

    f = open(output, 'w')
    for r in results:
        # renumber the results
        f.write(', '.join([str(i) for i in r]))
        f.write('\n')

    f.close()

if __name__ == "__main__":
    main(1000, 100, [50, 50], [1, 1], [30, 30],
         'simple-md.csv')
    main(1000, 100, [50, 50000], [1, 1000], [30, 30000],
         'simple-md-vsz-scaled.csv')
    main(1000, 100, [50, 50000], [1, 100], [30, 3000],
         'simple-md-vsz-not-scaled.csv')
