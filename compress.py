
import os
import os.path

def prepareGamePaths(mainDirPath):
    global BEAMNG_CONTENT_PATH
    BEAMNG_CONTENT_PATH = os.path.join(mainDirPath, "content")

    global BEAMNG_LEVELS_PATH
    BEAMNG_LEVELS_PATH = os.path.join(BEAMNG_CONTENT_PATH, "levels")
    global BEAMNG_VEHICLES_PATH
    BEAMNG_VEHICLES_PATH = os.path.join(BEAMNG_CONTENT_PATH, "vehicles")

def validateDirectory(targetDir):
    if not os.path.isdir(targetDir):
        raise NotADirectoryError("The specified path must point to a directory")
    else:
        return True

import errno

def checkAvailableSpace(targetDir, freeSpaceThreshold):
    validateDirectory(targetDir)

    diskFreeSpace = shutil.disk_usage(targetDir)["free"]

    if diskFreeSpace < freeSpaceThreshold:
        raise OSError(os.strerror(errno.ENOSPC))
    else:
        return True

import shutil
import zipfile

import tqdm

def compress(folderPath):
    os.chdir(folderPath)

    folderContents = list()

    for filename in sorted(os.listdir(os.getcwd())):
        if filename.endswith(".zip"):
            folderContents.append(filename)
    
    for filename in (pbar:=tqdm.tqdm(folderContents)):
        pbar.set_postfix_str(filename)

        with zipfile.ZipFile(filename, mode="r") as zipFile:
            zipFile.extractall(filename[:-4])

        os.remove(filename)

        with zipfile.ZipFile(filename, mode="w", compression=zipfile.ZIP_DEFLATED, compresslevel=9) as zipFile:
            for root, subdirs, files in os.walk(filename[:-4]):
                for nextFile in files:
                    zipFile.write(os.path.join(root, nextFile))

        shutil.rmtree(filename[:-4])

if __name__ == "__main__":
    pass

