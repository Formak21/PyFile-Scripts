#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This script finds duplicate files by comparing their hashes.
For more info, see README.md.

License: MIT
"""

import sys
import threading
from hashlib import sha1
from os import listdir
from os.path import isdir, isfile

HASH_FUNCTION = sha1
CHUNK_SIZE = 100 * 1024**2  # 100MiB


class EncoderThread:
    def __init__(self):
        # variable, that is needed to save founded by thread files
        # hash:[filepath1, filepath2, ...]
        self.thread_processed_files = dict()

    @staticmethod
    def sha_encoder(filepath: str) -> str:
        """Function to encode files with HASH_FUNCTION."""
        try:
            encoder = HASH_FUNCTION()
            with open(file=filepath, mode="rb") as file:
                chunk = 0
                while chunk != b"":
                    chunk = file.read(CHUNK_SIZE)
                    encoder.update(chunk)
            return encoder.hexdigest()
        except Exception as ex:
            print("Unknown exception: ", ex)
            return "An error occured while trying to encode this file"

    def executor(self, files_path: str, unprocessed_files: list[str]) -> None:
        """Function to calculate hashes and save them in dictionary."""
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
    """This function finds all duplicates in specified directory recursively."""
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


def get_processed_files() -> dict[str, list[str]]:
    """Function to get dictionaries from all threads."""
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
    if len(sys.argv) > 1:
        root_path = sys.argv[1]
    else:
        root_path = input("Enter path to the root directory: ")
    try:
        print("Starting threads...")
        duplicate_detector(root_path)
        print("Done. Waiting for all threads to finish...")
        for thread in threads_list:
            thread.join()
        print("Done. Counting duplicate files...")
        processed_files = get_processed_files()
        for hash_key, files in processed_files.items():
            if len(files) > 1:
                print(
                    "#" * 100,
                    *files,
                    f"Total: {len(files)} duplicates\n",
                    sep="\n",
                )
    except RecursionError:
        print("Script can't process directories with nesting levels > 999.")
    except FileNotFoundError:
        print("Path isn't valid or the directory isn't readable.")
    except Exception as e:
        print(f"Unknown exception: {e}")
