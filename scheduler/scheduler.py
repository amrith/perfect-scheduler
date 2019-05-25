#!/usr/bin/python

#
# scheduler.py
#
# a simple simulator for object placement simulation, and to help model
# the behavior of Nova object placement.
#
# Amrith
#

import logging
import random
import getopt
import sys
import numpy

#
# the object. this is the thing that gets placed into boxes
#

class Object:
    def __init__(self, objid, size):
        self._objid = objid

        if type(size) is list:
            self._size = size
        elif type(size) is int:
            self._size = [size]
        else:
            str = ("The size of an object should either be an int or a list "
                   "and not %s which is an %s." % (size, type(size)))
            logging.error(str)
            raise(Exception(str))

        logging.debug("Created object %(objid)s of size %(size)s.", {
            "objid": objid, "size": size })

    def __repr__(self):
        return("Object %s, size %s" % (self._objid, self._size))

    def size(self):
        return(self._size)


def compute_volume(a):
    volume = 1.0
    for ix in range(0, len(a)):
        volume *= a[ix]

    return(volume)

class Box:
    def __init__(self, boxid, size):
        self._objlist = []
        self._boxid = boxid

        if type(size) is list:
            self._size = size
        elif type(size) is int:
            self._size = [size]
        else:
            str = ("The size of a box should either be an int or a list "
                   "and not %s which is an %s." % (size, type(size)))
            logging.error(str)
            raise(Exception(str))

        self._size = size
        self._used = [0.0] * len(size)

        self._volume = compute_volume(size)
        self._volume_used = 0.0

        logging.debug("Created box %(boxid)s of size %(size)s.", {
            "boxid": boxid, "size": size })

    def __repr__(self):
        return("Box %s, size %s" % (self._boxid, self._size))

    def occupancy(self):
        return(len(self._objlist))

    def size(self):
        return(self._size)

    def volume(self):
        return(self._volume)

    def utilization(self):
        return(self._volume_used / self._volume)

    def fits(self, obj):
        objsize = obj.size()
        for ix in range(0, len(self._size)):
            if self._used[ix] + objsize[ix] > self._size[ix]:
                logging.debug("Object %(obj)s will not fit in Box %(box)s.",
                              {"obj": obj, "box": self})
                return False

        logging.debug("Object %(obj)s will fit in Box %(box)s.",
                      {"obj": obj, "box": self})
        return True

    def place(self, obj):
        if self.fits(obj):
            self._objlist.append(obj)
            objsize = obj.size()
            for ix in range(0, len(self._size)):
                self._used[ix] += objsize[ix]

            self._volume_used = compute_volume(self._used)
            logging.debug("Placed object %(obj)s in Box %(box)s.",
                          {"obj": obj, "box": self})
            return True

        logging.error("Object %(obj)s will not fit in Box %(box)s.",
                      {"obj": obj, "box": self})
        return False

class Boxes:
    algorithms = ['fullest', 'emptiest', 'random',
                  'first', 'smallest', 'largest']

    def __init__(self):
        self._boxlist = []

    def addbox(self, boxid, size):
        box = Box(boxid, size)
        self._boxlist.append(box)
        logging.debug("Added box %(box)s.", { "box": box })

    def occupancy(self):
        o = 0
        for b in self._boxlist:
            o += b.occupancy()

        return(o)

    def utilization(self):
        u = []
        for b in self._boxlist:
            u.append(b.utilization())

        return(round(100.0 * numpy.mean(u), 3))

    def place(self, obj, algorithm):
        if algorithm not in self.algorithms:
            str = "Unknown algorithm %s." % algorithm
            logging.error(str)
            raise(Exception(str))

        try:
            method_name = "place_%s" % algorithm
            method = getattr(self, "place_%s" % algorithm)
        except Exception as err:
            logging.error(str(err))
            raise err

        logging.debug("Calling %(method)s for %(obj)s.", {
            "method": method_name, "obj": obj })
        return method(obj)

    def place_fullest(self, obj):
        choose = None
        used = 0.0
        for box in self._boxlist:
            if box.fits(obj):
                bu = box.utilization()
                if choose is None or bu > used:
                    choose = box
                    used = bu

        if choose is not None:
            logging.debug("Placing %(obj)s in %(box)s.", {
                "obj": obj, "box": choose })
            choose.place(obj)
            return True

        logging.debug("No place to put %(obj)s.", { "obj": obj })
        return False

    def place_emptiest(self, obj):
        choose = None
        used = 0.0
        for box in self._boxlist:
            if box.fits(obj):
                bu = box.utilization()
                if choose is None or bu < used:
                    choose = box
                    used = bu

        if choose is not None:
            logging.debug("Placing %(obj)s in %(box)s.", {
                "obj": obj, "box": choose })
            choose.place(obj)
            return True

        logging.debug("No place to put %(obj)s.", { "obj": obj })
        return False

    def place_random(self, obj):
        bl = []
        for box in self._boxlist:
            if box.fits(obj):
                bl.append(box)

        if len(bl) == 0:
            logging.debug("No place to put %(obj)s.", { "obj": obj })
            return False

        choose = random.choice(bl)
        logging.debug("Placing %(obj)s in %(box)s.",
                      {"obj": obj, "box": choose})
        choose.place(obj)
        return True

    def place_first(self, obj):
        for box in self._boxlist:
            if box.fits(obj):
                logging.debug("Placing %(obj)s in %(box)s.", {
                    "obj": obj, "box": box })
                box.place(obj)
                return True

        logging.debug("No place to put %(obj)s.", { "obj": obj })
        return False

    def place_smallest(self, obj):
        choose = None
        v = 0.0
        for box in self._boxlist:
            if box.fits(obj):
                bv = box.volume()
                if choose is None or bv < v:
                    choose = box
                    v = bv

        if choose is not None:
            logging.debug("Placing %(obj)s in %(box)s.", {
                "obj": obj, "box": choose })
            choose.place(obj)
            return True

        logging.debug("No place to put %(obj)s.", { "obj": obj })
        return False


    def place_largest(self, obj):
        choose = None
        v = 0.0
        for box in self._boxlist:
            if box.fits(obj):
                bv = box.volume()
                if choose is None or bv > v:
                    choose = box
                    v = bv

        if choose is not None:
            logging.debug("Placing %(obj)s in %(box)s.", {
                "obj": obj, "box": choose })
            choose.place(obj)
            return True

        logging.debug("No place to put %(obj)s.", { "obj": obj })
        return False


