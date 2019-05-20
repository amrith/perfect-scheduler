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
        tsz += objectlist[ix]
        try:
            if algo == 0:
                boxes.place_fullest(o)
            elif algo == 1:
                boxes.place_emptiest(o)
            elif algo == 2:
                boxes.place_random(o)
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


def usage():
    print("Usage %s" % sys.argv[0])
    print("\t-h|--help         Get usage")
    print("\t-i|--iterations   Number of iterations (default: 1000)")
    print("\t-b|--boxes        Number of boxes (default: 100)")
    print("\t-s|--boxsize      Size of each box (default: 50)")
    print("\t--min             Minimum object size (default: 1)")
    print("\t--max             Maximum object size (default: 30)")


def sortkeyfunc(a):
    return(len(a))


def makeobjectstream(niter, mn, mx, boxes, boxsize):
    streamlist = []
    for ix in range(0, niter):
        # reseed the random number to generate deterministic data
        random.seed(ix)

        stream = []
        total = 0
        while total != boxes * boxsize:
            assert(boxes * boxsize - total >= mn)

            if (boxes * boxsize - total <= mn and
                boxes * boxsize - total >= mx):
                o = boxes * boxsize - total
            else:
                o = random.randint(mn, mx)

            if (boxes * boxsize - total - o == 0 or
                boxes * boxsize - total - o >= mn):
                stream.append(o)
                total += o

        assert(total == boxes * boxsize)
        streamlist.append(stream)

    # we now sort streamlist based on the number of elements in each sub-list
    streamlist.sort(key=sortkeyfunc)
    return(streamlist)

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], 'hi:b:s:o:',
                                   [ 'iterations=',
                                     'boxes=',
                                     'boxsize=',
                                     'output=',
                                     'min=',
                                     'max=',
                                     'help' ])
    except getopt.GetoptError as err:
        print (str(err))
        usage()
        sys.exit(2)

    niter = 1000
    boxes = 100
    boxsize = 50
    mi = 1
    mx = 30
    output = 'simple-1d.csv'

    for o, a in opts:
        if o in ('-h', '--help'):
            usage()
            sys.exit(0)
        elif o in ('-i', '--iterations'):
            niter = int(a)
        elif o in ('-b', '--boxes'):
            boxes = int(a)
        elif o in ('-s', '--boxsize'):
            boxes = int(a)
        elif o in ('-o', '--output'):
            output = a
        elif o in ('--min'):
            mi = int(a)
        elif o in ('--max'):
            mx = int(a)
        else:
            print("Unhandled option %s" % o)
            sys.exit(1)

    if mx < mi:
        usage()
        sys.exit(1)
    elif mi > boxsize:
        usage()
        sys.exit(1)
    elif mi <= 0:
        usage()
        sys.exit(1)

    f = open(output, 'w')

    # we now make the list of object streams. The object stream is a
    # list of integers in the range [min, max] such that the sum of
    # these integers is equal to boxes * boxsize.
    objectstream = makeobjectstream(niter, mi, mx, boxes, boxsize)

    # we now reseed the random number generator with a non-deterministic
    # seed
    random.seed(datetime.now())
    for ix in range(1, niter):
        fullest = run(boxes, boxsize, 0, objectstream[ix])
        emptiest = run(boxes, boxsize, 1, objectstream[ix])
        pr = run(boxes, boxsize, 2, objectstream[ix])

        f.write("%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s\n" % (
            ix, fullest[0], fullest[1], fullest[2], fullest[3],
            emptiest[0], emptiest[1], emptiest[2], emptiest[3],
            pr[0], pr[1], pr[2], pr[3]))

    f.close()

if __name__ == "__main__":
    main()
