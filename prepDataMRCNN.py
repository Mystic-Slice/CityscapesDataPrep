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
for jsonFile in JSON_FILES_GLOB:
    path = jsonFile.split("\\")
    path[0] = "Json_files"
    outPath = "\\".join(path)
    try:
        os.makedirs("\\".join(path[:-1]))
    except:
        pass
    shutil.copy(jsonFile, outPath)

# Rename leftImg8bit --> remove "leftImg8bit" part from filename
print("--> Renaming images")
IMAGE_FILES_GLOB = glob.glob("leftImg8bit\\*\\*\\*.png")
for imageFile in IMAGE_FILES_GLOB:
    path = imageFile.split("\\")
    if "leftImg8bit" in path[-1]:
        path[-1] = "_".join(path[-1].split("_")[:-1]) + ".png"
        os.rename(imageFile, "\\".join(path))

# Generate masks
print("--> Generating masks")
CITYSCAPES_SCRIPTS_PATH = "cityscapesscripts\\preparation"
for folder in SUB_FOLDERS:
    MASK_FOLDER = f"..\\..\\masks\\{folder}"
    JSON_FOLDER = f"Json_files\\{folder}\\*"
    for city in glob.glob(JSON_FOLDER):
        os.chdir(CITYSCAPES_SCRIPTS_PATH)
        os.system(f"python json2labelImg.py {MASK_FOLDER} ..\\..\\{city}")
        os.chdir("..\\..\\")

# Rename masks folders
print("--> Renaming masks folders")
for fileName in glob.glob("masks\\*\\*"):
    imgName = fileName.split("\\")[-1].split(".")[0]
    folder = fileName.split("\\")[-2]
    try:
        os.rename(fileName, f"masks\\{folder}\\{imgName.split('_gtFine_polygons')[0]}")
    except:
        print("Failed for ", fileName)

# Move images our of city directory
print("--> Moving images out of city directory")
CITY_FOLDER_SET = set([])
for fileName in glob.glob("leftImg8bit\\*\\*\\*.png"):
    outPath = fileName.split("\\")
    CITY_FOLDER_SET.add(outPath.pop(-2))
    outPath = "\\".join(outPath)
    shutil.move(fileName, outPath)

for city in CITY_FOLDER_SET:
    for folderName in glob.glob(f"leftImg8bit\\*\\{city}"):
        os.rmdir(folderName)

# Remove empty masks folders
for folder in glob.glob("masks\\*\\*"):
    try:
        os.rmdir(folder)
        print("Deleting ", folder)
    except:
        pass

# Remove images without masks
print("--> Removing images without masks")
for fileName in glob.glob("leftImg8bit\\*\\*.png"):
    imgName = fileName.split("\\")[-1].split(".")[0]
    folder = fileName.split("\\")[-2]
    try:
        os.listdir(f"masks\\{folder}\\{imgName}")
    except:
        print("Deleting ", fileName)
        os.remove(fileName)
