import sys
import os

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from scipy.spatial import distance as dist
import math
import time

class OpenEyesDetect():

    __instance = None

    @staticmethod
    def getInstance():
        if OpenEyesDetect.__instance == None:
            OpenEyesDetect()
        return OpenEyesDetect.__instance
    
    def __init__(self):
        if OpenEyesDetect.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            #TODO: use function from utils
            pred_path = fr'{os.path.join(os.path.dirname(__file__),"face_landmarks_predictor.dat")}'
            self.PREDICTOR_PATH = pred_path.encode(sys.getfilesystemencoding())
            print(self.PREDICTOR_PATH)
            OpenEyesDetect.__instance = self  

    def get_frames_per_seconds(self, camera_num):
        # Start camera
        video = cv2.VideoCapture(camera_num)
        num_frames = 60

        start = time.time()
        for i in range(0, num_frames) :
            ret, frame = video.read()
        end = time.time()
        
        # Time elapsed
        seconds = end - start
        # Calculate frames per second
        fps  = num_frames / seconds
        
        video.release()

        return math.floor(fps)

    def get_eye_aspect_ratio(self, eye):
        # computes the euclidean distance between
        # vertical eye landmarks
        v_left = dist.euclidean(eye[1], eye[5])
        v_right = dist.euclidean(eye[2], eye[4])

        # computes the euclidean distance between
        # horizontal eye landmarks
        h = dist.euclidean(eye[0], eye[3])

        # compute eye aspect ratio
        ear = (v_left + v_right) / (2.0 * h)
        return ear


    def detect_open_eyes(self, staring_time, camera_num, ear_threshold):
        open_eyes_frames_num = 0

        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.PREDICTOR_PATH)

        (left_start, left_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (right_start,
         right_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        print("[INFO] starting video stream thread...")
        print("[INFO] print q to quit...")

        fps = self.get_frames_per_seconds(camera_num)
        # TODO: need to calculate estimated frames. Move 0.6 to variable
        consec_frames_threshold = math.floor(staring_time * fps * 0.6)
        vs = VideoStream(camera_num).start()

        while open_eyes_frames_num <= consec_frames_threshold:
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            face_rects = detector(gray_frame, 0)

            for face_rect in face_rects:
                shape = predictor(gray_frame, face_rect)
                shape = face_utils.shape_to_np(shape)

                left_eye = shape[left_start:left_end]
                right_eye = shape[right_start:right_end]

                left_EAR = self.get_eye_aspect_ratio(left_eye)
                right_EAR = self.get_eye_aspect_ratio(right_eye)
                ear = (left_EAR + right_EAR) / 2.0

                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)

                cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

                if (ear >= ear_threshold):
                    if (open_eyes_frames_num <= consec_frames_threshold):
                        open_eyes_frames_num += 1

                cv2.putText(frame, "FR_OPEN_EYES: {}".format(open_eyes_frames_num), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            cv2.imshow("Detect Open Eyes", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        vs.stop()