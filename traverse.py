#!/usr/bin/python

import os
import sys
import matplotlib.pyplot as plt
from collections import deque
import re


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

if __name__ == "__main__":
    if(len(sys.argv) == 3):
        root_dir = sys.argv[1]
        pattern = sys.argv[2]
        res = traverse_directory(root_dir, pattern)
        print res

    else:
        print "Require 2 input arguments: <root_dir> <pattern>"
