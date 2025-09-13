import components.main_window as r
import tkinter as tk
import pyautogui as pg
from tkinter import ttk
class Coordinate:
    def __init__(self):
        self.coordinate_frame = ttk.Frame( r.root,borderwidth=5,width=10,height=40)
        self.coordinate_frame.pack(side="top",anchor="w",pady=10)
        self.coordinate_label = tk.Label(self.coordinate_frame,font="Arial")
        self.get_constant_coordination()
        self.coordinate_label.pack()
        r.root.bind("<F1>",self.copy)

    def get_constant_coordination(self):
        if True and self.coordinate_label.cget("text") != "Copied!":
            self.coordinate_label.configure(text = 'Coordinate: {} | {}\nPress F1 to copy!'.format(pg.position().x,pg.position().y))
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
       