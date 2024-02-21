# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'AnnotationCorrectionrKRCZs.ui'
##
## Created by: Qt User Interface Compiler version 5.15.2
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5 import *


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.resize(1440, 785)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.LoadFolderBtn = QPushButton(self.centralwidget)
        self.LoadFolderBtn.setObjectName(u"LoadFolderBtn")
        self.LoadFolderBtn.setGeometry(QRect(10, 10, 61, 32))
        self.directoryPathTxt = QLabel(self.centralwidget)
        self.directoryPathTxt.setObjectName(u"directoryPathTxt")
        self.directoryPathTxt.setGeometry(QRect(180, 20, 301, 16))
        self.FileNameTxt = QLabel(self.centralwidget)
        self.FileNameTxt.setObjectName(u"FileNameTxt")
        self.FileNameTxt.setGeometry(QRect(660, 20, 351, 20))
        self.NextFileBtn = QPushButton(self.centralwidget)
        self.NextFileBtn.setObjectName(u"NextFileBtn")
        self.NextFileBtn.setGeometry(QRect(1080, 10, 113, 51))
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QMenuBar(MainWindow)
        self.menubar.setObjectName(u"menubar")
        self.menubar.setGeometry(QRect(0, 0, 1440, 21))
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName(u"statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)

        QMetaObject.connectSlotsByName(MainWindow)
    # setupUi

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", u"MainWindow", None))
        self.LoadFolderBtn.setText(QCoreApplication.translate("MainWindow", u"Folder", None))
        self.directoryPathTxt.setText(QCoreApplication.translate("MainWindow", u"PathName", None))
        self.FileNameTxt.setText(QCoreApplication.translate("MainWindow", u"FileName", None))
        self.NextFileBtn.setText(QCoreApplication.translate("MainWindow", u"Next", None))
    # retranslateUi

