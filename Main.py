# Tim kiem danh sach tu moi va trang tu du lieu OCR.
# Buoc nay co the thay the bang thu cong
# Nguoi nhap se dung excel , xong do se dung chuong trinh de chuyen 
#excel thanh list tu moi va trang sach
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *
from AnnotationCorrection import Ui_MainWindow
import sys
import os
import glob
from PIL import Image
import numpy as np
import cv2
import json
from collections import Counter

class ClickableLabel(QLabel):
    def __init__(self, text, parent=None):
        super().__init__(text, parent)
        self.mousePressEvent = self.on_click

    def on_click(self, event):
        print(f"Clicked: {self.objectName()}")
        self.setVisible(False)



class ImageGroupBox(QWidget):
    def __init__(self, image_paths):
        super().__init__()
        self.initUI(image_paths)
    
    def initUI(self, image_paths):
        layout = QVBoxLayout()
        for path in image_paths:
            pixmap = QPixmap(path)
            label = QLabel()
            label.setPixmap(pixmap)
            layout.addWidget(label)
        
        self.setLayout(layout)

class MyMainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyMainWindow, self).__init__(parent)
        self.setupUi(self)
        self.classes = ['cell','glass_cell','plastic','copper']
        self.Group_image_index = [0]*len(self.classes)
        self.annotationIndex = -1
        self.group_boxes = []  # List to store the created group boxes
        # self.images_path = "/Users/hungnguyencong/Downloads/hung.PNG"
        # image = cv2.imread(self.images_path)
        # self.images_path_lbl.setText("Desktop/book_images")
        # self.db_directory = '/Users/hungnguyencong/Desktop/DU AN CUA HUNG/PYTHON_CODE/django_flashcard'
        self.LoadFolderBtn.clicked.connect(self.open_input_folder_dialog)
        self.CreateGroupBox(len(self.classes))

        # for i in range(numberOfImage):
        #     self.SetImageToGroup(image, 1, i,self.numberOfColumn)
        # self.convert.clicked.connect(self.run_images2txts)
        # self.show_txt_btn.clicked.connect(self.read_display_txt)
        self.NextFileBtn.clicked.connect(self.next_and_save)
        # self.back_btn.clicked.connect(self.back_function)
        # self.save_btn.clicked.connect(self.save_data_to_verify_tabele)
        # self.back_btn.clicked.connect(self.back_vocabulary)
        # self.next_btn.clicked.connect(self.next_vocabulary)
        # self.image_search.clicked.connect(self.click_search_image)
        # self.combobox_db.currentIndexChanged.connect(self.db_choosen)
        # self.combobox_filter_level.currentIndexChanged.connect(self.filter_level_choosen)
        # self.images_display.mousePressEvent = self.getPos
        # self.manual_confirm_checkbox.stateChanged.connect(self.db_choosen)
        # self.open_input_folder_dialog()

    def changeEvent(self, event):
        if event.type() == event.WindowStateChange:
            if self.windowState() & Qt.WindowMaximized:
                print("Window Maximized")
            elif self.windowState() & Qt.WindowMinimized:
                print("Window Minimized")

    
    def CreateGroupBox(self,numberOfClass):
        buffer = self.size().width()/((numberOfClass+1)*2*numberOfClass )
        class_size = self.size().width()/(numberOfClass+1)
        heightWidthGroupBoxRatio = self.size().height()//class_size
        self.GroupBoxArea = heightWidthGroupBoxRatio*class_size*class_size
        for idx in range(numberOfClass):
            group_box = QGroupBox(self)#(f'Group {idx+1}')  # Create QGroupBox with a title
            group_box.setGeometry(QRect(buffer +idx*(class_size + 2*buffer), 50, class_size, self.size().height()))
            self.group_boxes.append(group_box)  # Append the created group box to the list

    def SetImageToGroup(self, image, group_index, image_index, numberOfColumn, element_dict):
        row = image_index//numberOfColumn
        column = image_index%numberOfColumn
        element_dict['position'] = f'{group_index}_{row}_{column}'
        imageLabel = ClickableLabel(element_dict['position'],self.group_boxes[group_index])
        imageLabel.setGeometry(QRect((image_index%numberOfColumn)*self.imageLabelEdgeSize, (image_index//numberOfColumn)*self.imageLabelEdgeSize, self.imageLabelEdgeSize, self.imageLabelEdgeSize))
        imageLabel.setStyleSheet("background-color: rgb(251, 255, 230);")
        imageLabel.setObjectName(element_dict['position'])
        image = self.ConvertToQpixmap(image,imageLabel)
        imageLabel.setPixmap(image)
        imageLabel.show()
        # image.setWordWrap(True)
        # image.setObjectName("scan_txt_fr_book")

    def ConvertToQpixmap(self, img, Qlabel):
        if isinstance(img, np.ndarray):
            
            # img = img[int(self.zoom_ratio*h/2):h - int(self.zoom_ratio*h/2), int(self.zoom_ratio*w/2):w - int(self.zoom_ratio*w/2)]
            # img = cv2.resize(img, (Qlabel.size().width(), Qlabel.size().height()))
            img = self.fix_size(img, self.imageLabelEdgeSize, self.imageLabelEdgeSize, (150, 150, 150, 255))
            img = np.array(img)
            h, w, _ = img.shape
            img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            qimg = QImage(img.data, w, h, 3*w, QImage.Format_RGB888) 
            qpixmap = QPixmap(qimg)
            return qpixmap
        else:
            return img

    def find_labels_in_groupbox_and_delete(self):
        labels = []
        try:
            for i in range(len(self.classes)):
                for child in self.group_boxes[i].findChildren(QLabel):
                    if not child.isVisible():
                        labels.append(child.objectName())
                    child.deleteLater()
            #Delete
            for item in self.currentAnnotation['shapes'][:]: 
                if item['position'] in labels:
                    self.currentAnnotation['shapes'].remove(item)
                else:
                    del item['position']
        except:
            print('find_labels_in_groupbox_and_delete')
            return False
        return True
    
    def SaveAnnotationToJson(self):
        #Create backup_file

        #Save/overwrite file
        with open(self.json_files[self.annotationIndex], 'w') as json_file:
            json.dump(self.currentAnnotation, json_file)

    def UploadImagesToUI(self):
        # self.images_path = "/Users/hungnguyencong/Downloads/hung.PNG"
        # image = cv2.imread(self.images_path)
        # for i in range(20):
        #     self.SetImageToGroup(image, 1, i,self.numberOfColumn)
        # return
        for inx in range(len(self.currentAnnotation['shapes'])):
            label,bbox, element_dict = self.GetImageAnnotation(inx)
            group_index = self.classes.index(label)
            crop_image = self.currentImage[bbox[1]:bbox[3],bbox[0]:bbox[2]]
            self.SetImageToGroup(crop_image,group_index,self.Group_image_index[group_index],self.numberOfColumn, element_dict)
            self.Group_image_index[group_index] += 1
            # break
            
    def GetImageAnnotation(self, inx):
        element_dict = self.currentAnnotation['shapes'][inx]
        label = element_dict['label']
        bbox = element_dict['description'].split(',')
        bbox = [int(x) for x in bbox]
        return label,bbox,element_dict


    def ReadAnnotationInit(self):
        files = os.listdir(self.annotation_dir_path)
        self.json_files = [os.path.join(self.annotation_dir_path, file) for file in files if file.endswith('.json')]
        self.annotationIndex = 0
        self.FileNameTxt.setText(os.path.basename(self.json_files[self.annotationIndex]))
        self.currentAnnotation = self.ReadJson(self.json_files[self.annotationIndex])
        self.currentImage = self.ReadImage(self.json_files[self.annotationIndex].replace('json','PNG'))
    
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
        numberOfImage = max(dict(Counter(shape['label'] for shape in data['shapes'])).values())
        self.imageLabelEdgeSize = int(np.sqrt(self.GroupBoxArea/numberOfImage))
        self.numberOfColumn = int(self.group_boxes[0].size().width()/self.imageLabelEdgeSize)

        return data

        # Now you can work with the 'data' object, which contains the contents of the JSON file


    def fix_size(self,fn, desired_w=256, desired_h=256, fill_color=(0, 0, 0, 255)):
        """Edited from https://stackoverflow.com/questions/44231209/resize-rectangular-image-to-square-keeping-ratio-and-fill-background-with-black"""
        im = Image.fromarray(fn)
        x, y = im.size

        ratio = x / y
        desired_ratio = desired_w / desired_h

        w = max(desired_w, x)
        h = int(w / desired_ratio)
        if h < y:
            h = y
            w = int(h * desired_ratio)

        new_im = Image.new('RGBA', (w, h), fill_color)
        new_im.paste(im, ((w - x) // 2, (h - y) // 2))
        return new_im.resize((desired_w, desired_h))

    # def SetGroupSize():
    #     self.ClassNameGroup_1.setGeometry(QRect(self.class_pannel_size, 50, 121, 391))

    def open_input_folder_dialog(self):
        self.annotation_dir_path = QFileDialog.getExistingDirectory(self,"Select input annotations folder", "",QFileDialog.ShowDirsOnly)
        if not self.annotation_dir_path:
            return
        else:
            if os.path.exists(self.annotation_dir_path):
                self.directoryPathTxt.setText(self.annotation_dir_path)
                self.ReadAnnotationInit()
                self.UploadImagesToUI()
        # self.db_directory = '/Users/hungnguyencong/Desktop/DU AN CUA HUNG/PYTHON_CODE/django_flashcard'
        # self.reload_ui_display_after_picking_db()

    def removeChildren(self):
        for group_box in self.group_boxes:
            if group_box:
                group_layout = group_box.layout()
                while group_layout.count():
                    item = group_layout.takeAt(0)
                    widget = item.widget()
                    if widget:
                        widget.deleteLater()

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

        #Load new annotation
        self.annotationIndex += 1
        if len(self.json_files) <= self.annotationIndex:
            return
        self.FileNameTxt.setText(os.path.basename(self.json_files[self.annotationIndex]))
        self.currentAnnotation = self.ReadJson(self.json_files[self.annotationIndex])
        self.currentImage = self.ReadImage(self.json_files[self.annotationIndex].replace('json','PNG'))
        
        self.Group_image_index = [0]*len(self.classes)
        self.UploadImagesToUI()

app = QApplication(sys.argv)
my_wnd = MyMainWindow()
my_wnd.show()
sys.exit(app.exec_())