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
import tkinter.font as font
import pyttsx3

# project module
import show_attendance
import takeImage
import trainImage
import automaticAttedance


def text_to_speech(user_text):
    engine = pyttsx3.init()
    engine.say(user_text)
    engine.runAndWait()


haarcasecade_path = "haarcascade_frontalface_default.xml"

trainimagelabel_path = "./TrainingImageLabel/Trainner.yml"

trainimage_path = "./TrainingImage"
if not os.path.exists(trainimage_path):
    os.makedirs(trainimage_path)

studentdetail_path = "./StudentDetails/studentdetails.csv"

attendance_path = "Attendance"


# MAIN WINDOW
window = Tk()
window.title("CLASS VISION - Face Recognition Attendance")
window.geometry("1280x720")
window.configure(bg="#121212")
window.resizable(False, False)


def del_sc1():
    sc1.destroy()


# error message
def err_screen():
    global sc1
    sc1 = tk.Tk()
    sc1.geometry("400x110")
    sc1.title("Warning!!")
    sc1.configure(background="#1c1c1c")
    sc1.resizable(0, 0)

    tk.Label(
        sc1,
        text="Enrollment & Name required!!!",
        fg="yellow",
        bg="#1c1c1c",
        font=("Verdana", 16, "bold"),
    ).pack()

    tk.Button(
        sc1,
        text="OK",
        command=del_sc1,
        fg="yellow",
        bg="#333333",
        width=9,
        height=1,
        activebackground="red",
        font=("Verdana", 16, "bold"),
    ).place(x=110, y=50)


def testVal(inStr, acttyp):
    if acttyp == "1":
        if not inStr.isdigit():
            return False
    return True


# HEADER
header = Frame(window, bg="#0f3460", height=80)
header.pack(fill=X)

title = Label(
    header,
    text="CLASS VISION",
    bg="#0f3460",
    fg="white",
    font=("Helvetica", 30, "bold"),
)
title.pack(pady=10)

subtitle = Label(
    window,
    text="Face Recognition Attendance System",
    bg="#121212",
    fg="#00e5ff",
    font=("Helvetica", 18),
)
subtitle.pack(pady=10)


# IMAGES
ri = Image.open("UI_Image/register.png")
r_img = ImageTk.PhotoImage(ri)

ai = Image.open("UI_Image/attendance.png")
a_img = ImageTk.PhotoImage(ai)

vi = Image.open("UI_Image/verifyy.png")
v_img = ImageTk.PhotoImage(vi)


# DASHBOARD IMAGE FRAME
dashboard = Frame(window, bg="#121212")
dashboard.pack(pady=60)

label1 = Label(dashboard, image=r_img, bg="#121212")
label1.grid(row=0, column=0, padx=80)

label3 = Label(dashboard, image=v_img, bg="#121212")
label3.grid(row=0, column=1, padx=80)

label2 = Label(dashboard, image=a_img, bg="#121212")
label2.grid(row=0, column=2, padx=80)


# ==========================
# TAKE IMAGE WINDOW
# ==========================
def TakeImageUI():

    ImageUI = Tk()
    ImageUI.title("Take Student Image..")
    ImageUI.geometry("780x480")
    ImageUI.configure(background="#1c1c1c")
    ImageUI.resizable(0, 0)

    titl = tk.Label(
        ImageUI,
        text="Register Your Face",
        bg="#1c1c1c",
        fg="green",
        font=("Verdana", 30, "bold"),
    )
    titl.place(x=220, y=20)

    a = tk.Label(
        ImageUI,
        text="Enter the details",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 20, "bold"),
    )
    a.place(x=250, y=90)

    # Enrollment
    lbl1 = tk.Label(
        ImageUI,
        text="Enrollment No",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 14),
    )
    lbl1.place(x=120, y=150)

    txt1 = tk.Entry(
        ImageUI,
        width=20,
        validate="key",
        bg="#333333",
        fg="yellow",
        font=("Verdana", 16),
    )
    txt1.place(x=300, y=150)

    txt1["validatecommand"] = (txt1.register(testVal), "%P", "%d")

    # Name
    lbl2 = tk.Label(
        ImageUI,
        text="Name",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 14),
    )
    lbl2.place(x=120, y=210)

    txt2 = tk.Entry(
        ImageUI,
        width=20,
        bg="#333333",
        fg="yellow",
        font=("Verdana", 16),
    )
    txt2.place(x=300, y=210)

    lbl3 = tk.Label(
        ImageUI,
        text="Notification",
        bg="#1c1c1c",
        fg="yellow",
        font=("Verdana", 14),
    )
    lbl3.place(x=120, y=270)

    message = tk.Label(
        ImageUI,
        text="",
        width=30,
        bg="#333333",
        fg="yellow",
        font=("Verdana", 12, "bold"),
    )
    message.place(x=300, y=270)

    def take_image():
        l1 = txt1.get()
        l2 = txt2.get()

        takeImage.TakeImage(
            l1,
            l2,
            haarcasecade_path,
            trainimage_path,
            message,
            err_screen,
            text_to_speech,
        )

        txt1.delete(0, "end")
        txt2.delete(0, "end")

    takeImg = tk.Button(
        ImageUI,
        text="Take Image",
        command=take_image,
        font=("Verdana", 14, "bold"),
        bg="#16213e",
        fg="white",
        width=12,
    )
    takeImg.place(x=180, y=350)

    def train_image():

        trainImage.TrainImage(
            haarcasecade_path,
            trainimage_path,
            trainimagelabel_path,
            message,
            text_to_speech,
        )

    trainImg = tk.Button(
        ImageUI,
        text="Train Image",
        command=train_image,
        font=("Verdana", 14, "bold"),
        bg="#16213e",
        fg="white",
        width=12,
    )
    trainImg.place(x=400, y=350)


# ==========================
# BUTTON FUNCTIONS
# ==========================
def automatic_attedance():
    automaticAttedance.subjectChoose(text_to_speech)


def view_attendance():
    show_attendance.subjectchoose(text_to_speech)


# ==========================
# BUTTON FRAME
# ==========================
button_frame = Frame(window, bg="#121212")
button_frame.pack(pady=40)

btn1 = Button(
    button_frame,
    text="Register Student",
    command=TakeImageUI,
    font=("Helvetica", 16, "bold"),
    bg="#16213e",
    fg="white",
    width=18,
)
btn1.grid(row=0, column=0, padx=40)

btn2 = Button(
    button_frame,
    text="Take Attendance",
    command=automatic_attedance,
    font=("Helvetica", 16, "bold"),
    bg="#16213e",
    fg="white",
    width=18,
)
btn2.grid(row=0, column=1, padx=40)

btn3 = Button(
    button_frame,
    text="View Attendance",
    command=view_attendance,
    font=("Helvetica", 16, "bold"),
    bg="#16213e",
    fg="white",
    width=18,
)
btn3.grid(row=0, column=2, padx=40)


# EXIT BUTTON
exit_btn = Button(
    window,
    text="EXIT",
    command=quit,
    font=("Helvetica", 16, "bold"),
    bg="#e94560",
    fg="white",
    width=18,
)
exit_btn.pack(pady=20)

window.mainloop()