def usage():
    print("Usage %s" % sys.argv[0])
    print("\t-h     Show this usage")
    print("\t-v     Enable verbose logging")
    print("\t-i N   Run N iterations (default: 1000)")


def makemore(totalsize, listsize):
    assert(len(totalsize) == len(listsize))

    for ix in range(0, len(totalsize)):
        if listsize[ix] < totalsize[ix]:
            return True

    return False


def sortresults(a):
    return(a[0])


def simulate(dimensions, boxsizes, output, objectstream):
    logging.warning("Running simulation.")
    results = []
    iteration = 0
    total = len(objectstream)
    test = output.replace('.csv', '')
    for objlist in objectstream:
        if iteration % 10 == 0:
            logging.warning("Beginning iteration %(iteration)s of "
                            "%(total)s.", {
                                "iteration": iteration, "total": total})
        iteration += 1
        r = [iteration]

        for algorithm in Boxes.algorithms:
            logging.info("Beginning simulation, making Boxes(), "
                            "algorithm is %(a)s", {"a": algorithm})
            boxes = Boxes()

            for bs in boxsizes:
                for ix in range(0, bs["count"]):
                    boxes.addbox(ix, bs["size"])

            logging.debug("Created all boxes.")
            for ix in range(0, len(objlist)):
                if not boxes.place(objlist[ix], algorithm):
                    # we're done, we were not able to place this object
                    occupancy = boxes.occupancy()
                    assert(occupancy == ix)
                    utilization = boxes.utilization()
                    logging.info("Done: occupancy = %(o)s, "
                                 "utilization = %(u)s %%.",
                                 {"o": occupancy, "u": utilization})
                    r.append(occupancy)
                    r.append(utilization)
                    break

        results.append(r)

    logging.warning("Done with simulation.")
    of = open(output, 'w')
    for r in results:
        of.write(' '.join([str(s) for s in r]) + '\n')

    of.close()

    # results is a list of entries, each entry is a list that has an
    # iteration number, and two values for each algorithm. Transpose
    # and sort that data.
    summary = []
    ix = 1
    for algorithm in Boxes.algorithms:
        oc = [r[ix] for r in results]
        sr = [algorithm]
        sr.append(numpy.min(oc))
        sr.append(numpy.max(oc))
        sr.append(round(numpy.mean(oc), 3))
        sr.append(round(numpy.std(oc), 3))

        ut = [r[ix+1] for r in results]
        sr.append(numpy.min(ut))
        sr.append(numpy.max(ut))
        sr.append(round(numpy.mean(ut), 3))
        sr.append(round(numpy.std(ut), 3))

        summary.append(sr)

        ix += 2

    sf = open(test + "-summary.csv", 'w')
    for sr in summary:
        sf.write(' '.join([str(s) for s in sr]) + '\n')

    sf.close()

    return

def sortfunc(a):
    return(len(a))

