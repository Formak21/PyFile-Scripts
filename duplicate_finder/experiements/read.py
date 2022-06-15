from hashlib import sha256

PATHS = [
    "/Users/german/Downloads/English_File_3d_Advanced_Class_Cds.zip",
    "/Users/german/Downloads/M.NETFramework.exe",
    "/Users/german/Downloads/googlechromecanary.dmg",
    "/Applications/Xcode.app/Contents/PkgInfo",
    "/Applications/Xcode.app/Contents/version.plist",
    "/Applications/Xcode.app/Contents/Info.plist",
]

for path in PATHS:
    encoder = sha256()
    with open(file=path, mode="rb") as file:
        encoder.update(file.read())
    print(encoder.hexdigest())
