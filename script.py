
# pip install torch torchvision torchaudio --extra-index-url https://download.pytorch.org/whl/cu117
# pip install matplotlib
# pip install seaborn
# pip install tqdm
# pip install pyyaml
# python -m PyInstaller script.py

import gc
import torch
import numpy as np
import cv2
from PIL import Image
from PIL import ImageTk
import threading
import tkinter as tk
from tkinter import PhotoImage
import pandas as pd
import random
import time

model = torch.hub.load('ultralytics/yolov5', 'custom', path='yolov5/runs/train/results_100/weights/best.pt', force_reload=True)
model.eval()
print("Model fitted to exp8")


letter_list = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'I', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
letter_array = np.array(letter_list)
scores = [(0.8, "Perfect Score!", "#4eedc6"),    (0.5, "Well Done!", "#6fe798"),    (0.3, "Very Close", "#68d870"),    (0.1, "Getting There", "#9ae360"),    (0, "You will never see this message", "#fe7f73"),]
letter = ""
videoloop_stop = [False]

def random_letter():
    global letter, timer_label, running, start_time
    letter = random.choice(letter_array)

    running = True
    rand_label.config(text=letter)
    start_time = time.perf_counter()
    timer_label.config(text='5:00')
    timer_label.after(1000, count_down)

def change_letter():
    global letter
    letter = variable.get()
    rand_label.config(text=letter)

def count_down():
    global timer_label, running
    if running:
        current_time = int((time.perf_counter() - start_time) * 1000)
        remaining_time = 5000 - current_time
        if remaining_time > 0:
            seconds, milliseconds = divmod(remaining_time, 1000)
            timer_label.config(text='{:.2f}'.format(seconds + milliseconds/1000))
            timer_label.after(1, count_down)
        else:
            random_letter()

def stop_timer():
    global running
    running = False

def start_button_clicked(videoloop_stop):
    threading.Thread(target=videoLoop, args=(videoloop_stop,)).start()

def stop_button_clicked(videoloop_stop):
    videoloop_stop[0] = True

def show_image():
    popup = tk.Toplevel()
    popup.title("Letter Reference")

    image = PhotoImage(file="images\letters.gif")
    label = tk.Label(popup, image=image)
    label.image = image
    label.pack()

def show_CS():
    desc = tk.Toplevel()
    desc.title("Sign Descriptions")
    label_1 = tk.Label(desc, font=("", 10))
    with open("tips\cheat_sheet.txt", "r") as file:
        text = file.read()
    label_1.config(text=text)
    label_1.pack()
    desc.config(bg = "#8d9ee9")
    desc.geometry("600x600")

def update_labels(conf, name):
    name_label = tk.Label(root, text="", font=("", 9))
    name_label.place(x=50, y=450, width=120, height=50)
    conf_label = tk.Label(root, text="", font=("", 10))
    conf_label.place(x=200, y=450, width=100, height=50)
    for score, message, bg in scores:
        if conf >= score:
            name_label.config(text=(name, message), bg=bg)
            conf_label.config(text=("Score:", conf))
            break

    
def videoLoop(mirror=False):
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 300)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 300)

    # names_list = []
    # list_box = tk.Listbox(root, width=10, height=10)
    # list_box.pack(side="right")
    frame_rate=30

    while True:
        ret, frame = cap.read()
        results = model(frame)
        time.sleep(1/frame_rate)
        for i, row in results.pandas().xyxy[0].iterrows():
            name = (row['name']).upper()
            conf = round((row['confidence']), 1)
            if name == letter:
                update_labels(conf, name)
                # if conf > 0.79:
                #     names_list.append(name +": "+ str(conf))
                #     if len(names_list) > 10:
                #         names_list.pop(0)
                #     list_box.delete(0, tk.END)
                #     for item in names_list:
                #         list_box.insert(tk.END, item)    
        if mirror is True:
            frame = frame[:, ::-1]   

        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = Image.fromarray(image)
        image = ImageTk.PhotoImage(image)
        panel = tk.Label(image=image)
        panel.image = image
        panel.place(x=50, y=120)

        if videoloop_stop[0]:
            videoloop_stop[0] = False
            panel.destroy()
            cap.release()
            break

root = tk.Tk()
root.title("BSL Learning Tool")
root.config(bg = "#9b9fc8")
root.geometry("400x600+0+0")

# make a header and footer for the buttons to go in
footer = tk.Frame(root, height=75)
footer.config(bg = "#9b9fc8")
footer.pack(side="bottom", fill="x")
header = tk.Frame(root, height=75)
header.config(bg = "#9b9fc8")
header.pack(side="top", fill="x")
header2 = tk.Frame(root, height=50)
header2.config(bg = "#9b9fc8")
header2.pack(side="top", fill="x")
header3 = tk.Frame(root, height=20)
header3.config(bg = "#9b9fc8")
header3.pack(side="top", fill="x")

# display prompt for which letter to sign
rand_label = tk.Label(header3, font=("", 15))
rand_label.config(bg="#9b9fc8")
rand_label.pack(side="left", padx=10)

# display the time left until next letter switch
timer_label = tk.Label(header3, font=("", 10))
timer_label.config(bg = "#9b9fc8")
timer_label.pack(side="left", padx=10)

# drop down menu so users can select a specific letter
variable = tk.StringVar(header2)
variable.set("A")
choices = letter_array
option = tk.OptionMenu(header2, variable, *choices)
option.config(bg="#5fbac2")
option.pack(side="left", padx=10)

# button to change the letter to the users input
change_letter_button = tk.Button(header2, text="Change Letter", command=change_letter)
change_letter_button.config(bg="#398f95", foreground="White")
change_letter_button.pack(side="left", padx=10)

# button to change the prompt letter and start the timer
letter_button = tk.Button(header2, text="Start Timer", command=random_letter)
letter_button.config(bg = "#10a242", foreground="white")
letter_button.pack(side="left", padx=10)

# Button to stop the timer 
time_stop = tk.Button(header2, text="Stop Timer", command=stop_timer)
time_stop.config(bg = "#ab0e19", foreground="white")
time_stop.pack(side="left", padx=10)

# button to display the image
img_button = tk.Button(header, text="Reference Image", bg="#fff", font=("", 15), command=show_image)
img_button.config(bg="#393d68", foreground="white")
img_button.pack(side="left", fill="both", expand=True)

# button to show how to do the signs
img_button = tk.Button(header, text="Cheat Sheet", bg="#fff", font=("", 15), command=show_CS)
img_button.config(bg="#393d68", foreground="white")
img_button.pack(side="left", fill="both", expand=True)

# button to start the camera
start_button = tk.Button(footer, text="Start Camera", font=("", 15), command=lambda: start_button_clicked(videoloop_stop))
start_button.config(bg="#5cc33c")
start_button.pack(side="left", fill="both", expand=True)

# button to stop the camera (at that frame)
stop_button = tk.Button(footer, text="Freeze Frame", font=("", 15), command=lambda: stop_button_clicked(videoloop_stop))
stop_button.config(bg="#d8608e")
stop_button.pack(side="left", fill="both", expand=True)


root.mainloop()