import os, glob

EMPTY_FILES = glob.glob("masks\\*\\*\\0*.png")

for file in EMPTY_FILES:
    os.remove(file)
