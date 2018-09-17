#!/usr/bin/python

import os
import sys
import matplotlib.pyplot as plt
from collections import deque
import re

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
    if len(sys.argv) != 3:
        sys.exit("Require 2 input arguments: <root_dir> <keyword>")

    root_dir = sys.argv[1]
    pattern = sys.argv[2]
    res = traverse_directory(root_dir, pattern)
    print res
    plot_result(res)
