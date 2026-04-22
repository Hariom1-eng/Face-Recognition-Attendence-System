import csv
import os, cv2
import numpy as np
import pandas as pd
import datetime
import time

# take Image of user
def TakeImage(l1, l2, haarcasecade_path, trainimage_path, message, err_screen, text_to_speech):
    
    if (l1 == "") and (l2 == ""):
        t = 'Please Enter your Enrollment Number and Name.'
        text_to_speech(t)

    elif l1 == '':
        t = 'Please Enter your Enrollment Number.'
        text_to_speech(t)

    elif l2 == "":
        t = 'Please Enter your Name.'
        text_to_speech(t)

    else:
        try:
            cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
            detector = cv2.CascadeClassifier(haarcasecade_path)

            Enrollment = l1
            Name = l2
            sampleNum = 0

            path = os.path.join(os.getcwd(), "TrainingImage")
            os.makedirs(path, exist_ok=True)

            while True:
                ret, img = cam.read()

                # ✅ IMPORTANT FIX (no crash)
                if not ret or img is None:
                    print("Camera issue, try again...")
                    continue

                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.3, 5)

                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (255, 0, 0), 2)

                    sampleNum += 1

                    cv2.imwrite(
                        f"{path}/{Name}_{Enrollment}_{sampleNum}.jpg",
                        gray[y:y + h, x:x + w]
                    )

                    cv2.imshow("Frame", img)

                if cv2.waitKey(1) & 0xFF == ord("q"):
                    break
                elif sampleNum > 50:
                    break

            cam.release()
            cv2.destroyAllWindows()

            # Save student details
            row = [Enrollment, Name]
            with open("StudentDetails/studentdetails.csv", "a+", newline="") as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)

            res = "Images Saved for ER No: " + Enrollment + " Name: " + Name
            message.configure(text=res)
            text_to_speech(res)

        except FileExistsError:
            text_to_speech("Student Data already exists")