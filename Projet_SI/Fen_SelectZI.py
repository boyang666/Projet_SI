#!/usr/bin/python
# -*- coding: utf-8 -*-

import cv2
import Fen_SelectZI_design
import ZoneInteret as zi
from PyQt5 import QtCore, QtGui, QtWidgets
from PIL import Image
import os

# Gère l'affichage de la fenetre de selection de la Zi
class Fen_selectZI(QtWidgets.QDialog, Fen_SelectZI_design.Ui_Fen_SelectZI_Dialog):

    # initialise la fenêtre de Zone Interet
    def __init__(self, filename):
        QtWidgets.QDialog.__init__(self)
        Fen_SelectZI_design.Ui_Fen_SelectZI_Dialog.__init__(self)
        self.setupUi(self)
        video = filename
        self.get_one_image_from_video(video)

    # extrait une image de la vidéo selectionnée
    def get_one_image_from_video(self, video):
        video_capture = cv2.VideoCapture(video)
        # TODO : bien récupérer la dernière frame
        nb_frame = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        video_capture.set(cv2.CAP_PROP_FRAME_COUNT, int(nb_frame - 1))
        success, self.image = video_capture.read()
        print(success)
        cv2.imwrite("zi/image_modele.png", self.image)
        self.show_ZI_window()
        img = Image.open('zi/image_zone_interet.png')
        img_resize = img.resize((self.label.width(), self.label.height()))
        img_resize.save('zi/image_zone_interet_temp.png')
        pixmap = QtGui.QPixmap('zi/image_zone_interet_temp.png')
        self.label.setPixmap(pixmap)
        os.remove('zi/image_zone_interet_temp.png')

    def show_ZI_window(self):
        select_zi = zi.ZoneInteret()
        select_zi.show_window()


