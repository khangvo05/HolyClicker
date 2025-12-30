import threading
<<<<<<< HEAD
import tkinter as tk
from tkinter import ttk, messagebox
import pyautogui as pg
import time
import keyboard
import components.main_window as r
import json
DB_SETTING = "setting.json"
class SimpleAutoClicking:
    def __init__(self):
        # Frame Setup
        self.autoclick_frame = ttk.Frame(r.root, padding=10)
        self.autoclick_frame.pack(side=tk.TOP, fill=tk.X)
        
        # 1. Times Input
        row1 = ttk.Frame(self.autoclick_frame)
        row1.pack(fill=tk.X, pady=2)
        tk.Label(row1, text="Times:", width=10, anchor="w").pack(side=tk.LEFT)
        self.num_entry = tk.Entry(row1, width=15)
        self.num_entry.pack(side=tk.LEFT)
        self.num_entry.insert(0, "10") # Default

        # 2. Coordinates Input
        row2 = ttk.Frame(self.autoclick_frame)
        row2.pack(fill=tk.X, pady=2)
        tk.Label(row2, text="X, Y:", width=10, anchor="w").pack(side=tk.LEFT)
        self.coord_entry = tk.Entry(row2, width=15)
        self.coord_entry.pack(side=tk.LEFT)

        # 3. Interval Input
        row3 = ttk.Frame(self.autoclick_frame)
        row3.pack(fill=tk.X, pady=2)
        tk.Label(row3, text="Interval(s):", width=10, anchor="w").pack(side=tk.LEFT)
        self.interval_entry = tk.Entry(row3, width=15)
        self.interval_entry.pack(side=tk.LEFT)
        self.interval_entry.insert(0, "0.1")

        # 4. Buttons & Info
        self.start_btn = tk.Button(
            self.autoclick_frame, 
            text="Start Auto Click", 
            command=self.start_clicking,
            bg="#d1ecf1"
        )
        self.start_btn.pack(pady=5)
        
        stop_button = "q"
        try:
            with open(DB_SETTING,"r") as f:
                stop_button = json.load(f)[0]["stop"]
        except:
            pass
        keyboard.add_hotkey('{}'.format(stop_button.upper()), self.stop)

        self.status_lbl = tk.Label(
            self.autoclick_frame, 
            text="Press '{0}' to stop running tasks".format(stop_button), 
            fg="gray", font=("Arial", 8)
        )
        self.status_lbl.pack()

        self.stop_event = threading.Event()
        # Bind Q to stop this specific module as well



    def stop(self):
        self.stop_event.set()

    def start_clicking(self):
        # Validate Inputs
        try:
            times = int(self.num_entry.get())
            interval = float(self.interval_entry.get())
            raw_coords = self.coord_entry.get().split(',')
            
            if len(raw_coords) == 2:
                x, y = int(raw_coords[0]), int(raw_coords[1])
            else:
                return
                
        except ValueError:
            self.status_lbl.config(text="Error: Invalid Numbers", fg="red")
            return

        # Reset stop flag
        self.stop_event.clear()
        
        # Start Thread
        t = threading.Thread(
            target=self._clicking_logic, 
            args=(x, y, times, interval), 
            daemon=True
        )
        t.start()

    def _clicking_logic(self, x, y, times, interval):
        self.status_lbl.config(text="Running...", fg="green")
        
        # Move to start position
        pg.moveTo(x, y)
        
        count = 0
        while count < times and not self.stop_event.is_set():
            pg.click()
            count += 1
            time.sleep(interval)
            
        if self.stop_event.is_set():
            self.status_lbl.config(text="Stopped!", fg="red")
        else:
            self.status_lbl.config(text="Finished.", fg="blue")
=======
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
            interval = float(self.autoclick_interval_entry.get())
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
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
