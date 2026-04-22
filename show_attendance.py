import pandas as pd
from glob import glob
import os
import tkinter
import csv
import tkinter as tk
from tkinter import *

def subjectchoose(text_to_speech):

    def calculate_attendance():

        Subject = tx.get()

        if Subject == "":
            text_to_speech("Please enter the subject name.")
            return

        filenames = glob(f"Attendance\\{Subject}\\{Subject}*.csv")

        df_list = []

        for file in filenames:
            df_list.append(pd.read_csv(file))

        newdf = pd.concat(df_list, ignore_index=True)

        newdf = newdf.drop_duplicates(subset=["Enrollment"], keep="first")

        for i in range(len(newdf)):

            attendance_mean = newdf.iloc[i, 2:-1].mean()

            if pd.isna(attendance_mean):
                percentage = 0
            else:
                percentage = int(round(attendance_mean * 100))

            newdf.loc[i, "Attendance"] = f"{percentage}%"

        newdf.to_csv(f"Attendance\\{Subject}\\attendance.csv", index=False)

        root = tkinter.Tk()
        root.title("Attendance of " + Subject)
        root.geometry("700x400")
        root.configure(bg="#121212")

        cs = f"Attendance\\{Subject}\\attendance.csv"

        with open(cs) as file:

            reader = csv.reader(file)

            r = 0

            for col in reader:

                c = 0

                for row in col:

                    label = tkinter.Label(
                        root,
                        width=12,
                        height=1,
                        fg="white",
                        font=("Helvetica", 12, "bold"),
                        bg="#1f1f1f",
                        text=row,
                        relief=tkinter.RIDGE,
                        bd=2
                    )

                    label.grid(row=r, column=c, padx=2, pady=2)

                    c += 1

                r += 1

        root.mainloop()



    # ================= WINDOW =================

    subject = Tk()

    subject.title("View Attendance")

    subject.geometry("620x360")

    subject.resizable(False, False)

    subject.configure(bg="#121212")



    # ================= HEADER =================

    header = Frame(subject, bg="#0f3460", height=70)

    header.pack(fill=X)

    title = Label(
        header,
        text="Select Subject to View Attendance",
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



    def Attf():

        sub = tx.get()

        if sub == "":
            text_to_speech("Please enter the subject name!!!")

        else:
            os.startfile(f"Attendance\\{sub}")



    view_btn = Button(
        button_frame,
        text="View Attendance",
        command=calculate_attendance,
        font=("Helvetica", 14, "bold"),
        bg="#16213e",
        fg="white",
        width=15,
        bd=3
    )

    view_btn.grid(row=0, column=0, padx=20)



    sheet_btn = Button(
        button_frame,
        text="Check Sheets",
        command=Attf,
        font=("Helvetica", 14, "bold"),
        bg="#e94560",
        fg="white",
        width=15,
        bd=3
    )

    sheet_btn.grid(row=0, column=1, padx=20)



    subject.mainloop()