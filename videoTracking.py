import os

import cv2, datetime, time, pandas
from datetime import datetime


class VideoTracking:

    def __init__(self):
        self.dataframe = pandas.DataFrame(columns=["Start", "End"])
        self.video = cv2.VideoCapture(0)
        self.firstFrame = None
        self.statusList = [None, None]
        self.times = []

    @property
    def getVideoFeed(self):
        while True:
            check, frame = self.video.read()
            status = 0
            grayFrame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            grayFrame = cv2.GaussianBlur(grayFrame, (21, 21), 0)

            if self.firstFrame is None:
                self.firstFrame = grayFrame
                continue

            deltaFrame = cv2.absdiff(self.firstFrame, grayFrame)
            thresFrame = cv2.threshold(deltaFrame, 30, 255, cv2.THRESH_BINARY)[1]
            thresFrame = cv2.dilate(thresFrame, None, iterations=2)

            (cont, _) = cv2.findContours(thresFrame.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            for counter in cont:
                if cv2.contourArea(counter) < 10000:
                    continue
                status = 1
                (x, y, z, w) = cv2.boundingRect(counter)
                cv2.rectangle(frame, (x, y), (x + z, y + w), (0, 255, 0), 4)

            self.statusList.append(status)
            if self.statusList[-1] == 1 and self.statusList[-2] == 0:
                self.times.append(datetime.now())
            if self.statusList[-1] == 0 and self.statusList[-2] == 1:
                self.times.append(datetime.now())

            now = datetime.now()
            p = os.path.sep.join(['shots', "shot_{}.png".format(str(now).replace(":", ''))])
            cv2.imwrite(p, frame)
            key = cv2.waitKey(1)

            try:
                ret, buffer = cv2.imencode('.jpg', cv2.flip(frame, 1))
                frame = buffer.tobytes()
                yield (b'--frame\r\n'
                       b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')
            except Exception as e:
                pass

            if key == ord("q"):
                break

        for i in range(0, len(self.times), 2):
            df = self.dataframe.append({"Start": self.times[i], "End": self.times[i + 1]}, ignore_index=True)

        self.dataframe.to_csv("MotionCaptureTimes.csv")
        self.video.release()
        cv2.destroyAllWindows()
