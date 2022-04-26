import cv2
import numpy as np
import glob
import os
from pathlib import Path
from dateutil.parser import parse

# https://stackoverflow.com/questions/49511342/python-move-a-file-up-one-directory

# from fastai.learner import load_learner


def is_date(string, fuzzy=False):
    """
    Return whether the string can be interpreted as a date.

    :param string: str, string to check for date
    :param fuzzy: bool, ignore unknown tokens in string if True

    Taken from: https://stackoverflow.com/questions/25341945/check-if-string-has-date-any-format#25341965
    """
    try: 
        parse(string, fuzzy=fuzzy)
        return True

    except ValueError:
        return False

def moveup_and_rename(p, moveTwo=False):
    """ Appends parent dir to filename and moves it up a dir """
    if moveTwo:
        parent_dir = p.parents[2]                   
        newName = p.parents[1].name + ' ' + p.parents[0].name + ' ' + p.name
        p.rename(parent_dir / newName)
    else:
        parent_dir = p.parents[1]
        newName = p.parents[0].name + ' ' + p.name
        p.rename(parent_dir / newName)
    return

if __name__ == "__main__":
    # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    cwd = os.getcwd()
    imgs_path = os.path.join(cwd, "Sample Pollen Data", "**", "*")
    imgs_list = []
    dirs_to_delete = []
    for file in glob.glob(imgs_path, recursive=True):
        p = Path(file).absolute()
        # Check if dir and is Date or Old
        print(p.name)
        if os.path.isdir(file):
            if is_date(p.name) or p.name == "Old":
                dirs_to_delete.append(file)
            continue
        # Delete DS_STORE
        if file.endswith('.DS_Store'):
            os.remove(file)
            print("Deleted:\t", file)
            continue
        # Handles date/Old/*.JPG
        if p.parents[0].name == "Old" and is_date(p.parents[1].name):
            if ".JPG" in file:
                imgs_list.append(file)
                moveup_and_rename(p, moveTwo=True)
                continue
        # Handles /Old/*.JPG and /Date/*.JPG
        if p.parents[0].name == "Old" or is_date(p.parents[0].name):
            if file.endswith('.JPG'):
                imgs_list.append(file)
                moveup_and_rename(p)
                # if "10X" in file:
                #     print(file)


    print("Num Images:", len(imgs_list))
    print()
    for dir in dirs_to_delete:
        print(dir)

    # scan = os.scandir(os.path.join(cwd, "Sample Pollen Data"))
    # for file in scan:
    #     print(file.name)
    