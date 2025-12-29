import subprocess
import tkinter as tk
import pyautogui as pg
import pyscreenshot
import webbrowser
from tkinter import scrolledtext
import components.main_window as r
from tkinter import messagebox
from tkinter import ttk

                    
class TutorialAndScreenshot:
    def __init__(self):
        self.tutorial_window = None
        self.button_frame = ttk.Frame(r.root,padding=10,height=20)
        self.button_frame.pack(side="left",fill="x",pady=(0,10))
        self.screenshot_button = tk.Button(self.button_frame,text = "TAKE SCREENSHOT",font="Arial,8",command=self.screenshot_window_func)
        self.screenshot_button.pack(side="left",fill="x")
        self.tutorial_button = tk.Button(self.button_frame,text = "TUTORIAL", font="Arial,8",command=self.tutorial)
        self.tutorial_button.pack(side="left",fill="x")
    def screenshot_window_func(self):
        try:
            subprocess.Popen("SnippingTool.exe")
        except Exception:
            messagebox.showerror("ERROR","Can not find SnippingTool.exe,please take screenshot manually!")
    def tutorial(self):
        webbrowser.open("https://www.youtube.com/watch?v=dQw4w9WgXcQ&list=RDdQw4w9WgXcQ&start_radio=1")
        




