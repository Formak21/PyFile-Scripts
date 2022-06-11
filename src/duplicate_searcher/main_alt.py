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
import threading

# Parameters
MEMORY_AMOUNT = 28 * 1024 * 1024 * 1024
ROOT_PATH = 'C:/Users/Form49d/Desktop'
EXPORT_FILENAME = 'Duplicates.txt'
LOG_FILENAME = 'Errors.log'
SILENT_MODE = False

# Global vars
encoders_list = []
threads_list = []


# function that needed to print program log
def print_log(data: str):
    if not SILENT_MODE:
        print(data)
    with open(file=LOG_FILENAME, mode='at', encoding='utf-8') as file:
        file.write(data + '\n')


# function that needed to print founded duplicates
def print_data(data: str):
    if not SILENT_MODE:
        print(data)
    with open(file=EXPORT_FILENAME, mode='at', encoding='utf-8') as file:
        file.write(data + '\n')


# encodes files with sha512 to check for uniqueness
def sha_encoder(file_path: str) -> str:
    with open(file=file_path, mode='rb') as file:
        return sha512(file.read(-1)).hexdigest()


class EncoderThread:
    def __init__(self):
        # variable, that is needed to save founded by thread files
        # hash:[filepath1, filepath2, ...]
        self.thread_processed_files = dict()

    # function that calculates and saves hash values for list of files
    def executor(self, unprocessed_files: list[str]) -> None:
        for file_path in unprocessed_files:
            t_hash_key = sha_encoder(file_path)
            self.thread_processed_files[t_hash_key] = self.thread_processed_files.get(t_hash_key, list()) + [file_path]


# function to get dictionaries from all threads
def get_processed_files() -> dict:
    processed_files = dict()
    processed_files_keys = set()

    for encoder_thread in encoders_list:
        processed_files_keys = set.union(
            processed_files_keys,
            set(encoder_thread.thread_processed_files.keys()),
        )

    processed_files_keys = list(processed_files_keys)
    for t_hash_key in processed_files_keys:
        processed_files[t_hash_key] = []
        for encoder_thread in encoders_list:
            processed_files[
                t_hash_key
            ] += encoder_thread.thread_processed_files.get(t_hash_key, list())

    return processed_files


if __name__ == "__main__":

    processed_files = dict()
    directories = [ROOT_PATH]

    try:
        while len(directories):

            current_path = directories[0]
            directories = directories[1:]

            for element in listdir(current_path):

                element_path = f'{current_path}/{element}'

                if isfile(element_path):
                    file_size = getsize(element_path)
                    processed_files[file_size] = processed_files.get(file_size, list()) + [element_path]

                elif isdir(element_path):
                    directories.append(element_path)

    except FileNotFoundError:
        print_log('Path isn\'t correct.')
        exit()

    except Exception as e:
        print_log("Unknown exception: " + str(e))
        exit()

    try:
        for file_size in list(processed_files.keys()):

            if len(processed_files[file_size]) < 2:
                continue

            encoders_list.append(EncoderThread())
            encoders_list[-1].executor(processed_files[file_size])
        '''
            threads_list.append(
                threading.Thread(
                    target=encoders_list[-1].executor,
                    args=(processed_files[file_size]),
                    daemon=True,
                )
            )
            threads_list[-1].start()


        for thread in threads_list:
            thread.join()
        '''

        processed_files = get_processed_files()

        for file_hash in list(processed_files.keys()):

            if len(processed_files[file_hash]) < 2:
                processed_files.pop(file_hash)
                continue

            print_data('#' * 100 + '\n' + '\n'.join(processed_files[file_hash])
                       + f'\n\nFound {len(processed_files[file_hash])} duplicates')

    except Exception as e:
        print_log("Unknown exception: " + str(e))