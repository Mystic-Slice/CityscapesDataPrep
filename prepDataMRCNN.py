# Needs leftImg8bit, masks, and scripts folder
# Modify the json2labelImg.py script to accept cmd line args

import os
import glob
import shutil

# Build the file structure
print("--> Building file structure")
FOLDERS = ["masks", "Json_files"]
SUB_FOLDERS = ["test", "train", "val"]

for folder in FOLDERS:
    for subFolder in SUB_FOLDERS:
        try:
            os.makedirs(os.path.join("./", folder, subFolder))
        except:
            # Folder already present
            pass

# Copy jsons
print("--> Copying Jsons")
JSON_FILES_GLOB = glob.glob("gtFine\\*\\*\\*.json")
count = 0
for jsonFile in JSON_FILES_GLOB:
    path = jsonFile.split("\\")
    path[0] = "Json_files"
    outPath = "\\".join(path)
    try:
        os.makedirs("\\".join(path[:-1]))
    except:
        pass
    shutil.copy(jsonFile, outPath)
    print(f"\r {count}/{len(JSON_FILES_GLOB)}", end="")
    count += 1
print()

# Rename leftImg8bit --> remove "leftImg8bit" part from filename
print("--> Renaming images")
IMAGE_FILES_GLOB = glob.glob("leftImg8bit\\*\\*\\*.png")
count = 0
for imageFile in IMAGE_FILES_GLOB:
    path = imageFile.split("\\")
    if "leftImg8bit" in path[-1]:
        path[-1] = "_".join(path[-1].split("_")[:-1]) + ".png"
        os.rename(imageFile, "\\".join(path))
    print(f"\r {count}/{len(IMAGE_FILES_GLOB)}", end="")
    count += 1
print()

# Generate masks
print("--> Generating masks")
CITYSCAPES_SCRIPTS_PATH = "cityscapesscripts\\preparation"
count = 0
for folder in SUB_FOLDERS:
    MASK_FOLDER = f"..\\..\\masks\\{folder}"
    JSON_FOLDER = f"Json_files\\{folder}\\*"
    for city in glob.glob(JSON_FOLDER):
        os.chdir(CITYSCAPES_SCRIPTS_PATH)
        os.system(f"python createInstanceMasks.py {MASK_FOLDER} ..\\..\\{city}")
        os.chdir("..\\..\\")
    print(f"\r {count}/{len(SUB_FOLDERS)}", end="")
    count += 1
print()

# Rename masks folders
print("--> Renaming masks folders")
count = 0
MASKS_PATH = glob.glob("masks\\*\\*")
for fileName in MASKS_PATH:
    imgName = fileName.split("\\")[-1].split(".")[0]
    folder = fileName.split("\\")[-2]
    try:
        os.rename(fileName, f"masks\\{folder}\\{imgName.split('_gtFine_polygons')[0]}")
    except:
        print("Failed for ", fileName)
    print(f"\r {count}/{len(MASKS_PATH)}", end="")
    count += 1
print()

# Move images our of city directory
print("--> Moving images out of city directory")
CITY_FOLDER_SET = set([])
IMAGES_PATH = glob.glob("leftImg8bit\\*\\*\\*.png")
count = 0
for fileName in IMAGES_PATH:
    outPath = fileName.split("\\")
    CITY_FOLDER_SET.add(outPath.pop(-2))
    outPath = "\\".join(outPath)
    shutil.move(fileName, outPath)
    print(f"\r {count}/{len(IMAGES_PATH)}", end="")
    count += 1
print()

count = 0
for city in CITY_FOLDER_SET:
    for folderName in glob.glob(f"leftImg8bit\\*\\{city}"):
        os.rmdir(folderName)
    print(f"\r {count}/{len(CITY_FOLDER_SET)}", end="")
    count += 1
print()

# Remove empty masks folders
MASKS_PATH = glob.glob("masks\\*\\*")
count = 0
for folder in MASKS_PATH:
    try:
        os.rmdir(folder)
        print("Deleting ", folder)
    except:
        pass
    print(f"\r {count}/{len(MASKS_PATH)}", end="")
    count += 1
print()

# Remove images without masks
print("--> Removing images without masks")
IMAGES_PATH = glob.glob("leftImg8bit\\*\\*.png")
count = 0
for fileName in IMAGES_PATH:
    imgName = fileName.split("\\")[-1].split(".")[0]
    folder = fileName.split("\\")[-2]
    try:
        os.listdir(f"masks\\{folder}\\{imgName}")
    except:
        print("Deleting ", fileName)
        os.remove(fileName)
    print(f"\r {count}/{len(IMAGES_PATH)}", end="")
    count += 1
print()
