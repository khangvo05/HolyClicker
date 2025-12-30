import pyautogui as pg
import components.coordinate as coordinate
import components.scripting as scripting
import components.simple_auto_clicking as simple_auto_clicking
import components.main_window as r
import components.tutorial_and_screenshot as tutorial_and_screenshot

#Author: Vo An Khang
class HolyClicker:
    def __init__(self):
        coordinate.Coordinate()
        simple_auto_clicking.SimpleAutoClicking()
        scripting.Scripting()
        tutorial_and_screenshot.TutorialAndScreenshot()

HolyClicker()
r.root.mainloop()


