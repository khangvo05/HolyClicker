import threading
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