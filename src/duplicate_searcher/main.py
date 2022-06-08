#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This program is free software. It comes without any warranty, to
# * the extent permitted by applicable law. You can redistribute it
# * and/or modify it under the terms of the Do What The Fuck You Want
# * To Public License, Version 2, as published by Sam Hocevar. See
# * http://www.wtfpl.net/ for more details.

# This script is searches file duplicates.
from sys import exit
from hashlib import sha256
from os import listdir
from os.path import isfile, isdir


# encodes files with sha256 to check for uniqueness
def encoder(filepath) -> str:
    with open(file=filepath, mode='rb') as f:
        return sha256(f.read(-1)).hexdigest()


# global variable, thath is needed to save the founded files
# hash:[filepath1, filepath2, ...]
processed_files = dict()


def duplicate_detector(path):
    global processed_files
    directories = list()
    unprocessed_files = list()

    for element in listdir(path):
        tmp_path = f'{path}/{element}'
        if isfile(tmp_path):
            unprocessed_files.append(element)
        elif isdir(tmp_path):
            directories.append(element)

    for file in unprocessed_files:
        file = f'{path}/{file}'
        tmp_hash_key = encoder(file)
        if tmp_hash_key not in processed_files.keys():
            processed_files[tmp_hash_key] = []
        processed_files[tmp_hash_key].append(file)

    for directory in directories:
        directory = f'{path}/{directory}'
        duplicate_detector(directory)


start_path = input('Enter root path: ')

try:
    duplicate_detector(start_path)

    for hash_key in processed_files.keys():
        if len(processed_files[hash_key]) > 1:
            print('#' * 100, *processed_files[hash_key], f'\nFound {len(processed_files[hash_key])} duplicates',
                  sep='\n')

except RecursionError:
    print('Script can\'t process file paths deeper than 999 folders.')

except FileNotFoundError:
    print('Path isn\'t correct.')
    exit()
