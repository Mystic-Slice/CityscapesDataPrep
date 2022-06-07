import sys
import os 
import glob

def main(args):
    MASKS_DIR = args[0]
    JSON_DIR = args[1]
    JSON_FILES = glob.glob(f"{JSON_DIR}\\*.json")
    counter = 0
    for jsonFile in JSON_FILES:
        inJson = jsonFile
        os.system(f"python json2instanceImg.py {jsonFile} {MASKS_DIR}")
        print()

    

if __name__ == "__main__":
    main(sys.argv[1:])