import subprocess
import tkinter as tk
import pyautogui as pg
import pyscreenshot
from tkinter import scrolledtext
import components.main_window as r
from tkinter import messagebox
from tkinter import ttk


HEADING_LIST = ["How to use","Importing","Interval between each command","//","clickX,Y","clickX,Y,T","clickIMG.PNG,COLOR,REGION","waitTIME","waituntilTIME","typeTEXT","pressBUTTON","clickdownBUTTON","releaseBUTTON","mousedownX,Y,OPTION","mouseupX,Y,OPTION","dragToX,Y,OPTION,t","listenIMG.PNG,S,INTERVAL,N,TIME,COLOR,REGION","randomcommandN,UNIFORM","randomcommandN,P1,...,PN","randomtypeFILE.*,DELETE","repeatN:"]
DESCRIPTION_LIST = ['''After open the scripting window, click ADD to add new entries. Each entry only contains one command. Your script will be executed sequentially.
''',
                    '''To import your own scripts, the list of scripts you want to import has to follow this format :
[{"id" : INTEGER, "name" : STRING, "command" : LIST},
...]
Those scripts will be appended into the current list.''',
"In the Editor window, INTERVAL is the sleep time between each command",
                    "Use this to comment on your script. This command also has to be used on a separate entry.",
                    "Move the cursor to coordinate X, Y",
                    '''Click the cursor at coordinate X,Y T times. If T is not provided, the cursor will only be clicked 1 times.
T (Optional): positive integer ( ≥ 1)
X,Y : Coordinate with respect to the boundary of your monitor.''',
                    '''Click at the center of img.png.
COLOR is whether you want to find the image with color accuracy or not. Without color accuracy (false),the performance will be improved. 
COLOR: true | false
REGION is the region on the screen you want to search for the image. You should provide four integers,the first two integers are the coordinate of the top left corner of the area, and the next two are the coordinate of the bottom right corner of the area. This parameter helps improving performance. This parameter is OPTIONAL. 
REGION (Optional): (x1,y1,x2,y2)
img.png should be presented in the same directory with the .exe file''',
                    '''Wait TIME seconds.
X > 0 and X is divisible by 0.1)''',
                    '''Wait until TIME in the same day. TIME format is hh:mm.
Example: 06:15, 18:20''',
                    '''Type TEXT.''',
                    '''Press and release BUTTON.''',
                    '''Press down BUTTON.''',
                    '''Release BUTTON.''',
                    '''Press down the mouse at coordinate X Y.
OPTION: right,left and middle.''',
                    '''Release the mouse at position with coordinate X and Y with OPTION.''',
                    '''Drag the mouse to position  with coordinate X and Y, while holding down BUTTON in t seconds
t ≥ 0''',
                    '''Start looking for img.png on the monitor for S seconds.If found, execute the next N commands (next N entries).
INTERVAL indicates the sleep time between each time the app look for img.png. Lower INTERVAL value yields better sensitivity but require more resource.
TIME is the maximum number of time the next N entries will be executed if IMG.PNG is found.
COLOR and REGION are the same with Cimg.png,COLOR,REGION.
This command can be run in parallel.''',
                    '''Randomly execute one of the next N commands, following uniform distribution''',
                    '''Randomly execute one of the next N commands, following custom probability distribution, (P1 + P2 + ... + PN = 1)''',
                    '''Randomly type one of the lines in the FILE.* . This file should be of text file format (.docx,.doc,.txt,...)
DELETE : true | false is an optional parameter. Provide it if you want to delete the typed line in the text file after it was typed.
                    ''',
                    '''Repeat the next section of commands N times. The section stop with the "end" command.
Example usage:
repeat2:
click100,100
pressf5
end
click200,200
...'''
                    ]
class TutorialAndScreenshot:
    def __init__(self):
        self.tutorial_window = None
        self.button_frame = ttk.Frame(r.root,padding=10,height=20)
        self.button_frame.pack(side="left",fill="x",pady=(0,10))
        self.screenshot_button = tk.Button(self.button_frame,text = "TAKE SCREENSHOT",font="Arial,8",command=self.screenshot_window_func)
        self.screenshot_button.pack(side="left",padx=(0,15))
        self.tutorial_button = tk.Button(self.button_frame,text = "TUTORIAL", font=("Arial",12),command=self.tutorial)
        self.tutorial_button.pack(side="right")
    def screenshot_window_func(self):
        try:
            subprocess.Popen("SnippingTool.exe")
        except Exception:
            messagebox.showerror("ERROR","Can not find SnippingTool.exe,please take screenshot manually!")
    def tutorial(self):
        self.tutorial_window = tk.Toplevel(r.root)
        self.tutorial_window.title("Tutorial")
        self.tutorial_window.geometry("700x650")
        main_frame = tk.Frame(self.tutorial_window)
        main_frame.pack(fill="both", expand=True)
        title = tk.Label(main_frame, text = "Scripting Tutorial",font=("Arial", 18, "bold"))
        textarea = scrolledtext.ScrolledText(main_frame, width=400, height=300,font=("Arial", 18, "bold"))
        #Configure font of each part in the scrolltext
        def style_configure():
            textarea.tag_configure("heading",font=("Arial", 14, "bold"),foreground="#3498db")
            textarea.tag_configure("description",font=("Arial", 12),foreground="#2c3e50")
            textarea.tag_configure("title",font=("Arial", 18, "bold"),foreground="#2c3e50")
            textarea.tag_configure("uncategorized tutorial",font=("Arial", 14, "bold"),foreground="#2d3e50")
        def add_text():
            textarea.insert(tk.INSERT,"GUIDE TO SCRIPTING\n","title")
            for i in range(0,3):
                textarea.insert(tk.INSERT,"• " +HEADING_LIST[i]+"\n","uncategorized tutorial")
                textarea.insert(tk.INSERT,DESCRIPTION_LIST[i]+"\n\n","description")
            for i in range(3,len(HEADING_LIST)):
                textarea.insert(tk.INSERT,"• " +HEADING_LIST[i]+"\n","heading")
                textarea.insert(tk.INSERT,DESCRIPTION_LIST[i]+"\n\n","description")


        add_text()
        style_configure()
        textarea.configure(state="disabled")
        textarea.pack(fill="both", expand=True)




