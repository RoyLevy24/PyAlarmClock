import math
import time

import cv2
import dlib
import imutils
from imutils import face_utils
from imutils.video import VideoStream
from scipy.spatial import distance as dist


class OpenEyesDetect():
    """
    This class is responsible of detecting that 
    a user has opened his eyes for a certain amount of time.
    """
    __instance = None

    @staticmethod
    def getInstance():
        """
        Creates OpenEyesDetect instance if not already exists.
        Returns OpenEyesDetect instance.
        """
        if OpenEyesDetect.__instance == None:
            OpenEyesDetect()
        return OpenEyesDetect.__instance

    def __init__(self):
        """
        Creates OpenEyesDetect instance if not already exists.
        """
        if OpenEyesDetect.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            # set up path for face landmarks predictor
            pred_path = "backend/OpenEyesDetection/face_landmarks_predictor.dat"
            self.PREDICTOR_PATH = pred_path
            print(self.PREDICTOR_PATH)
            OpenEyesDetect.__instance = self

    def get_frames_per_seconds(self, camera_num):
        """
        Calculates a camera frames per seconds.

        Args:
            camera_num (int): device number of the camera.
        """
        # Start camera
        video = cv2.VideoCapture(camera_num)
        num_frames = 60

        start = time.time()
        for i in range(0, num_frames):
            ret, frame = video.read()
        end = time.time()

        # Time elapsed
        seconds = end - start
        # Calculate frames per second
        fps = num_frames / seconds

        video.release()

        return math.floor(fps)

    def get_eye_aspect_ratio(self, eye):
        """
        Calculate eye aspect ratio for an eye
        """
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
        """
        Detecting that the user has opened his eyes for certain amount of time.

        Args:
            staring_time (int): time in seconds the user needs to keep his eyes open.
            camera_num (int): device number of the camera the method uses.
            ear_threshold (float): eye aspect ratio threshold for detecting an eye is opened.

        """
        # setting up amount of frames the user has opened his eyes
        open_eyes_frames_num = 0

        # getting detector and predictor objects from dlib
        detector = dlib.get_frontal_face_detector()
        predictor = dlib.shape_predictor(self.PREDICTOR_PATH)

        # getting the facial landmarks of left and right eyes
        (left_start, left_end) = face_utils.FACIAL_LANDMARKS_IDXS["left_eye"]
        (right_start,
         right_end) = face_utils.FACIAL_LANDMARKS_IDXS["right_eye"]

        # calculate frames per seconds based on the camera
        fps = self.get_frames_per_seconds(camera_num)

        # estimating amount of frames needed
        consec_frames_threshold = math.floor(staring_time * fps * 0.6)

        # staring the camera
        vs = VideoStream(camera_num).start()
        while open_eyes_frames_num <= consec_frames_threshold:
            # getting the current frame
            frame = vs.read()
            frame = imutils.resize(frame, width=450)
            gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

            # detect face in the frame
            face_rects = detector(gray_frame, 0)

            for face_rect in face_rects:
                # finds the facial landmarks in the frame
                shape = predictor(gray_frame, face_rect)
                # converts the facial landmarks for np.array
                shape = face_utils.shape_to_np(shape)

                # extract the left and right eye coordinates from the facial landmarks
                left_eye = shape[left_start:left_end]
                right_eye = shape[right_start:right_end]

                # compute eye aspect ratio for the eyes
                left_EAR = self.get_eye_aspect_ratio(left_eye)
                right_EAR = self.get_eye_aspect_ratio(right_eye)
                ear = (left_EAR + right_EAR) / 2.0

                # coputes the smallest shape to connect the eye coordinates for visualization
                left_eye_hull = cv2.convexHull(left_eye)
                right_eye_hull = cv2.convexHull(right_eye)

                # draw the shape computed surrounding the eyes
                cv2.drawContours(frame, [left_eye_hull], -1, (0, 255, 0), 1)
                cv2.drawContours(frame, [right_eye_hull], -1, (0, 255, 0), 1)

                # increment the frames the user opened his eyes if the
                # computed ear >= ear_threshold
                if (ear >= ear_threshold):
                    if (open_eyes_frames_num <= consec_frames_threshold):
                        open_eyes_frames_num += 1

                cv2.putText(frame, "FR_OPEN_EYES: {}".format(open_eyes_frames_num), (10, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)
                cv2.putText(frame, "EAR: {:.2f}".format(ear), (300, 30),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 0, 255), 2)

            # showing current frame
            cv2.imshow("Detect Open Eyes", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("q"):
                break
        cv2.destroyAllWindows()
        vs.stop()
