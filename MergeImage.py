from AnnotationCorrection import Ui_MainWindow
import sys
import os
import glob
from PIL import Image , ImageDraw, ImageFont
import numpy as np
import cv2
import json
from collections import Counter
from shapely.geometry import Polygon
from shapely.ops import unary_union
import geopandas as gpd

class MyMainWindow():
    def __init__(self, annotation_dir_path ):
        self.classes = ['cell','glass_cell','plastic','copper']
        self.Group_image_index = [0]*len(self.classes)
        self.annotationIndex = -1
        self.group_boxes = []  # List to store the created group boxes
        left, upper, right, lower = 800,500,4400,3400
        mainImageWidth = right - left
        mainImageHeight = lower - upper
        files = os.listdir(annotation_dir_path)
        self.text_files = [os.path.join(annotation_dir_path, file) for file in files if file.endswith('.txt')]
        count = 0
        for txtPath in self.text_files:
            row, column = int(txtPath[-7]), int(txtPath[-5])

            text_main_path =  txtPath[:-8] + '.txt'
            image_path = txtPath.replace('.txt', '.jpg')
            image = cv2.imread(image_path)
            width, height = image.shape[1],image.shape[0]

            if row ==0:
                subUpper = 0
            else:
                subUpper = mainImageHeight - height

            if column == 0:
                subLeft = 0
            elif column == 1:
                subLeft = int(mainImageWidth/2) - int(width/2)
            else:
                subLeft = mainImageWidth - width

            tempDict = {}
            if os.path.exists(text_main_path):
                mainFile = open(text_main_path, "r")
                mainLines = mainFile.readlines()
                for line in mainLines:
                    lineSplit = line.replace("\n","").split(" ")
                    arr = np.array(lineSplit[1:], dtype = float).reshape(-1, 2)
                    if len(arr) == 0: continue
                    if line[0] in tempDict:
                        tempDict[line[0]].append(arr)
                    else:
                        tempDict[line[0]] = [arr]

                mainFile.close()

            with open(text_main_path, "a") as mainFile:

                with open(txtPath, "r") as file:
                    # Read all lines from the file into a list

                    lines = file.readlines()

                    for line in lines:
                        mergeFlag = False
                        lineSplit = line.replace("\n","").split(" ")
                        arr = np.array(lineSplit[1:], dtype = float).reshape(-1, 2)*np.array([width, height])
                        if len(arr) == 0: continue
                        arr = (arr + np.array([subLeft,subUpper]) + np.array([left,upper]))/np.array([5488,3672])

                        if line[0] in tempDict:
                            values = tempDict[line[0]]
                            for index in range(len(tempDict[line[0]])):
                                merge_result = None
                                merge_result = self.merge_overlapping_polygons(arr, values[index])
                                if merge_result is not None:
                                    values[index] = merge_result
                                    mergeFlag = True
                                    break
                            if not mergeFlag:
                                tempDict[line[0]].append(arr)
                        else:
                            tempDict[line[0]] = [arr]
    
                for key, values in tempDict.items():
                    for arr in values:
                        contentPrepared = key
                        for index in range(len(arr)):
                            contentPrepared += f' {arr[index][0]} {arr[index][1]}'
                            if index == len(arr) -1:
                                contentPrepared += '\n'
                        mainFile.write(contentPrepared)
                    


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
        with open(self.text_files[self.annotationIndex], 'w') as json_file:
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



    def merge_overlapping_polygons(self, pl1, pl2):
        # Create Shapely Polygon objects from the lists of points
        polygon1 = Polygon(pl1)
        polygon2 = Polygon(pl2)
        
        gdf = gpd.GeoDataFrame(geometry=[polygon1, polygon2])

        # Merge overlapping polygons
        merge_polygon = unary_union(gdf.geometry)

        # Check if the two polygons intersect
        if "Multi" not in merge_polygon.geom_type:
            # # If they intersect, perform a union operation to merge them
            # merged_polygon = polygon1.union(polygon2)
            # # Extract the coordinates of the merged polygon
            # merged_coords = list(merged_polygon.exterior.coords)
            # # Remove the last coordinate, which is a duplicate of the first one
            # merged_coords.pop()
            # print('merged')
            return list(merge_polygon.exterior.coords)
        else:
            # If they don't intersect, return None
            return None


convert = MyMainWindow(r'E:\yolov9\data\0218\outputSegV8\YoloV8OutputWithModel300_0317') 