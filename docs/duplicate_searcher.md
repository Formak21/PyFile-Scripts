# Duplicate Searcher
## About
This program allows you to quickly find duplicate files in specified directory recursively. Currently, there are 2 versions available: normal (with recursive function, limited to max of 999 nested directories), and alternative (might be more stable in some edge cases, though it is slower now).
## How to use:
### Input
Use any path to the directory, as your OS supports it. Unfortunately, files relative to the user directory (~) in *nix systems are not supported as of now, but you still can specify them relative to your root directory (/) or current folder (.).
### Output
For each group of duplicates, the program outputs them as following:
```
####################################################################################################
/path/to/duplicate1
...
/path/to/duplicateN
Total: N duplicates

```
## Other information
### Speed 
No trusted measures yet, but the normal version uses threads to utilize all of your CPU, and reads files in chunks to preserve memory. Please note, that number of threads is limited to a number of files, with no more than 1 thread per file available for stability reasons. However, the program is capable of creating threads for each file, which will be executed in the order your OS believes works best for your computer. We believe reading in chunks provides best average-case time when they are about 100MiB in size, however, if you do not have that much RAM or know the exact number that works best for you, feel free to change their size in the 18 line of _main.py_ (size in bytes, text after "#" is ignored, math operations supported, "**" means raising to some power):
```python3
CHUNK_SIZE = 100 * 1024**2  # 100MiB
```
### Stability
A lot of exception-catching is done inside, though beware of files without reading permission: those might and will be marked as duplicates if there are more than 2 of them. Hidden files work in any OS regardless of what name they have. If you have strongly limited RAM, see previous paragraph with information on how to change chunk size and decrease/increase memory usage.
