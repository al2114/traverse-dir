# File Directory Traverser
`traverse.py` is a python script that recursively traverses through a directory and counts the number of files matching a given keyword/pattern in each subdirectory.

### Setup

Script has dependencies on `matplotlib.pyplot` and `regex` modules, to ensure you have required dependencies, type
```
pip install matplotlib regex
```

### Usage

To run, execute the script specifying arguments in the format:
```
./traverse.py <dir_path> <keyword>
```

`keyword` is specified as a regex pattern

An optional `-t` specifier may be provided to make use of multiple cores when running (e.g. `-t4` for 4 threads). This can speed up the routine if the directory structure is large.

### Output

The program will output to `stdout` a dictionary of key-values where key specifies a given subdirectory and the value the count of matching files found in the subdirectory (e.g. `{’a/b’: 6, ’a/b/c’: 7,
‘a/b/c/d’:0}`).

A bar chart is generated as `filecount.png` visualising the data output.

## Test cases

Test cases to consider when implementing a test-suite for this routine:

* Basic functional correctness – testing a simple directory structure and asserting the expected output (stdout and graph file generated)
* Testing different regex patterns – testing different operators (e.g. `?`,`*`,`.`,`{}` etc.) produces correct count with matching and unmatching files
* Testing correct count – count should only count files and not directories that match the specified pattern
* Test invalid inputs correctly responds with error:
  * root_dir:
  	* Specified directory does not exist
  	* Specified path is a file
  * Regex
    * Check invalid regex patterns (e.g. '[')
* Test different directory path formats work – e.g. Unix systems using `path/to/dir` vs Windows `C:\\path\to\dir`
* Scale test – e.g. testing if large numbers of nested directories or large number of subdirs under root can cause program to crash (e.g. stack overflow in deep recursion).

