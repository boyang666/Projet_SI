import Fen_principale_design
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
from ZoneInteret import *
from Fen_SelectZI import Fen_selectZI
from PIL import Image
import cv2
import numpy as np
import affichage_graphique
import threading
import subprocess
import algo_distance
import algo_flots_optiques


def lancer_video(video):
    subprocess.Popen([os.path.join("vlc"), os.path.join(video)])

def thread(video, unAlgo, frame):
     ma_liste = unAlgo.traiterVideo(video, frame)
     pomme = affichage_graphique.affichage_graphique(video, frame)
     #thread_video = threading.Thread(None, lancer_video, None,(), kwargs={'video': video})
     #thread_video.start()
     pomme.afficher(ma_liste)

class Fen_principale(QtWidgets.QMainWindow, Fen_principale_design.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Fen_principale_design.Ui_MainWindow.__init__(self)
        self.lowH = 0
        self.highH = 0
        self.start_frame = 3

        self.setupUi(self)
        self.pushButton_parcourir.clicked.connect(self.parcourir_clicked)
        self.pushButton_choisir_couleur.clicked.connect(self.couleur_choisir_clicked)
        self.pushButton_zi.clicked.connect(self.zone_interet_clicked)
        self.couleur_name = "#000000"
        #self.pushButton_valider_couleur.clicked.connect(self.on_btn_operator_clicked)
        self.pushButton_lancer.clicked.connect(self.on_myButton_clicked)

    def parcourir_clicked(self):
        filename, types = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_path.setText(str(filename))

    def couleur_choisir_clicked(self):
        couleur = QtWidgets.QColorDialog.getColor()
        if couleur.isValid():
            self.couleur_name = couleur.name()
            self.lineEdit_couleur_choisie.setStyleSheet('QWidget {background-color:%s}'%self.couleur_name)

    def zone_interet_clicked(self):
        choix = self.comboBox_zone.currentIndex()
        if choix == 0:
            self.fen_selectZI = Fen_selectZI(self.lineEdit_path.text())
            self.fen_selectZI.show()
            if ZoneInteret.verifier_presence_fichier_ini():
                img = Image.open('zi/image_zone_interet.png')
                img_resize = img.resize((self.label_zi_img.width(), self.label_zi_img.height()))
                img_resize.save('zi/image_zone_interet_temp.png')
                pixmap = QtGui.QPixmap('zi/image_zone_interet_temp.png')
                self.label_zi_img.setPixmap(pixmap)
                os.remove('zi/image_zone_interet_temp.png')
        elif choix == 1:
            # Presence du fichier "param.ini"
            if ZoneInteret.verifier_presence_fichier_ini():
                img = Image.open('zi/image_zone_interet.png')
                img_resize = img.resize((self.label_zi_img.width(), self.label_zi_img.height()))
                img_resize.save('zi/image_zone_interet_temp.png')
                pixmap = QtGui.QPixmap('zi/image_zone_interet_temp.png')
                self.label_zi_img.setPixmap(pixmap)
                os.remove('zi/image_zone_interet_temp.png')
            else:
                QMessageBox.warning(self, "Erreur", "Impossible de trouver les fichiers dans le repertoire /zi",
                                    QMessageBox.Ok)
        else:
            button = QMessageBox.question(self, "Question", "Etes-vous sûr de vouloir supprimer la Zone d'intérêt actuelle ？",
                                          QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
            if button == QMessageBox.Ok:
                ZoneInteret.supprimer_ZI(self)
                self.label_zi_img.clear()

    # Gère l'appui du bouton "Valider couleur"
    def on_btn_operator_clicked(self):
        self.plainTextEdit_histoire.setPlainText("")
        toHex = self.couleur_name
        #list1 = list(self.couleur.to_string())
        #list2 = ['#', list1[1], list1[2], list1[5], list1[6], list1[9], list1[10]]
        #toHex = ''.join(list2)
        print(toHex)
        RGB = self.hex_to_rgb(toHex)
        print(toHex)
        print(RGB)
        self.couleur_name = np.uint8([[[RGB[0], RGB[1], RGB[2]]]])
        hsv_color = cv2.cvtColor(self.couleur_name, cv2.COLOR_RGB2HSV)
        hue = hsv_color[0][0][0]
        self.lowH = hue - 20
        self.highH = hue + 100
        if self.lowH < 0:
            self.lowH = 0
        if self.highH < 0:
            self.highH = 0

        self.isoler_operator()


    # Converti valeurs hexa en RGB
    def hex_to_rgb(self, value):
        """Return (red, green, blue) for the color given as #rrggbb."""
        value = value.lstrip('#')
        lv = len(value)
        return tuple(int(value[i:i + lv // 3], 16) for i in range(0, lv, lv // 3))

    # Permet de retourner la première image d'une vidéo ne comportant pas la couleur désirée
    def isoler_operator(self):
        self.plainTextEdit_histoire.insertPlainText("\n" + "Detection de l'opérateur...")
        video_path = self.lineEdit_path.text()
        if (os.path.exists(video_path)):
            cap = cv2.VideoCapture(video_path)
            while (cap.isOpened()):
                ret, frame = cap.read()
                if ret == True:
                    # Transformation en HSV
                    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
                    print(hsv)
                    # Paramètres hsv pour isoler la couleur teinte, saturation, Valeur
                    # Teinte = couleur
                    # Saturation : L'intensité de la couleur
                    # Valeur : Brillance de couleur
                    lower_color = np.array([self.lowH, self.lowH, self.lowH])
                    upper_color = np.array([self.highH, self.highH, self.highH])
                    mask = cv2.inRange(hsv, lower_color, upper_color)
                    #kernel = np.ones((5, 5), np.uint8)
                    kernel = cv2.getStructuringElement(cv2.MORPH_RECT, (3, 3))
                    # lissage pour enlever des éventuels bruits
                    erosion = cv2.erode(mask, kernel, iterations=1)
                    print(lower_color)
                    print(upper_color)
                    print(erosion)
                    # detection des contours de l'operateur
                    ret, binary = cv2.threshold(erosion, cv2.THRESH_BINARY)
                    contours, hierarchy = cv2.findContours(binary, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
                    if (len(contours) > 0):
                        # operateur présent

                        cv2.drawContours(frame, contours, -1, (0, 255, 0), 3)
                        self.start_frame = self.start_frame + 1
                        image = Image.fromarray(frame, 'RGB')
                        image.save("tmp.jpeg")
                        #self.GTKImage.set_from_file("tmp.jpeg")
                        pixmap = QtGui.QPixmap("tmp.jpeg")
                        self.label_valider_operateur.setPixmap(pixmap)
                    else:
                        break
                    if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
                    if cap.get(cv2.CAP_PROP_POS_FRAMES) == cap.get(cv2.CAP_PROP_FRAME_COUNT):
                        # If the number of captured frames is equal to the total number of frames, we stop
                        break
            self.plainTextEdit_histoire.insertPlainText("Opérateur détecté!")




    # Gère l'appui du bouton pour lancer le traitement
    def on_myButton_clicked(self):
        # Choix de l'algorithme
        self.plainTextEdit_histoire.setPlainText("")
        algo = self.comboBox_algo.currentIndex() + 1
        video_name = self.lineEdit_path.text()
        # Si la vidéo existe, on lance un autre thread en exécutant le bon algo
        if (os.path.exists(video_name)):
            #self.spinner.start()
            self.plainTextEdit_histoire.insertPlainText("\n" + "Suppression de l'opérateur de la vidéo...")

            self.plainTextEdit_histoire.insertPlainText("\n" + "Suppression terminé...")

            # Algorithme Distance
            if (algo == 1):
                self.plainTextEdit_histoire.insertPlainText("\n" + "Application de l'algorithme Distances...")
                a = threading.Thread(None, thread, None, (),
                                     {'video': video_name, 'unAlgo': algo_distance.algo_distance(),
                                      'frame': self.start_frame})
                a.start()
                # Algorithme flotsoptiques
            elif (algo == 2):
                self.plainTextEdit_histoire.insertPlainText("\n" + "Application de l'algorithme flots optiques...")
                a = threading.Thread(None, thread, None, (), {'video': video_name,
                                                              'unAlgo': algo_flots_optiques.algo_flots_optiques(),
                                                              'frame': self.start_frame})
                a.start()
            #self.spinner.stop()
        else:
            print("no video")