#!/usr/bin/python2
# -*- encoding: utf-8 -*-

from abc import ABCMeta, abstractmethod

class algorithme():
    """
    Classe abstracte qui possède les méthodes à implémenter.
    Cette classe est la classe père de tous les algos.
    @version 2.0
    """

    __metaclass__ = ABCMeta

    #doit retourner une liste
    @abstractmethod
    def traiterVideo(self,video,start_frame):
        """
        Méthode pour traiter la vidéo.
        Le retour est une liste des points qui peuvent être dessinés dans une courbe
        Ces points correspondent aux movement de poulet
        :param video: la vidéo à traiter
        :param start_frame: la frame où on commence le traitement
        :return: une liste de points à dessiner
        """
        pass

    @abstractmethod
    def get_nomAlgo(self):
        """
        Retourner le nom de l'algo qui est utilisé
        :return: le nom de l'algo
        """
        pass



