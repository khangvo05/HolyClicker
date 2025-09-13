import threading
from threading import Thread
from tkinter import ttk, messagebox
import components.main_window as r
import tkinter as tk
import pyautogui as pg
import time
import keyboard
class SimpleAutoClicking:
    def __init__(self):
        self.autoclick_frame = ttk.Frame(r.root)
        self.autoclick_frame.pack(expand=True,side=tk.TOP,anchor=tk.W)
        self.num_frame = ttk.Frame(self.autoclick_frame)
        self.num_frame.pack(fill=tk.X,pady=(0,5))
        self.autoclick_num_entry = tk.Entry(self.num_frame,width=10,font=("Arial",11))
        self.autoclick_num_entry.pack(side=tk.LEFT)
        self.num_time = tk.Label(self.num_frame, text="Times", font=("Arial", 11))
        self.num_time.pack(side=tk.LEFT)

        self.coordinate_frame = ttk.Frame(self.autoclick_frame)
        self.coordinate_frame.pack(fill=tk.X,pady=5)
        self.autoclick_coordinate_entry = tk.Entry(self.coordinate_frame,width=10,font = ("Arial",11))
        self.autoclick_coordinate_entry.pack(side=tk.LEFT)
        self.coordinate_text = tk.Label(self.coordinate_frame,text="Coordinate",font=("Arial",11))
        self.coordinate_text.pack(side=tk.LEFT)

        self.interval_frame = ttk.Frame(self.autoclick_frame)
        self.interval_frame.pack(fill=tk.X,pady=5)
        self.autoclick_interval_entry = tk.Entry(self.interval_frame,width=10,font=("Arial",11))
        self.autoclick_interval_entry.pack(side=tk.LEFT)
        self.interval_label = tk.Label(self.interval_frame,text="Interval(s)",font=("Arial",11))
        self.interval_label.pack(side=tk.LEFT)

        self.autoclick_button = tk.Button(self.autoclick_frame,text = "Auto Click!",command=self.simple_autoclick,font=("Arial",11))
        self.autoclick_button.pack(side="left")
        self.error_label = tk.Label(self.autoclick_frame,text = "PRESS Q TO CANCEL ANY AUTO CLICKING")
        self.error_label.pack()
    def simple_autoclick(self):
        try:
            num = int(self.autoclick_num_entry.get())
            coordinate = self.autoclick_coordinate_entry.get().split(",")
            coordinate[0] = int(coordinate[0])
            coordinate[1] = int(coordinate[1])
            pg.moveTo(coordinate[0],coordinate[1])
            count = 0
            self.flag_stop = threading.Event()
            check_stop = threading.Thread(target=self.stop_clicking,daemon=True,args=[interval])
            check_stop.start()
            while count < num and not self.flag_stop.is_set():
                count+=1
                pg.click()
                time.sleep(interval)
            self.flag_stop.set()
        except Exception as e:
            self.error_label.configure(text = "PLEASE FILL ALL ENTRIES THE RIGHT WAY")
    def stop_clicking(self,interval):
        while not self.flag_stop.is_set():
            if keyboard.is_pressed("q"):
                self.flag_stop.set()
                messagebox.showinfo(message="Cancelled!")
                break
            time.sleep(interval)