import tkinter as tk
from tkinter import *
import os, cv2
import shutil
import csv
import numpy as np
from PIL import ImageTk, Image
import pandas as pd
import datetime
import time
import tkinter.ttk as tkk
import tkinter.font as font

haarcasecade_path = "haarcascade_frontalface_default.xml"

trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"
trainimage_path = "./TrainingImage"
studentdetail_path = "./StudentDetails/studentdetails.csv"

attendance_path = "Attendance"


def subjectChoose(text_to_speech):

    def FillAttendance():

        sub = tx.get()
        now = time.time()
        future = now + 25

        if sub == "":
            text_to_speech("Please enter the subject name!!!")

        else:
            try:

                recognizer = cv2.face.LBPHFaceRecognizer_create()

                try:
                    recognizer.read(trainimagelabel_path)
                except:
                    e = "Model not found, please train model"
                    Notifica.configure(text=e)
                    text_to_speech(e)
                    return

                facecasCade = cv2.CascadeClassifier(haarcasecade_path)
                df = pd.read_csv(studentdetail_path)

                cam = cv2.VideoCapture(0)
                font = cv2.FONT_HERSHEY_SIMPLEX

                col_names = ["Enrollment", "Name"]
                attendance = pd.DataFrame(columns=col_names)

                while True:

                    ret, im = cam.read()
                    gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)

                    faces = facecasCade.detectMultiScale(gray, 1.2, 5)

                    for (x, y, w, h) in faces:

                        Id, conf = recognizer.predict(gray[y:y + h, x:x + w])

                        if conf < 70:

                            Subject = tx.get()

                            ts = time.time()

                            date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")

                            timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                            aa = df.loc[df["Enrollment"] == Id]["Name"].values[0]

                            tt = str(Id) + "-" + str(aa)

                            attendance.loc[len(attendance)] = [Id, aa]

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 255, 0), 3)

                            cv2.putText(im, tt, (x, y - 10), font, 0.8, (255, 255, 0), 2)

                        else:

                            cv2.rectangle(im, (x, y), (x + w, y + h), (0, 0, 255), 3)

                            cv2.putText(im, "Unknown", (x, y - 10), font, 0.8, (0, 0, 255), 2)

                    if time.time() > future:
                        break

                    attendance = attendance.drop_duplicates(["Enrollment"], keep="first")

                    cv2.imshow("Filling Attendance...", im)

                    if cv2.waitKey(30) & 0xFF == 27:
                        break

                ts = time.time()

                attendance[date] = 1

                date = datetime.datetime.fromtimestamp(ts).strftime("%Y-%m-%d")
                timeStamp = datetime.datetime.fromtimestamp(ts).strftime("%H:%M:%S")

                Hour, Minute, Second = timeStamp.split(":")

                path = os.path.join(attendance_path, sub)

                if not os.path.exists(path):
                    os.makedirs(path)

                fileName = f"{path}/{sub}_{date}_{Hour}-{Minute}-{Second}.csv"

                attendance = attendance.drop_duplicates(["Enrollment"], keep="first")

                attendance.to_csv(fileName, index=False)

                m = "Attendance Filled Successfully for " + sub
                Notifica.configure(text=m)

                text_to_speech(m)

                cam.release()
                cv2.destroyAllWindows()

            except:

                text_to_speech("No Face found for attendance")
                cv2.destroyAllWindows()


    def Attf():

        sub = tx.get()

        if sub == "":
            text_to_speech("Please enter the subject name!!!")

        else:
            os.startfile(f"Attendance\\{sub}")


    # ================= WINDOW =================

    subject = Tk()

    subject.title("Subject Selection")

    subject.geometry("600x350")

    subject.resizable(False, False)

    subject.configure(bg="#121212")



    # ================= HEADER =================

    header = Frame(subject, bg="#0f3460", height=70)

    header.pack(fill=X)

    title = Label(
        header,
        text="Select Subject for Attendance",
        bg="#0f3460",
        fg="white",
        font=("Helvetica", 22, "bold")
    )

    title.pack(pady=15)



    # ================= INPUT =================

    main_frame = Frame(subject, bg="#121212")

    main_frame.pack(pady=40)

    sub = Label(
        main_frame,
        text="Subject Name",
        font=("Helvetica", 14, "bold"),
        bg="#121212",
        fg="white"
    )

    sub.grid(row=0, column=0, padx=10, pady=10)

    tx = Entry(
        main_frame,
        width=20,
        font=("Helvetica", 16),
        bg="#1f1f1f",
        fg="white",
        insertbackground="white",
        bd=3
    )

    tx.grid(row=0, column=1, padx=10)



    # ================= BUTTONS =================

    button_frame = Frame(subject, bg="#121212")

    button_frame.pack(pady=30)

    fill_a = Button(
        button_frame,
        text="Fill Attendance",
        command=FillAttendance,
        font=("Helvetica", 14, "bold"),
        bg="#16213e",
        fg="white",
        width=15,
        bd=3
    )

    fill_a.grid(row=0, column=0, padx=20)

    attf = Button(
        button_frame,
        text="Check Sheets",
        command=Attf,
        font=("Helvetica", 14, "bold"),
        bg="#e94560",
        fg="white",
        width=15,
        bd=3
    )

    attf.grid(row=0, column=1, padx=20)



    # ================= NOTIFICATION =================

    Notifica = Label(
        subject,
        text="",
        bg="#121212",
        fg="yellow",
        font=("Helvetica", 12, "bold")
    )

    Notifica.pack(pady=10)

    subject.mainloop()