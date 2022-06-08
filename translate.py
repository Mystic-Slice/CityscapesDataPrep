def trainId(idx):
    return idx - 23

import os, glob

MASK_FILES = glob.glob("masks\\*\\*\\*.png")

for file in MASK_FILES:
    x = file.split("\\")
    fileName = x[-1]
    idx, rest = fileName.split("_")
    idx = trainId(int(idx))
    fileName = str(idx%10) + "_" + rest
    x.pop()
    x.append(fileName)
    outpath = "\\".join(x)
    os.rename(file, outpath)
