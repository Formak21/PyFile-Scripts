import os
import sys
import threading

# User-defined settings
RECURSION_LIMIT = 1000
LOGGING = False
SILENT = False
ENCODING = "utf-8"

# OS-provided settings
SEPARATOR = os.path.sep


def log(message, end="\n"):
    if LOGGING:
        pass
    if not SILENT:
        print(message, end=end, flush=True)


def get_files(d: str) -> list[str]:
    files = []
    try:
        for p in os.listdir(d):
            if os.path.isfile(d + SEPARATOR + p):
                files.append(d + SEPARATOR + p)
            elif os.path.isdir(d + SEPARATOR + p):
                for file in get_files(d + SEPARATOR + p):
                    files.append(file)
    except Exception as e:
        if isinstance(e, OSError) and str(e)[7:9] == "12":
            print(f"Not enough memory for {d}")
        else:
            print(f"Unknown exception while checking directory {d}: {str(e)}")
    return files


class QuickFinder:
    def __init__(self, path: str, query: str):
        self.result = False
        self.path = path
        self.query = query

    def check_query(self) -> bool:
        try:
            with open(self.path, "rt", encoding=ENCODING) as file:
                if self.query in file.read():
                    self.result = True
                    return True
        except UnicodeDecodeError:
            pass
        except Exception as e:
            print(
                f"Unknown exception while reading file {self.path}: {str(e)} {str(type(e))}"
            )
        return False


def check_files(files: list[str], query: str) -> list[str]:
    threads = []
    result = []
    log("- Creating threads...", end="\t")
    for file in files:
        qf = QuickFinder(file, query)
        t = threading.Thread(target=qf.check_query, daemon=True)
        t.start()
        threads.append((qf, t))
    log("Done.")
    log("- Waiting for threads to finish...", end="\t")
    for thread in threads:
        thread[1].join()
        if thread[0].result:
            result.append(thread[0].path)
    log("Done.")
    return result


def search(path: str, query: str) -> list[str]:
    log(f'Getting all files recursively from "{path}"...')
    files = get_files(path)
    log(f"Done. Found {len(files)} files...")
    log(f'Looking for "{query}":')
    results = check_files(files, query)
    log(f"Done. Found {len(results)} results.", end="\n\n")
    return results


if __name__ == "__main__":
    sys.setrecursionlimit(RECURSION_LIMIT)
    if len(sys.argv) > 2:
        path = sys.argv[1]
        query = sys.argv[2]
    else:
        path = input("Path: ")
        query = input("Query: ")

    # Issue #4 workaround(https://github.com/Formak21/PyFile-Scripts/issues/4)
    if "~" in path:
        path = os.path.expanduser(path)

    r = search(path, query)
    print(*r, f"\nTotal: {len(r)}", sep="\n")
