#!/usr/bin/env python3
# -*- coding: utf-8 -*-


# This program is free software. It comes without any warranty, to
# * the extent permitted by applicable law. You can redistribute it
# * and/or modify it under the terms of the Do What The Fuck You Want
# * To Public License, Version 2, as published by Sam Hocevar. See
# * http://www.wtfpl.net/ for more details.

# This script is searches file duplicates.
from hashlib import sha256
from os import listdir
from os.path import isfile, isdir

# how many threads does have your processor
THREAD_AMOUNT = 16


class EncoderThread:
    def __init__(self):
        # variable, that is needed to save founded by thread files
        # hash:[filepath1, filepath2, ...]
        self.thread_processed_files = dict()

    # encodes files with sha256 to check for uniqueness
    def sha_encoder(self, filepath) -> str:
        encoder = sha256()
        with open(file=filepath, mode="rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(1024)
                encoder.update(chunk)
        return encoder.hexdigest()

    # function that calculates and saves hash values for list of files
    def executor(self, files_path, unprocessed_files):
        for file in unprocessed_files:
            file = f"{files_path}/{file}"
            t_hash_key = self.sha_encoder(file)
            if t_hash_key not in self.thread_processed_files.keys():
                self.thread_processed_files[t_hash_key] = []
            self.thread_processed_files[t_hash_key].append(file)


# there will be multithreading
encoder_threads = [EncoderThread() for _ in range(THREAD_AMOUNT)]


# recursive function that searches files and directories in given path
def duplicate_detector(path):
    directories = list()
    unprocessed_files = list()

    for element in listdir(path):
        tmp_path = f"{path}/{element}"
        if isfile(tmp_path):
            unprocessed_files.append(element)
        elif isdir(tmp_path):
            directories.append(element)

    encoder_thread = encoder_threads[0]  # here will be multithreading
    encoder_thread.executor(path, unprocessed_files)

    for directory in directories:
        directory = f"{path}/{directory}"
        duplicate_detector(directory)


# function that needed for unification thread_processed_files dicts in one single
def get_processed_files() -> dict:
    processed_files = dict()
    processed_files_keys = set()

    for encoder_thread in encoder_threads:
        processed_files_keys = set.union(
            processed_files_keys,
            set(encoder_thread.thread_processed_files.keys()),
        )

    processed_files_keys = list(processed_files_keys)

    for t_hash_key in processed_files_keys:
        processed_files[t_hash_key] = []
        for encoder_thread in encoder_threads:
            processed_files[
                t_hash_key
            ] += encoder_thread.thread_processed_files.get(t_hash_key, [])

    return processed_files


if __name__ == "__main__":

    start_path = input("Enter root path: ")

    try:
        duplicate_detector(start_path)

        processed_files = get_processed_files()
        for hash_key in processed_files.keys():
            if len(processed_files[hash_key]) > 1:
                print(
                    "#" * 100,
                    *processed_files[hash_key],
                    f"\nFound {len(processed_files[hash_key])} duplicates",
                    sep="\n",
                )

    except RecursionError:
        print("Script can't process file paths deeper than 999 directories.")

    except FileNotFoundError:
        print("Path isn't correct.")
