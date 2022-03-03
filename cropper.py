import shutil
import sys

import numpy as np
import io
from PIL import Image, ImageFile
import os
import cv2
import mediapipe as mp

MARKER = False


def crop(name, source_folder_name, destination_folder_name):
    print(f"Processing {name}")
    input_path = f"{source_folder_name}/{name}"
    output_path = f"{destination_folder_name}/{name}"
    face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')
    img = cv2.imread(input_path)
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(gray, 1.3, 5)
    it = iter(faces)
    x, y, w, h = next(it)
    center = (x + int(w / 2), y + int(h / 2))

    modified_width_ratio = 1.5
    modified_width = int(w * modified_width_ratio)
    width_height_ratio = 1.2
    modified_height = int(modified_width * width_height_ratio)

    modified_top_left = (center[0] - int(modified_width / 2), center[1] - int(modified_height / 2))
    if modified_top_left[0] < 0:
        modified_top_left = (0, modified_top_left[1])
    if modified_top_left[1] < 0:
        modified_top_left = (modified_top_left[0], 0)

    modified_bottom_right = (modified_top_left[0] + modified_width, modified_top_left[1] + modified_height)

    if MARKER:
        cv2.rectangle(img, (modified_top_left), (modified_bottom_right), color=(255, 0, 255))
        cv2.circle(img, center, radius=2, color=(255, 0, 255), thickness=5)
        cv2.imwrite(destination_folder_name, img)
        exit(0)

    cropped_image = img[modified_top_left[1]:modified_bottom_right[1], modified_top_left[0]:modified_bottom_right[0]]
    # cropped_image = remove_bg(cropped_image, R, G, B)
    cv2.imwrite(output_path, cropped_image)


def crop_all(sourceFolderName, destinationFolderName):
    directory = sourceFolderName
    for file in os.listdir(directory):
        print(f"Processing {file}")
        try:
            crop(file, sourceFolderName, destinationFolderName)
        except:
            shutil.copy2(f"{sourceFolderName}/{file}", f"{destinationFolderName}/{file}")
            print(f"Could not process image {file}", file=sourceFile)
            sourceFile.close()


if __name__ == "__main__":
    print(sys.argv[0])
    sourceFile = open('error.txt', 'w')
    if not os.path.isdir("temp"):
        os.mkdir("temp")

    sourceFolderName = "raw"
    destinationFolderName = "temp"
    crop_all(sourceFolderName, destinationFolderName)
    sys.exit()
