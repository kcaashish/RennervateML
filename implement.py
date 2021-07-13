# importing the required libraries
import os
from typing import OrderedDict
import time
import datetime
import threading
from pydub import AudioSegment
from pydub.playback import play
import cv2
import dlib
from formulae import eye_aspect_ratio, mouth_aspect_ratio
from dataProcessor import save_ear
from dlib68 import download_detector
import pickle


start_time = time.time()


def raise_alarm():
    "used to play the alarm sound on loop"
    alert_sound = AudioSegment.from_wav("audio/beep-06.wav")
    while ALARM_ON:
        play(alert_sound)


def logger(message):
    "used to log messages"
    if __debug__:
        print(message)


def main():
    EAR_THRESH = 0.25
    EAR_CONSECUTIVE_FRAMES = 42

    COUNTER = 0
    # count = 0
    global ALARM_ON
    # ALARM_ON = False

    print("Preparing the detectors:")
    download_detector()
    print("Loading modules:")
    loaded_model = pickle.load(open("knn_model.sav", "rb"))

    start = datetime.datetime.now()
    P = "shape_predictor_68_face_landmarks.dat"
    print("Loading facial landmark predictor...")

    detector = dlib.get_frontal_face_detector()
    predictor = dlib.shape_predictor(P)
    after_model_load = datetime.datetime.now()

    # For dlib's 68-point facial detector:
    FACIAL_LANDMARKS = OrderedDict(
        [
            ("jaw", list(range(0, 17))),
            ("right_eyebrow", list(range(17, 22))),
            ("left_eyebrow", list(range(22, 27))),
            ("nose", list(range(27, 36))),
            ("right_eye", list(range(36, 42))),
            ("left_eye", list(range(42, 48))),
            ("mouth", list(range(48, 68))),
        ]
    )

    # using 0 for external camera input
    cap = cv2.VideoCapture(0)

    if cap.isOpened():
        CHECK, frame = cap.read()
    else:
        CHECK = False

    time_stamp = True
    while CHECK:
        CHECK, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

        before_face = datetime.datetime.now()
        faces = detector(gray)
        after_face = datetime.datetime.now()

        for (i, face) in enumerate(faces):
            x1 = face.left()
            x2 = face.right()
            y1 = face.top()
            y2 = face.bottom()

            # draw the face bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            # show the face number
            cv2.putText(
                frame,
                "Face #{}".format(i + 1),
                (x1 - 10, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 255, 0),
                2,
            )

            before_landmarks = datetime.datetime.now()
            landmarks = predictor(gray, face)
            after_landmarks = datetime.datetime.now()

            # calculating the facial landmamrks
            landmark_keys = ["right_eye", "left_eye", "mouth"]
            required_landmarks = []
            for key in landmark_keys:
                required_landmarks.extend(FACIAL_LANDMARKS.get(key))

            # drawing the facial landmarks in the video
            for n in required_landmarks:
                x = landmarks.part(n).x
                y = landmarks.part(n).y
                cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

            calculated_mar = mouth_aspect_ratio(FACIAL_LANDMARKS["mouth"], landmarks)

            left_EAR = eye_aspect_ratio(FACIAL_LANDMARKS["left_eye"], landmarks)
            right_EAR = eye_aspect_ratio(FACIAL_LANDMARKS["right_eye"], landmarks)

            ear_both_eyes = (left_EAR + right_EAR) / 2

            result = loaded_model.predict([[ear_both_eyes, calculated_mar]])

            if result == 1:
                COUNTER += 1

                if COUNTER >= EAR_CONSECUTIVE_FRAMES:
                    if not ALARM_ON:
                        ALARM_ON = True

                        # creating new thread to play the alarm in background
                        audio_thread = threading.Thread(target=raise_alarm)
                        audio_thread.start()

                    cv2.putText(
                        frame,
                        "Drowsiness Alert!",
                        (10, 30),
                        cv2.FONT_HERSHEY_SIMPLEX,
                        0.5,
                        (0, 255, 0),
                        2,
                    )
                    # print("Drowsiness detected!")
            else:
                COUNTER = 0
                ALARM_ON = False

            cv2.putText(
                frame,
                "MAR: {:.2f}".format(calculated_mar),
                (300, 400),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

            cv2.putText(
                frame,
                "EAR: {:.2f}".format(ear_both_eyes),
                (300, 30),
                cv2.FONT_HERSHEY_SIMPLEX,
                0.5,
                (0, 0, 255),
                2,
            )

        cv2.namedWindow("Capturing")
        cv2.imshow("Capturing", frame)

        if time_stamp:
            logger("---{} seconds---".format(round((time.time() - start_time), 2)))
            logger("Model load: " + str(after_model_load - start))
            logger("Face detection: " + str(after_face - before_face))
            if len(faces) > 0:
                logger("Landmark detection: " + str(after_landmarks - before_landmarks))
            time_stamp = False

        key = cv2.waitKey(1)

        # Use q to close the detection
        if key == ord("q"):
            print("Ending the capture")
            break

    cv2.destroyAllWindows()
    cap.release()


if __name__ == "__main__":
    main()
