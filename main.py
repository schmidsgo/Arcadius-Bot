from ctypes.wintypes import PLARGE_INTEGER
from pyautogui import click, press, keyDown, keyUp
import numpy as np
import cv2
import mss

castImg = cv2.imread('Assets/clickToCast.png', cv2.IMREAD_UNCHANGED)
testImg = cv2.imread('Assets/test.png', cv2.IMREAD_UNCHANGED)

class Bot():
    def __intit__(self):
        self.stc = mss.mss()

    

class Bot:
    def __init__(self):
        self.stc = mss.mss()
        self.screen = None

        # Fishing Variables
        self.cast = False
        self.fishOnHook = False
        self.counter = 0
        self.fishCatched = 0


    def screenshot(self, top=860, left=1548, widht=982, height=387):
        
        # Make the screenshot
        scr = self.stc.grab({"top": top,
                        "left": left,
                        "width": widht,
                        "height": height
                        })
        # Convert to numpy Array
        img = np.array(scr)

        # Convert color coding
        self.screen = cv2.cvtColor(img, cv2.IMREAD_COLOR)


    def Cast(self):
        needleImg = cv2.imread('Assets/clickToCast.png', cv2.IMREAD_UNCHANGED)
        threshold = 0.8

        #Compare ScreenShopt to Needle Image
        result = cv2.matchTemplate(self.screen, needleImg, cv2.TM_CCOEFF_NORMED)

        #Filter all Results that are aboth the threshold
        yloc, xloc = np.where(result >= threshold)

        # If it finds a correct result left click to cast 
        if len(yloc) > 0:
            click()
            self.cast = True
            print("Fishingrod casted")

    def CatchFish(self):
        
        indicatorColor = np.array([0,173,255], dtype = "uint8") 
        sweetSpotColor = np.array([0,133,188], dtype = "uint8")

        maskIndicator = cv2.inRange(self.screen, indicatorColor, indicatorColor)
        maskSweetSpot = cv2.inRange(self.screen, sweetSpotColor, sweetSpotColor)

        try:
            IndicatorLeft = np.transpose(maskIndicator.nonzero())[0][1]
            IndicatorRigth = np.transpose(maskIndicator.nonzero())[-1][1]
            SweetSpotLeft = np.transpose(maskSweetSpot.nonzero())[0][1]
            SweetSpotRight = np.transpose(maskSweetSpot.nonzero())[-1][1]

            self.fishOnHook = True

            # 33 is real width of Sweetspot
            if(0 < SweetSpotRight-IndicatorRigth < 40 or 0 <IndicatorLeft - SweetSpotLeft < 40): 
                click()
        except:
            if self.fishOnHook:
                self.counter += 1
            if self.counter > 10:
                self.counter = 0
                self.fishOnHook = False
                self.cast = False
                self.fishCatched += 1
                print(str(self.fishCatched) + ' Fish catched!')



bot = Bot()


while True:
    if not bot.cast:
        bot.screenshot()
        bot.Cast()
    else:
        if bot.fishCatched >= 19    :
            keyDown('alt')
            press('tab')
            keyUp('alt')
            break
        bot.screenshot(948, 2039, 490, 69)
        bot.CatchFish()