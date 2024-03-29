#!/usr/bin/env python3
# -*- coding: utf-8 -*-

# This program is free software. It comes without any warranty, to
# * the extent permitted by applicable law. You can redistribute it
# * and/or modify it under the terms of the Do What The Fuck You Want
# * To Public License, Version 2, as published by Sam Hocevar. See
# * http://www.wtfpl.net/ for more details.

# This script is searches file duplicates.
from hashlib import sha512
from os import listdir
from os.path import isfile, isdir
import threading

CHUNK_SIZE = 100 * 1024 ** 2  # 100MiB


class EncoderThread:
    def __init__(self):
        # variable, that is needed to save founded by thread files
        # hash:[filepath1, filepath2, ...]
        self.thread_processed_files = dict()

    # encodes files with sha512 to check for uniqueness
    def sha_encoder(self, file_path: str) -> str:
        try:
            encoder = sha512()
            with open(file=file_path, mode="rb") as file:
                chunk = file.read(CHUNK_SIZE)
                while chunk != b"":
                    encoder.update(chunk)
                    chunk = file.read(CHUNK_SIZE)
            return encoder.hexdigest()
        except Exception as ex:
            print(f"Unknown exception: {ex}")
            return "-1"

    # function that calculates and saves hash values for list of files
    def executor(self, files_path: str, unprocessed_files: list[str]) -> None:
        for file in unprocessed_files:
            file = f"{files_path}/{file}"
            t_hash_key = self.sha_encoder(file)
            if t_hash_key not in self.thread_processed_files.keys():
                self.thread_processed_files[t_hash_key] = []
            self.thread_processed_files[t_hash_key].append(file)


# Saving all threads to read results later
encoders_list = []
threads_list = []


def duplicate_detector(path: str) -> None:
    """
    This function finds all duplicates in specified directory recursively.
    """
    directories = []

    for element in listdir(path):
        tmp_path = f"{path}/{element}"
        if isfile(tmp_path):
            # Create and start a thread for each file
            encoders_list.append(EncoderThread())
            threads_list.append(
                threading.Thread(
                    target=encoders_list[-1].executor,
                    args=(path, [element]),
                    daemon=True,
                )
            )
            threads_list[-1].start()
        elif isdir(tmp_path):
            directories.append(element)

    for directory in directories:
        directory = f"{path}/{directory}"
        duplicate_detector(directory)


# function to get dictionaries from all threads
def get_processed_files() -> dict[str, list[str]]:
    processed_files = {}
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
            ] += encoder_thread.thread_processed_files.get(t_hash_key, [])

    return processed_files


if __name__ == "__main__":
    root_path = input("Enter path to the root directory: ")
    try:
        print("Starting threads...")
        duplicate_detector(root_path)
        print("Done. Waiting for all threads to finish...")
        for thread in threads_list:
            thread.join()
        print("Done. Counting duplicate files...")
        processed_files = get_processed_files()
        for hash_key in processed_files.keys():
            if len(processed_files[hash_key]) > 1:
                print(
                    "#" * 100,
                    *processed_files[hash_key],
                    f"Total: {len(processed_files[hash_key])} duplicates\n",
                    sep="\n",
                )
    except RecursionError:
        print("Script can't process directories with nesting levels > 999.")
    except FileNotFoundError:
        print("Path isn't valid or the directory isn't readable.")
    except Exception as e:
        print(f"Unknown exception: {e}")
