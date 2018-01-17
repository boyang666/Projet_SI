import Fen_principale_design
from PyQt5 import QtGui, QtWidgets
from PyQt5.QtWidgets import QApplication
import os
from ZoneInteret import *
from PIL import Image
import affichage_resultat
import threading
import algo_distance
import algo_flots_optiques
import remove_operateur
import time

def thread(video, unAlgo, frame):
    """
    Cette méthode permet de créer un job avec un vidéo, un algo et le frame à commencer.
    Ce job peut être utilisé dans un thread pour gagner la vitesse de calcul

    :param video: la vidéo à traiter
    :param unAlgo: l'algo
    :param frame: le frame à commencer
    :return:
    """
    ma_liste = unAlgo.traiterVideo(video, frame)
    pomme = affichage_resultat.affichage_graphique(video, frame)
    pomme.afficher(ma_liste)


class Fen_principale(QtWidgets.QMainWindow, Fen_principale_design.Ui_MainWindow):

    """
    Cette classe hérite la classe de Fen_principale_design pour enrichir les fonctionnalités de la fenêtre principale.
    Toutes les opérations et signals sont définis dans cette classe.

    @author Boyang Wang
    @version 2.0
    """

    def __init__(self):
        """
        Le constructeur pour créer les signals et la création de UI
        """

        QtWidgets.QMainWindow.__init__(self)
        Fen_principale_design.Ui_MainWindow.__init__(self)
        self.lowH = 0
        self.highH = 0
        self.start_frame = 3

        self.setupUi(self)
        self.group = QtWidgets.QButtonGroup()
        self.group.addButton(self.radioButtonOui)
        self.group.addButton(self.radioButtonNon)
        self.group.setId(self.radioButtonOui, 0)
        self.group.setId(self.radioButtonNon, 1)
        self.radioButtonNon.setChecked(True)
        self.plainTextEdit_histoire.setReadOnly(True)

        # les signals
        self.pushButton_parcourir.clicked.connect(self.parcourir_clicked)
        self.pushButton_select.clicked.connect(self.zone_interet_select)
        self.pushButton_consulter.clicked.connect(self.zone_interet_consulter)
        self.pushButton_supprimer.clicked.connect(self.zone_interet_supprimer)
        self.pushButton_lancer.clicked.connect(self.on_myButton_clicked)

    def parcourir_clicked(self):
        """
        Cette méthode permet de gérer la clique sur le bouton parcourir pour choisir une vidéo
        :return:
        """
        filename, types = QtWidgets.QFileDialog.getOpenFileName()
        self.lineEdit_path.setText(str(filename))

    def zone_interet_select(self):
        """
        La méthode pour gérer la clique sur le bouton Selectionner une Zone Interet
        Il faut que la vidéo doit être choisi en avance
        Dans la fenêtre principale en haut à droite affiche la zone interêt choisie

        :return:
        """
        if(os.path.exists(self.lineEdit_path.text())):
            zi = ZoneInteret(self.lineEdit_path.text())
            if ZoneInteret.verifier_presence_fichier_ini() and zi.flag:
                img = Image.open('zi/image_zone_interet.png')
                img_resize = img.resize((self.label_zi_img.width(), self.label_zi_img.height()))
                img_resize.save('zi/image_zone_interet_temp.png')
                pixmap = QtGui.QPixmap('zi/image_zone_interet_temp.png')
                self.label_zi_img.setPixmap(pixmap)
                os.remove('zi/image_zone_interet_temp.png')
        else:
            QMessageBox.warning(self, "Erreur", "Impossible de trouver la video",
                                QMessageBox.Ok)


    def zone_interet_consulter(self):
        """
        Le méthode pour gérer la clique sur Consulter une zone interet
        Si les fichiers de zone d'interêt sont présents, dans la fenêtre principale en haut à droite affiche la zone interêt choisie
        :return:
        """

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

    def zone_interet_supprimer(self):
        """
        Le méthode pour gérer la clique sur Supprimer une zone interet
        Les fichiers de zone interêt vont être supprimés
        :return:
        """
        button = QMessageBox.question(self, "Question",
                                      "Etes-vous sûr de vouloir supprimer la Zone d'intérêt actuelle ？",
                                      QMessageBox.Ok | QMessageBox.Cancel, QMessageBox.Ok)
        if button == QMessageBox.Ok:
            ZoneInteret.supprimer_ZI(self)
            self.label_zi_img.clear()


    def on_myButton_clicked(self):
        """
        La méthode pour gère l'appui du bouton pour lancer le traitement
        Cette méthode permet de passer l'algo choisi, la vidéo et la zone interêt à un thread pour traiter
        Si Detection Opérateur est choisi, le programme va tout d'abord supprimer l'opérateur dans la vidéo.
        C'est-à-dire qu'on enlève les frames où l'opérateur se présent.
        :return:
        """

        # Choix de l'algorithme
        self.plainTextEdit_histoire.setPlainText("")
        algo = self.comboBox_algo.currentIndex() + 1

        # obtenir la vidéo
        video_name = self.lineEdit_path.text()

        # si détecter l'opérateur est choisi
        if (self.group.checkedId() == 0):

            self.plainTextEdit_histoire.appendPlainText("Suppression de l'opérateur de la vidéo...")
            QApplication.processEvents()
            try:

                # commencer à détecter
                removeObject = remove_operateur.RemoveOperator()
                video_name = removeObject.remove_operator(video_name)

                # fin de détecttion de l'opérateur
                self.plainTextEdit_histoire.appendPlainText("Suppression terminé...")
                QApplication.processEvents()
                time.sleep(2)
            except:
                QMessageBox.warning(self, "Erreur", "Erreurs lors de suppression de l'opérateur",
                                    QMessageBox.Ok)


        # Si la vidéo existe, on lance un autre thread en exécutant le bon algo
        if (os.path.exists(video_name)):

            # Algorithme Distance
            if (algo == 1):
                self.plainTextEdit_histoire.insertPlainText("\n" + "Application de l'algorithme Distances...")
                try:
                    a = threading.Thread(None, thread, None, (),
                                         {'video': video_name, 'unAlgo': algo_distance.algo_distance(),
                                          'frame': self.start_frame})
                    a.start()
                except:
                    QMessageBox.warning(self, "Erreur", "Erreurs lors de l'exécution",
                                        QMessageBox.Ok)
                self.plainTextEdit_histoire.insertPlainText("\n" + "Le résultat est enregistré dans le répertoire /resultats sous format PDF.")

                # Algorithme flotsoptiques
            elif (algo == 2):
                self.plainTextEdit_histoire.insertPlainText("\n" + "Application de l'algorithme flots optiques...")
                try:
                    a = threading.Thread(None, thread, None, (), {'video': video_name,
                                                                  'unAlgo': algo_flots_optiques.flot_optiques(),
                                                                  'frame': self.start_frame})
                    a.start()
                except:
                    QMessageBox.warning(self, "Erreur", "Erreurs lors de l'exécution",
                                        QMessageBox.Ok)
                self.plainTextEdit_histoire.insertPlainText(
                    "\n" + "Le résultat est enregistré dans le répertoire /resultats sous format PDF.")
        else:
            print("no video")