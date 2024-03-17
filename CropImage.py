from AnnotationCorrection import Ui_MainWindow
import sys
import os
import glob
from PIL import Image , ImageDraw, ImageFont
import numpy as np
import cv2
import json
from collections import Counter

class MyMainWindow():
    def __init__(self, annotation_dir_path ):
        self.classes = ['cell','glass_cell','plastic','copper']
        self.Group_image_index = [0]*len(self.classes)
        self.annotationIndex = -1
        self.group_boxes = []  # List to store the created group boxes
        files = os.listdir(annotation_dir_path)
        self.imagesPath = [os.path.join(annotation_dir_path, file) for file in files if file.endswith('.PNG')]
        count = 0
        for imageFilePath in self.imagesPath:

            #with open(jsonFilePath.replace('json','txt'), 'w') as file:
                
            #read image
            image = Image.open(imageFilePath)

            # Zoom image
            #(800,500) to (4400,3400)
            annotationList = []
            left, upper, right, lower = 800,500,4400,3400
            croppedImage = self.CropImage(image, left, upper, right, lower)
            

            #croppedImage.save('test.jpg')

            newWidth, newHeight = right - left, lower - upper
            column, row = 3,2
            widthMargin = newWidth/((column -1)*20)
            heightMargin = newHeight/((row - 1)*20)
            
            for i in range(row):
                for j in range(column):
                    if j == 0:
                        subLeft = 0
                        subRight = (newWidth/column) * (j+1) + widthMargin   
                    elif j == column - 1:
                        subRight = newWidth
                        subLeft = (newWidth/column) * j - widthMargin
                    else:
                        subLeft = (newWidth/column) * j - widthMargin
                        subRight = (newWidth/column) * (j+1) + widthMargin   

                    if i == 0:
                        subUpper = 0
                        subLower = subRight - subLeft
                    elif i == row - 1:
                        subLower = newHeight
                        subUpper = newHeight - (subRight - subLeft)
                    else:
                        subUpper = newHeight/row * i - heightMargin
                        subLower = newHeight/row * (i+1) + heightMargin



                    subWidth, subHeight = subRight - subLeft, subLower - subUpper

                    subImage = croppedImage.crop((subLeft, subUpper, subRight, subLower))
                    
                    #draw = ImageDraw.Draw(subImage)

                    #dirpath
                    dirPath = os.path.dirname(imageFilePath)
                    fileName = os.path.basename(imageFilePath)

                    dirPath = os.path.join(dirPath,'outputSegV8')
                    self.CheckDirExist(dirPath)

                    dirPath = os.path.join(dirPath,'cropped')

                    self.CheckDirExist(dirPath)

                    imagePath = os.path.join(dirPath, fileName.replace('.PNG', f'_{i}_{j}.jpg'))

                    subImage.save(imagePath)

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
        with open(self.imagesPath[self.annotationIndex], 'w') as json_file:
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

    def read_display_txt(self):
        try:
            if self.index == 1:
                self.index = int(open(os.path.join(self.annotation_dir_path,f'page.txt'), "r").read())
        except:
            pass
        try:
            self.page_number.setText(f"{self.index}")
            f = open(os.path.join(self.annotation_dir_path,f'{self.index}.txt'), "r")
            self.textEdit_page_content.setPlainText(f.read())
        except Exception as ex:
            print(ex)
            txt_paths = glob.glob(os.path.join(self.annotation_dir_path,'*.*'))
            if self.index > len(txt_paths):
                self.page_number.setText(f"{self.index}/{len(txt_paths)} Done!")

    def next_and_save(self):
        
        self.find_labels_in_groupbox_and_delete()
        self.SaveAnnotationToJson()
        #self.removeChildren()

        #Load new ann
        self.annotationIndex += 1
        if len(self.imagesPath) <= self.annotationIndex:
            return
        self.FileNameTxt.setText(os.path.basename(self.imagesPath[self.annotationIndex]))
        self.currentAnnotation = self.ReadJson(self.imagesPath[self.annotationIndex])
        self.currentImage = self.ReadImage(self.imagesPath[self.annotationIndex].replace('json','PNG'))
        
        self.Group_image_index = [0]*len(self.classes)
        self.UploadImagesToUI()

convert = MyMainWindow(r'E:\yolov9\data\0315')