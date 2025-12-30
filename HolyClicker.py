import pyautogui as pg
<<<<<<< HEAD
import components.coordinate as coordinate
import components.scripting as scripting
import components.simple_auto_clicking as simple_auto_clicking
import components.main_window as r
=======
from components.main_window import root
import components.coordinate as coordinate
import components.scripting as scripting
import components.simple_auto_clicking as simple_auto_clicking
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
import components.tutorial_and_screenshot as tutorial_and_screenshot

#Author: Vo An Khang
class HolyClicker:
    def __init__(self):
<<<<<<< HEAD
=======
        #Built-in screenshot taker for image handling
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
        coordinate.Coordinate()
        simple_auto_clicking.SimpleAutoClicking()
        scripting.Scripting()
        tutorial_and_screenshot.TutorialAndScreenshot()

HolyClicker()
<<<<<<< HEAD
r.root.mainloop()


=======
root.mainloop()
>>>>>>> 358525b105fd275ed0745680f6162683843288f4
