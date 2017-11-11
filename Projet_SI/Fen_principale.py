import Fen_principale_design
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication, QMainWindow, QMessageBox
import os
from ZoneInteret import *
from Fen_SelectZI import Fen_selectZI
from PIL import Image

class Fen_principale(QtWidgets.QMainWindow, Fen_principale_design.Ui_MainWindow):
    def __init__(self):
        QtWidgets.QMainWindow.__init__(self)
        Fen_principale_design.Ui_MainWindow.__init__(self)
        self.setupUi(self)
        self.pushButton_parcourir.clicked.connect(self.parcourir_clicked)
        self.pushButton_choisir_couleur.clicked.connect(self.couleur_choisir_clicked)
        self.pushButton_zi.clicked.connect(self.zone_interet_clicked)

    def parcourir_clicked(self):
        filename, types = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_path.setText(str(filename))

    def couleur_choisir_clicked(self):
        couleur = QtWidgets.QColorDialog.getColor()
        if couleur.isValid():
            self.lineEdit_couleur_choisie.setStyleSheet('QWidget {background-color:%s}'%couleur.name())

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




