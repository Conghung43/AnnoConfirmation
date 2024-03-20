from AnnotationCorrection import Ui_MainWindow
import sys
import os
import glob
from PIL import Image , ImageDraw, ImageFont
import numpy as np
import cv2
import json
from collections import Counter
import shutil

class MyMainWindow():
    def __init__(self, annotation_dir_path ):
        self.classes = ['cell','glass_cell','plastic','copper']
        self.Group_image_index = [0]*len(self.classes)
        self.annotationIndex = -1
        self.group_boxes = []  # List to store the created group boxes
        files = os.listdir(annotation_dir_path)
        self.json_files = [os.path.join(annotation_dir_path, file) for file in files if file.endswith('.json')]
        count = 0
        for jsonFilePath in self.json_files:
            #dirpath
            dirPath = os.path.dirname(jsonFilePath)
            fileName = os.path.basename(jsonFilePath)

            dirPath = os.path.join(dirPath,'outputSegV8')
            self.CheckDirExist(dirPath)

            if count %3 == 0:
                dirPath = os.path.join(dirPath,'test')
            elif count %4 ==0:
                dirPath = os.path.join(dirPath,'valid')
            else:
                dirPath = os.path.join(dirPath,'train')

            self.CheckDirExist(dirPath)

            textDir = os.path.join (dirPath, 'labels')
            imageDir = os.path.join (dirPath, 'images')

            self.CheckDirExist(textDir)
            self.CheckDirExist(imageDir)

            txtPath = os.path.join(textDir, fileName.replace('.json',f'auto.txt'))
            imagePath = os.path.join(imageDir, fileName.replace('.json',f'auto.jpg'))

            with open(txtPath, 'w') as file:
                annotationList = []
                currentAnnotation = self.ReadJson(jsonFilePath)
                for index in range(len(currentAnnotation['shapes'])):
                    label,bbox, _ = self.GetAnnotation(currentAnnotation['shapes'][index])
                    bbox = np.array(bbox)
                    annotationList.append((label, bbox))

                original_width, original_height = currentAnnotation['imageWidth'], currentAnnotation['imageHeight']

                for ann in annotationList:
                    ann = list(ann)
                    bbox = ann[1]
                    
                    bbox = bbox/np.array([original_width,original_height])
                    contentPrepared = f'{self.classes.index(ann[0])}'
                    for index in range(len(bbox)):
                        contentPrepared += f' {bbox[index][0]} {bbox[index][1]}'
                        if index == len(bbox) -1:
                            contentPrepared += '\n'
                    file.write(contentPrepared)

                    #draw.rectangle(ann[1:], outline="red")

            shutil.move(jsonFilePath.replace('.json','.jpg'), imagePath)

            count += 1



                # for index in range(len(currentAnnotation['shapes'])):
                #     label,bbox, _ = self.GetAnnotation(currentAnnotation['shapes'][index])
                #     contentPrepared = f'{self.classes.index(label)} {((bbox[2]+bbox[0])/2)/original_width} {((bbox[3]+bbox[1])/2)/original_height} {(bbox[2]-bbox[0])/original_width} {(bbox[3]-bbox[1])/original_height}'
                #     if index < len(currentAnnotation['shapes']):
                #         contentPrepared += '\n'
                #     file.write(contentPrepared)

    def CheckDirExist(self, path):
        if not os.path.exists(path):
            os.makedirs(path)

    def CropImage(self, image, centerPoint, size):
        # Define the crop region (left, upper, right, lower)
        crop_region = (centerPoint[0] - size[0]/2, centerPoint[1] - size[1]/2, centerPoint[0] + size[0]/2, centerPoint[1] + size[1]/2)
        croppedImage = image.crop(crop_region)
        return croppedImage
    
    def CropImage(self, image, left, upper, right, lower):
        # Define the crop region (left, upper, right, lower)
        crop_region = (left, upper, right, lower)
        croppedImage = image.crop(crop_region)
        return croppedImage
    
    def ModifyAnnotation(self, ann, left, upper, right, lower):
        # Define the crop region (left, upper, right, lower)
        crop_region = (left, upper, right, lower)
        croppedImage = image.crop(crop_region)
        return croppedImage

    def SaveAnnotationToJson(self):
        #Create backup_file

        #Save/overwrite file
        with open(self.json_files[self.annotationIndex], 'w') as json_file:
            json.dump(self.currentAnnotation, json_file)
     
    def GetAnnotation(self, anno):
        element_dict = anno
        label = element_dict['label']
        bbox = element_dict['points']
        return label,bbox,element_dict


    # def ReadAnnotation(self, jsonFilePath):
    #     self.
    #     self.currentImage = self.ReadImage(jsonFilePath.replace('json','PNG'))
    
    def ReadImage(self, imagePath):
        if os.path.exists(imagePath):
            return cv2.imread(imagePath)
        else:
            return None

    def ReadJson(self, file_path):
        # Open the JSON file
        with open(file_path, 'r') as file:
            # Load the JSON data
            data = json.load(file)
            for inx in range(len(data['shapes'])):
                polypoints = np.array(data['shapes'][inx]['points'])
                topLeft = (np.min(polypoints[:,0]), np.min(polypoints[:,1]))
                rightBottom = (np.max(polypoints[:,0]), np.max(polypoints[:,1]))
                data['shapes'][inx]['description'] = f'{int(topLeft[0])},{int(topLeft[1])},{int(rightBottom[0])},{int(rightBottom[1])}'
        return data

        # Now you can work with the 'data' object, which contains the contents of the JSON file

convert = MyMainWindow(r'E:\yolov9\data\Epoch200 - modified V2 (0318)')