def run(iterations, dimensions, boxes, objsizes, output):
    logging.warning("Running %(iteration)s iterations with %(dimensions)s "
                    "dimensions.", {"iteration": iterations,
                                    "dimensions": dimensions})
    # do validation as we go
    assert(dimensions == len(objsizes))

    # how big is the entire system?
    totalsize = [0] * dimensions

    for ix in range(0, len(boxes)):
        # how big is this set of boxes?
        be = boxes[ix]

        # the boxelement is a dictionary with a count and a size
        assert(dimensions == len(be["size"]))
        for iy in range(0, dimensions):
            totalsize[iy] += be["count"] * be["size"][iy]

    logging.info("Total system size is %(size)s.", {"size": totalsize})

    # then make the object stream which will be used for all simulations. We
    # do this because the random placement method also uses the PRNG and since
    # we want the same scenario for all placements, we have to make them up
    # ahead of time. We make enough objects to at least occupy totalsize of
    # resources.
    logging.info("Making objectstreams.")
    objectstream = []
    for ix in range(0, iterations):
        logging.debug("Making object stream for iteration %(ix)s.", {"ix": ix})

        objlist = []
        listsize = [0] * dimensions

        # random seeding here makes sure that we can generate a deterministic
        # data set each time.
        random.seed(ix)
        objid = 1
        xval = 0
        while makemore(totalsize, listsize):
            objsize = []
            for iy in range(0, dimensions):
                assert(len(objsizes[iy]) == 3)
                # objsizes must be a list of length 3, min, max and scale.
                # if min and max are both 0, then scale is used to multiply
                # the 0th dimension value
                if not (iy != 0 and
                        objsizes[iy][0] == 0 and
                        objsizes[iy][1] == 0):
                    objdim = random.randint(objsizes[iy][0],
                                            objsizes[iy][1])
                    xval = objdim
                else:
                    objdim = xval

                objdim *= objsizes[iy][2]

                objsize.append(objdim)
                listsize[iy] += objdim

            obj = Object(objid, objsize)
            objid += 1

            objlist.append(obj)

        logging.debug("Completed object stream for iteration %(ix)s "
                      "with %(count)s objects. listsize is %(size)s.", {
                          "ix": ix, "count": objid-1, "size": listsize})
        objectstream.append(objlist)

    logging.info("Completed making object streams.")
    objectstream.sort(key=sortfunc)

    # now we have object streams, run the simulations
    simulate(dimensions, boxes, output, objectstream)
    return

def main():
    verbose = 0
    iterations = 1000

    try:
        opts, args = getopt.getopt(sys.argv[1:], 'vh')
    except getopt.GetoptError as err:
        print(str(err))
        sys.exit(1)

    for o, a in opts:
        if o in ('-v'):
            verbose += 1
        elif o in ('-h'):
            usage()
            sys.exit(0)
        elif o in ('-i'):
            iterations = int(a)
        else:
            print("Unhandled option %s" % o)
            sys.exit(1)

    if verbose == 0:
        ll = logging.WARN
    elif verbose == 1:
        ll = logging.INFO
    else:
        ll = logging.DEBUG

    logging.basicConfig(format='%(asctime)s [%(levelname)s] %(message)s',
                        datefmt='%Y-%m-%d %H:%M:%S', level=ll)

    run(iterations, 1, [{"count": 50, "size": [50]}],
        [[1, 30, 1]], 'simulate-1d.csv')
    run(iterations, 2, [{"count": 50, "size": [50, 50]}],
        [[1, 30, 1], [1, 30, 1]], 'simulate-2d.csv')
    run(iterations, 3, [{"count": 50, "size": [50, 50, 50]}],
        [[1, 30, 1], [1, 30, 1], [1, 30, 1]], 'simulate-3d.csv')
    run(iterations, 3, [{"count": 50, "size": [50, 500, 5000]}],
        [[1, 30, 1], [0, 0, 10], [0, 0, 100]], 'simulate-3d-scaled.csv')
    run(iterations, 1, [{"count": 20, "size": [50]},
                        {"count": 20, "size": [20]},
                        {"count": 20, "size": [100]},
                        {"count": 20, "size": [30]}],
        [[1, 30, 1]], 'simulate-1d-multisize.csv')
    run(iterations, 2, [{"count": 20, "size": [20, 20000]},
                        {"count": 20, "size": [300, 30000]},
                        {"count": 20, "size": [75, 7500]},
                        {"count": 20, "size": [100, 10000]}],
        [[1, 30, 1], [1, 30, 100]], 'simulate-2d-multisize.csv')
    run(iterations, 3, [{"count": 20, "size": [150, 15000, 1500]},
                        {"count": 20, "size": [50, 5000, 500]},
                        {"count": 20, "size": [200, 20000, 2000]},
                        {"count": 20, "size": [100, 10000, 1000]}],
        [[1, 30, 1], [1, 30, 100], [1, 30, 10]],
        'simulate-3d-multisize.csv')
    run(iterations, 3, [{"count": 20, "size": [150, 15000, 1500]},
                        {"count": 20, "size": [15, 1500, 150]},
                        {"count": 20, "size": [30, 3000, 300]},
                        {"count": 20, "size": [60, 6000, 600]}],
        [[1, 30, 1], [0, 0, 100], [0, 0, 10]],
        'simulate-3d-scaled-multisize.csv')


if __name__ == "__main__":
    main()
