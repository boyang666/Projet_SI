#!/usr/bin/python2
# -*- encoding: utf-8 -*-

import algo
import os.path
import cv2
import numpy as np
import ZoneInteret as zi


class algo_distance(algo.algorithme):
    """
    Cette classe hérite la classe algo pour implémenter les méthodes
    Cette classe utilise l'algo de distance pour traiter la vidéo.
    Cet algo compare la différence des pixels entre deux frames successives,
    le nombre de changement est enregistré comme un indicateur de détection de stress
    @version 2.0
    """


    def get_nomAlgo(self):
        return "distance"

    def traiterVideo(self, video, start_frame):
        ma_liste = list()
        if type(video) is str:
            if not os.path.exists(video):
                raise Exception("Le fichier video '" + video + "' Introuvable!")
            cap = cv2.VideoCapture(video)
        else:
            cap = video


        # Detection de l'opérateur
        # On ne commence le traitement sur la première image dépourvu d'opérateur
        # On Passe les images
        # tant que l'indice ne correspond pas à ce que la méthode isoler_operateur() nous a renvoye plus tôt
        for i in range(0, start_frame):
            cap.read()

        # Premières captures
        ret, old_frame = cap.read()
        ret, frame = cap.read()

        # Si la ZoneInteret a été selectionnée on récupère les paramètres de cette dernière
        # et on les appliques aux frames
        if zi.ZoneInteret.verifier_presence_fichier_ini() :
            with open("./zi/param.ini", "r") as file:
                line = file.readline()
                param = [int(x.strip()) for x in line.split(',')]
            frame = frame[param[1]:param[1] + param[3], param[0]:param[0] + param[2]]
            old_frame = old_frame[param[1]:param[1] + param[3], param[0]:param[0] + param[2]]

        old_gray = cv2.cvtColor(old_frame, cv2.COLOR_BGR2GRAY)
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        # Matrice de cumul de différences
        differences = np.zeros(frame_gray.shape, dtype=np.int32)

        while ret:
            frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            nvdifferences = cv2.absdiff(old_gray, frame_gray)
            ma_liste.append(np.mean(np.add(differences, nvdifferences, dtype=np.int32)))
            old_gray = frame_gray.copy()
            differences = nvdifferences
            ret, frame = cap.read()

            # On applique les paramètres à chaque frame
            if ret and zi.ZoneInteret.verifier_presence_fichier_ini():
                frame = frame[param[1]:param[1] + param[3], param[0]:param[0] + param[2]]

        cap.release()

        return ma_liste

