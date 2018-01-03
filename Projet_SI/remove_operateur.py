import cv2
import os


class RemoveOperator:

    def remove_operator(self, video):
        if (not os.path.exists(video)):
            #os.remove("oto_other.mp4")
            print("video non trouve")
        cap = cv2.VideoCapture(video)
        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        totalFrameNumber = cap.get(cv2.CAP_PROP_FRAME_COUNT)
        #print(totalFrameNumber)

        height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
        width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))

        midFrame = totalFrameNumber / 2
        threeFourth = totalFrameNumber / 4 * 3
        threeFourth = 100
        numFrame = 0
        sumGray = 0
        sumGray1 = 0
        sumGray2 = 0
        cap.set(cv2.CAP_PROP_POS_FRAMES, midFrame)
        ret1, frame1 = cap.read()
        cap.set(cv2.CAP_PROP_POS_FRAMES, threeFourth)
        ret2, frame2 = cap.read()

        gray1 = cv2.cvtColor(frame1, cv2.COLOR_BGR2GRAY)
        gray2 = cv2.cvtColor(frame2, cv2.COLOR_BGR2GRAY)

        for i in range(0, height):
            sumGray1 += sum(gray1[i])
            sumGray2 += sum(gray2[i])

        if (sumGray1 >= sumGray2):
            percente = (sumGray1 - sumGray2) * 10000 / sumGray1
        else:
            percente = (sumGray2 - sumGray1) * 10000 / sumGray1
        if percente > 400:
            percente = 400

        fps = cap.get(cv2.CAP_PROP_FPS)
        size = (int(cap.get(cv2.CAP_PROP_FRAME_WIDTH)),
                int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT)))

        remove_index = str(video).index('.')
        video_remove = str(video)[0:remove_index] + "_remove.avi"

        fourcc = cv2.VideoWriter_fourcc(*'XVID')
        #videoWriter = cv2.VideoWriter(video_remove, cv2.CAP_PROP_FOURCC, fps, size)
        videoWriter = cv2.VideoWriter(video_remove, fourcc, fps, size)

        cap.set(cv2.CAP_PROP_POS_FRAMES, 0)
        ret, frame = cap.read()

        while ret:
            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            sumGray = 0
            for i in range(0, height):
                sumGray += sum(gray[i])
            if (sumGray >= sumGray1):
                perc = (sumGray - sumGray1) / sumGray1 * 10000
            else:
                perc = (sumGray1 - sumGray) / sumGray1 * 10000
            #print(perc)
            if perc <= percente:
                videoWriter.write(frame)

            ret, frame = cap.read()
        cap.release()
        return video_remove
