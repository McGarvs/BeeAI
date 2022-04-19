import cv2
import numpy as np
import glob
import os
import fnmatch
# from fastai.learner import load_learner
def read_imgs(imgs):
    print("Length", len(imgs))
    return "AAAAAHHHH"

if __name__ == "__main__":
    # https://stackoverflow.com/questions/2186525/how-to-use-glob-to-find-files-recursively
    counter = 0
    cwd = os.getcwd()
    imgs_path = os.path.join(cwd, "Sample Pollen Data", "**", "*.JPG")
    imgs_list = []
    for file in glob.glob(imgs_path, recursive=True):
        if "10X" in file:
            print(file)
        # if counter < 20:
        #     print(file)
        #     counter += 1
            imgs_list.append(file) 
    read_imgs(imgs_list)