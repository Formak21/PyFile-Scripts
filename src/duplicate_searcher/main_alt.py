#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This program is free software. It comes without any warranty, to
# * the extent permitted by applicable law. You can redistribute it
# * and/or modify it under the terms of the Do What The Fuck You Want
# * To Public License, Version 2, as published by Sam Hocevar. See
# * http://www.wtfpl.net/ for more details.

from sys import exit
from hashlib import sha512
from os import listdir
from os.path import isfile, isdir, getsize

THREAD_AMOUNT = 16
MEMORY_AMOUNT = 28 * 1024 * 1024 * 1024
ROOT_PATH = 'C:/Users/Form49d/Desktop'
EXPORT_FILENAME = 'Duplicates.txt'
LOG_FILENAME = 'Errors.log'
SILENT_MODE = False


def print_log(data):
    if not SILENT_MODE:
        print(data)
    with open(file=LOG_FILENAME, mode='at', encoding='utf-8') as file:
        file.write(data + '\n')


def print_data(data):
    if not SILENT_MODE:
        print(data)
    with open(file=EXPORT_FILENAME, mode='at', encoding='utf-8') as file:
        file.write(data + '\n')


def sha_encoder(file_path) -> str:
    with open(file=file_path, mode='rb') as file:
        return sha512(file.read(-1)).hexdigest()


if __name__ == "__main__":

    preprocessed_files = dict()
    directories = [ROOT_PATH]

    try:
        while len(directories):

            current_path = directories[0]
            directories = directories[1:]

            for element in listdir(current_path):

                element_path = f'{current_path}/{element}'

                if isfile(element_path):
                    file_size = getsize(element_path)
                    preprocessed_files[file_size] = preprocessed_files.get(file_size, list()) + [element_path]

                elif isdir(element_path):
                    directories.append(element_path)

    except FileNotFoundError:
        print_log('Path isn\'t correct.')
        exit()

    except Exception as e:
        print_log("Unknown exception: " + str(e))
        exit()

    processed_files = dict()

    for file_size in list(preprocessed_files.keys()):

        if len(preprocessed_files[file_size]) < 2:
            preprocessed_files.pop(file_size)
            continue

        for file_path in preprocessed_files.get(file_size, list()):
            # multithread this
            file_hash = sha_encoder(file_path)
            processed_files[file_hash] = processed_files.get(file_hash, list()) + [file_path]
            # multithread this

    del preprocessed_files

    for file_hash in list(processed_files.keys()):

        if len(processed_files[file_hash]) < 2:
            processed_files.pop(file_hash)
            continue

        print_data('#' * 100 + '\n' + '\n'.join([file_object.file_path for file_object in processed_files[
            file_hash]]) + f'\n\nFound {len(processed_files[file_hash])} duplicates')
