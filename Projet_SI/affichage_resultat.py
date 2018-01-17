#!/usr/bin/python3
# -*- encoding: utf-8 -*-
import matplotlib.pyplot as plt
from matplotlib import gridspec
from matplotlib.widgets import Cursor
import numpy as np
import cv2
import time

class affichage_graphique:
    """
        Cette class est utilisée pour gère l'affichage du resultat.
        L'affichage se fait dans une nouvelle fenêtre créée par matplotlib.
        Le résultat est une courbe avec un curseur.
        En cliquant sur la courbe, en bas à gauche affichera l'image correspondante

        @version 2.0
    """

    def __init__(self, video, start_frame):
        """
            Le constructeur qui initiale la fenêtre d'affichage
        """
        self.fig = plt.figure(figsize=(10, 8), dpi=80)
        self.gs = gridspec.GridSpec(2, 2)
        self.subplot1 = self.fig.add_subplot(self.gs[0, :])
        self.fig.canvas.mpl_connect('button_press_event', self.__onclick)
        self.fig.canvas.set_window_title('Resultat du traitement')

        self.frame_list = list()
        self.video = video
        self.cap = cv2.VideoCapture(self.video)

        for i in range(0, start_frame):
            self.cap.read()

        self.ret, self.new_frame = self.cap.read()

        while self.ret:
            self.frame_list.append(self.new_frame)
            self.ret, self.new_frame = self.cap.read()

        self.cap.release()


    def __onclick(self, event):
        """
        Gère l'événement du click de souris

        :param event: évènement
        :return:
        """

        x = int(float(event.xdata))
        subplot2 = self.fig.add_subplot(self.gs[1, 0])
        plt.title("Image correspondante :")
        plt.imshow(cv2.cvtColor(self.frame_list[x], cv2.COLOR_BGR2RGB))
        plt.axis("off")
        self.fig.canvas.draw()


    def afficher(self, ma_liste):
        """
        Dessine la courbe de résultats

        :param ma_liste: list de résultat fournis par l'algo de calcul
        :return:
        """
        # Variables utiles
        x = np.array(range(len(ma_liste)))
        y = np.array(ma_liste)
        y_max = max(y)
        y_min = min(y)
        y_mean = np.mean(y)
        localtime = time.localtime(time.time())
        localtime_str = str(localtime.tm_year)+'_'+str(localtime.tm_mon)+'_'+ str(localtime.tm_mday)+'_'+str(localtime.tm_hour)+'h'+str(localtime.tm_min)+'m'+str(localtime.tm_sec)+'s'
        # Initialisation du graphique
        plt.axis([0, len(ma_liste) + 10, 0, int(max(y)) + 10])

        plt.xlabel("Nombre d'images")
        plt.ylabel("Quantite de mouvement")
        plt.tight_layout()

        plt.plot(x, y)

        subplot3 = self.fig.add_subplot(self.gs[1, 1])

        cursor = Cursor(self.subplot1, useblit=True, color='red', linewidth=2)

        plt.title("Statistiques : ")
        plt.axis([0, 100, 0, 100])
        plt.axis("off")
        plt.text(20, 80, "min : " + str(y_min))
        plt.text(20, 60, "max : " + str(y_max))
        plt.text(20, 40, "moyenne : " + str(y_mean))
        plt.show()
        self.fig.savefig('resultats/'+str(localtime_str)+'.pdf')
        plt.close()
