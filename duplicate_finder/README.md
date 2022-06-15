# Duplicate Searcher

## About

This program allows you to quickly find duplicate files in specified directory recursively. Currently, there are 2 versions available: normal (with recursive function, limited to max of 999 nested directories by default, and alternative (might be more stable in some edge cases, though it is slower now).

## How to use:

### Input

Use any path to the directory, as your OS supports it. Files relative to the user directory (~) in \*nix systems are now also supported (only in normal version).

### Output

For each group of duplicates, the program outputs them as following:

```
####################################################################################################
/path/to/duplicate1
...
/path/to/duplicateN
Total: N duplicates
```

### Customizations

You can change the hashing algorithm, chunk size (in bytes, should not be more than available RAM), and recursion limit (maximum nested directories depth) in the following lines (`main.py`, not available in the alternative version):

```python
HASH_FUNCTION = sha1
CHUNK_SIZE = 100 * 1024**2
RECURSION_LIMIT = 1000
```

Please note, that `HASH_FUNCTION` is called from code, so when you change it, do not forget to either import it from a library, or add it to the code.

## Other information

### Speed

No trusted measures yet, but the normal version uses threads to utilize all of your CPU, and reads files in chunks to preserve memory. Please note, that number of threads is limited to a number of files, with no more than 1 thread per file available for stability reasons. However, the program is capable of creating threads for each file, which will be executed in the order your OS believes works best for your computer. We believe reading in chunks provides best average-case time when they are about 100MiB in size, however, this value can be changed if necessary.

### Stability

A lot of exception-catching is done inside, though beware of files without reading permission: those might and will be marked as duplicates if there are more than 2 of them. Hidden files work in any OS regardless of what name they have. If you have strongly limited RAM, you can change chunk size to a smaller value.

## TODO

- [x] Multithreading
- [x] Exception Handling
- [x] Nesting level limitation
- [ ] Logging
- [ ] Silent mode
- [x] Additional code comments
- [x] Launch with terminal parameter
- [x] Docs
