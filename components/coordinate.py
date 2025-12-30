import components.main_window as r
import tkinter as tk
import pyautogui as pg
from tkinter import ttk
import json
DB_SETTING = "setting.json"
class Coordinate:
    def __init__(self):
        self.coordinate_frame = ttk.Frame( r.root,borderwidth=5,width=10,height=40)
        self.coordinate_frame.pack(side="top",anchor="w",pady=10,fill="x")
        self.coordinate_label = tk.Label(self.coordinate_frame,font="Arial,12")

        self.copy_button = "f1"
        try:
            with open(DB_SETTING,"r") as f:
                self.copy_button = json.load(f)[0]["copy"]
        except:
            pass
            
        self.get_constant_coordination()
        self.coordinate_label.pack()


        r.root.bind("<{}>".format(self.copy_button.upper()),self.copy)

    def get_constant_coordination(self):
        if True and self.coordinate_label.cget("text") != "Copied!":
            self.coordinate_label.configure(text = 'Coordinate: {} | {}\nPress {} to copy!'.format(pg.position().x,pg.position().y,self.copy_button))
            self.coordinate_label.after(100, self.get_constant_coordination)
    def copy(self,event):
        text = '{},{}'.format(pg.position().x,pg.position().y)
        r.root.clipboard_clear()
        r.root.clipboard_append(text)
        r.root.update()
        self.coordinate_label.configure(text = "Copied!")
        self.coordinate_label.after(250,self.copy_over)

    def copy_over(self):
        self.coordinate_label.configure(text = "")
        self.get_constant_coordination()
       