import cv2
import os

class RemoveOperator:
    """
    Cette classe est pour detecter l'operateur dans la video et generer un nouvel video sans operateur
    @version 1.0
    """
    def remove_operator(self, video):
        """
        Cette méthode permet de prendre la vidéo d'entrée pour détecter l'opérateur dans la vidéo.
        Après elle retourne la nouvelle vidéo sans l'opérateur
        :param video: la vidéo d'origine
        :return: la video sans l'opérateur
        """

        # si le video ne peut pas etre trouve
        if (not os.path.exists(video)):
            print("video non trouve")

        # lire video
        cap = cv2.VideoCapture(video)

        # configurer l'indice de la frame
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)

        # obtenir le nombre de frame dans le video
        totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)

        # obtenir la taille du video
        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        # calculer l'indice de frame
        midFrame = totalFrameNumber / 2
        threeFourth = totalFrameNumber / 4 * 3
        threeFourth = 100
        numFrame = 0

        # sum de valeur de girs de la frame correspondant
        sumGray = 0
        sumGray1 = 0
        sumGray2 = 0

        # obtenir les deux frame(1/2,3/4)
        cap.set(cv2.CAP_PROP_POS_FRAMES, midFrame)
        ret1, frame1 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, threeFourth)
        ret2, frame2 = cap.read()

        # Convertir en niveaux de gris
        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        for i in range(0, height):
            sumGray1 += sum(gray1[i])
            sumGray2 += sum(gray2[i])

        # Calculer le taux de changement
        if (sumGray1 >= sumGray2):
            percente = (sumGray1 - sumGray2) / sumGray1 * 10000
        else:
            percente = (sumGray2 - sumGray1) / sumGray1 * 10000

        # Définir le taux de changement ne dépasse pas le seuil
        if percente > 400:
            percente = 400

        # generer le nouvle video
        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        remove_index = str(video).index('.')
        video_remove = str(video)[0:remove_index] + "_remove.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        videoWriter = cv2.VideoWriter(video_remove, fourcc, fps, size)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

        # calculer le taux de changement a partir de la première frame
        while ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sumGray = 0
            for i in range(0, height):
                sumGray += sum(gray[i])
            if (sumGray >= sumGray1):
                perc = (sumGray - sumGray1) / sumGray1 * 10000
            else:
                perc = (sumGray1 - sumGray) / sumGray1 * 10000

            # si le taux de changement inferieur que le taux calcule, ajouter dans le nouvel video
            if perc <= percente:
                videoWriter.write(frame)

            # lire la frame suivante
            ret, frame = cap.read()
        cap.release()
        return video_remove
