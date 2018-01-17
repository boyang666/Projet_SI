# -*- coding: utf-8 -*-
import os.path
import cv2
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
from matplotlib.patches import Rectangle
from PyQt5.QtWidgets import QMessageBox

class ZoneInteret:

    """
    Cette classe permet de gérer les information de zone interet
    Une zone interet est un cadre d'image sur l'image entière.
    On se concentre sur cette zone interet pour faire le traitement.
    C'est une manière de réduire le bruit sur le résultat de traitement
    @version 2.0
    """

    @staticmethod
    def verifier_presence_fichier_ini():
        """
        Vérifier si les fichiers de zone interet sont déjà présents dans le dossier
        :return: true si présent, false sinon
        """
        return os.path.isfile('./zi/param.ini')

    @staticmethod
    def supprimer_ZI(window):
        """
        La méthode pour gérer la suppresion de zone interet
        :param window: le fenetre principale
        :return:
        """
        if os.path.isfile('./zi/param.ini'):
            try:
                os.remove("./zi/param.ini")
                os.remove("./zi/image_modele.png")
                os.remove("./zi/image_zone_interet.png")
                QMessageBox.information(window, "Information", "Supprimer la Zone d'intérêt avec succès", QMessageBox.Ok)
            except OSError:
                QMessageBox.warning(window, "Erreur", "Impossible de supprimer les fichiers dans le repertoire /zi",
                                    QMessageBox.Ok)
        else:
            QMessageBox.warning(window, "Erreur", "Impossible de trouver les fichiers dans le repertoire /zi",
                                QMessageBox.Ok)


    def __init__(self, video):
        """
        Initialise les variables nécessaires à l'affichage de l'image et aux événements
        :param video: la vidéo à traiter
        """
        self.flag = False
        self.get_one_image_from_video(video)

        # On se sert de l'image extraite précédemment
        self.img = mpimg.imread('./zi/image_modele.png')

        # On initialise le titre de la fenêtre
        fig = plt.figure(1)
        fig.canvas.set_window_title("Zone Interet")

        # On récupère les infos des axes
        self.ax = plt.gca()

        # On initialise le futur rectangle dessiné (non rempli aux bordures rouges)
        self.rect = Rectangle((0, 0), 1, 1, fill=False, edgecolor="red")

        # Initialisation des points du rectangle
        self.x0 = None
        self.y0 = None
        self.x1 = None
        self.y1 = None
        self.ax.add_patch(self.rect)

        # Liaison des événements
        self.ax.figure.canvas.mpl_connect('button_press_event', self.on_mouseclick_press)
        self.ax.figure.canvas.mpl_connect('button_release_event', self.on_mouseclick_release)
        self.ax.figure.canvas.mpl_connect('key_press_event', self.on_keyboard_press)

        # Affichage de l'image dans la fenêtre
        self.imgplot = plt.imshow(self.img)

        self.show_window()

    def on_mouseclick_press(self, event):
        """
        Un click gauche -> sauvegarde des coordonnées du pointeur
        :param event: évènement de clique
        :return:
        """
        self.x0 = event.xdata
        self.y0 = event.ydata


    def on_mouseclick_release(self, event):
        """
        Click gauche relâché -> dessin du rectangle
        :param event: évènement de souris
        :return:
        """
        self.x1 = event.xdata
        self.y1 = event.ydata
        self.rect.set_width(self.x1 - self.x0)
        self.rect.set_height(self.y1 - self.y0)
        self.rect.set_xy((self.x0, self.y0))
        self.ax.figure.canvas.draw()


    def on_keyboard_press(self, event):
        """
        Si la touche "enter" est appuyée, on sauvegarde la zone d'intérêt
        :param event: évenenment de keyboard
        :return:
        """
        if event.key == 'enter':
            self.flag = True
            with open("./zi/param.ini", "w") as file:
                file.write(str(int(self.rect.get_x())) + ",")
                file.write(str(int(self.rect.get_y())) + ",")
                file.write(str(int(self.rect.get_width())) + ",")
                file.write(str(int(self.rect.get_height())))

            # On cache les axes avant d'enregistrer l'image modele avec la zone d'interet
            self.ax.get_xaxis().set_visible(False)
            self.ax.get_yaxis().set_visible(False)
            plt.title("Zone interet")
            plt.savefig("./zi/image_zone_interet.png")
            plt.close()


    def show_window(self):
        """
        Pour afficher la fenêtre qui est utilisée pour choisir une zone interet
        :return:
        """
        plt.title("Selectionner la zone interet avec la souris. Appuyez sur entrer pour valider.")
        plt.show()

    def get_one_image_from_video(self, video):
        """
        Extrait une image de la vidéo selectionnée
        Cette image est utilisée pour choisir une zone interet
        :param video: la vidéo choisie
        :return:
        """
        video_capture = cv2.VideoCapture(video)
        nb_frame = video_capture.get(cv2.CAP_PROP_FRAME_COUNT)
        video_capture.set(cv2.CAP_PROP_FRAME_COUNT, int(nb_frame - 1))
        success, self.image = video_capture.read()
        #sauvegarder l'image
        cv2.imwrite("zi/image_modele.png", self.image)




