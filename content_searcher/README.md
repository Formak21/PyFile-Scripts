# Content Searcher

## About

This program helps you to quickly search for any string in all files in a given directory. It uses multithreading to speed up the search, and also supports multiple encodings.

## How to use:

### Input

You can provide path and search query in this order as a terminal arguments, or input them during runtime. Use any path to the directory, as supported by your OS.

### Output

Apart from progress information, the program outputs results in the following format:

```
/full/path/to/file1
/full/path/to/file2
...
/full/path/to/fileN

Total: N
```

### Customizations

You can change some settings in `main.py`. These are the defaults:

```python
# User-defined settings
RECURSION_LIMIT = 1000
LOGGING = False
SILENT = False
ENCODING = "utf-8"
```

`ENCODING` must be from those supported by Python when opening a file.

## Other information

### Speed

Not measured, but not should be limited in any way but by your memory, disk IO, and CPU speed.

### Stability

A lot of error-handling was done, though there are still a few restrictions, such as:

- If you do not have enough memory to load a file, search cannot be performed because of OS Error.
- In case file uses different encoding, you have to specify it, or it will not work.
- If different files use different encodings, chances are search results will be incomplete.

Moreover, file has to be loaded to RAM completely before searching, which might lead to temporary performance degradation.

## TODO

- [x] Multithreading
- [x] Exception Handling
- [x] Nesting level limitation
- [ ] Logging
- [x] Silent mode
- [x] Launch with terminal parameters
- [ ] Docs
- [ ] Regex
