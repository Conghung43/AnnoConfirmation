# from IPython import display
# display.clear_output()

# import ultralytics
# ultralytics.checks()

from ultralytics import YOLO
import os
#from IPython.display import display, Image
import numpy as np
from PIL import Image
import shutil


def get_image_paths(directory):
    image_paths = []
    # Traverse through the directory and its subdirectories
    directories = [os.path.join(directory, d) for d in os.listdir(directory) if os.path.isdir(os.path.join(directory, d))]
    for mainFolder in directories:
        subFolders = directories = [os.path.join(mainFolder, d) for d in os.listdir(mainFolder) if os.path.isdir(os.path.join(mainFolder, d))]
        for folder in subFolders:
            image_path = GetImageFromFolder(folder)
            if len(image_path) == 0:
                continue
            image_paths.extend(image_path)
    return image_paths

def GetImageFromFolder(directory):
    files = os.listdir(directory)
    images_files_path = [os.path.join(directory, file) for file in files if file.endswith(('.png', '.jpg', '.jpeg', '.gif', '.bmp'))]
    return images_files_path



#imagesPath = get_image_paths(r"E:\yolov9\data\0218\outputSegV8")

directory = r"E:\yolov9\data\0218\outputSegV8 - Copy"
exportFolderName = 'YoloV8Output'
exportFolderPath = os.path.join(directory,exportFolderName)
if not os.path.exists(exportFolderPath):
    os.makedirs(exportFolderPath)
image_paths = get_image_paths(directory)
model = YOLO(r'C:\Users\kai\Downloads\best.pt')

for imagePath in image_paths:
    print(imagePath)
    # write image and annotation
    newTxtName = os.path.basename( imagePath.replace('.jpg','.txt'))
    newImageName = os.path.basename(imagePath)

    if os.path.exists( newImageName):
        continue
    results = model.predict(source=imagePath, conf=0.25, save=True)

    if results[0].masks is None:
        continue

    masks = results[0].masks.xy
    cls = results[0].boxes.cls.numpy()
    #image = Image.open(imagePath)
    subWidth,subHeight = results[0].orig_shape

    newTxtPath = os.path.join(exportFolderPath,newTxtName)
    newImagePath = os.path.join(exportFolderPath,newImageName)

    with open(newTxtPath, 'w') as file:
        for idx, ann in enumerate( masks):
            ann = ann/np.array([subWidth,subHeight])
            contentPrepared = f'{int(cls[idx])}'
            for index in range(len(ann)):
                contentPrepared += f' {ann[index][0]} {ann[index][1]}'
                if index == len(ann) -1:
                    contentPrepared += '\n'
            file.write(contentPrepared)

                #draw.rectangle(ann[1:], outline="red")
    shutil.copy(imagePath, newImagePath)

print(results[0].masks.xy)