#!/usr/bin/python

import os
import sys
import matplotlib.pyplot as plt
from collections import deque
import re
from multiprocessing.pool import Pool
from multiprocessing import Manager, JoinableQueue


# Takes a path and a pattern and returns the number of
# files matching the pattern and a list of subdirs
def search_directory(path, pattern):
    dirs = []
    count = 0
    for f in os.listdir(path):
        if(os.path.isfile(os.path.join(path,f))):
            if re.match(pattern,f):
                count = count + 1
        else:
            dirs.append(f)
    return count, dirs


# Takes a path and pattern and returns a dict for each subdir
# as key and the count of filenames matching as value
def traverse_directory(root_dir, pattern):
    directory_queue = deque([root_dir])
    res = {}
    while directory_queue:
        path = directory_queue.popleft()
        count, dirs = search_directory(path, pattern)
        res[path] = count
        for d in dirs:
            directory_queue.append(os.path.join(path,d))
    return res

# Asynchronouse worker function for threaded pool
# Must init res: Manager.dir(), dir_queue: JoinableQueue()
# and pattern: str globally before calling
def async_traverse():
    while True:
        path = dir_queue.get()
        count, dirs = search_directory(path,pattern)
        res[path] = count
        for d in dirs:
            dir_queue.put(os.path.join(path,d))
        dir_queue.task_done()

def plot_result(res):
    x = range(len(res))
    plt.bar(x, list(res.values()), align='center')
    plt.xticks(x, list(res.keys()))
    plt.ylabel('files matching keyword')
    plt.xlabel('subdir pathname')
    plt.title('Files matching keyword in path')
    plt.savefig('filecount.png')
    plt.close()

if __name__ == "__main__":

    threads = 1

    # Search if -t flag specified
    tflag = filter(lambda arg: arg.startswith('-t'), sys.argv)
    if tflag:
        sys.argv.remove(tflag[0])
        try:
            # Set number of threads according to specifer, e.g. 4 for '-t4'
            threads = int(tflag[0].split('-t')[1])
        except:
            sys.exit("Invalid -t flag specifier, specify flag with number of threads e.g. -t4")


    if len(sys.argv) != 3:
        sys.exit("Require 2 input arguments: <root_dir> <keyword>")

    pattern = sys.argv[2]
    try:
        re.compile(pattern)
    except:
        sys.exit("Invalid regex pattern")

    root_dir = sys.argv[1]

    if not os.path.isdir(root_dir):
        sys.exit("Specified root_dir is not a directory or does not exist!")

    if threads == 1:
        res = traverse_directory(root_dir, pattern)
    else: # Process multi-threaded
        # Manager dict handles concurrent write has no race condition
        # when using multithread processing
        res = Manager().dict()

        # Queue handle allocating tasks for async threads
        dir_queue = JoinableQueue()
        dir_queue.put(root_dir)

        # Init number of threads
        pool = Pool(threads)
        for _ in range(threads):
            pool.apply_async(async_traverse)

        # Wait for queue to empty
        dir_queue.join()

    print res
    plot_result(res)
