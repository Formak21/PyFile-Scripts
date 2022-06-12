from hashlib import sha256
import threading

CHUNK = 100 * 1024**2  # 10MB
PATHS = [
    "/Users/german/Downloads/English_File_3d_Advanced_Class_Cds.zip",
    "/Users/german/Downloads/M.NETFramework.exe",
    "/Users/german/Downloads/googlechromecanary.dmg",
    "/Applications/Xcode.app/Contents/PkgInfo",
    "/Applications/Xcode.app/Contents/version.plist",
    "/Applications/Xcode.app/Contents/Info.plist",
]


class Encoder:
    def __init__(self):
        self.result = None

    def encode(self, path: str) -> None:
        encoder = sha256()
        with open(file=path, mode="rb") as file:
            chunk = 0
            while chunk != b"":
                chunk = file.read(CHUNK)
                encoder.update(chunk)
        self.result = encoder.hexdigest()


threads = []
encoders = []
for path in PATHS:
    encoders.append(Encoder())
    t = threading.Thread(target=encoders[-1].encode, args=(path,), daemon=True)
    threads.append(t)
    t.start()

for t in range(len(encoders)):
    threads[t].join()
    print(encoders[t].result)
