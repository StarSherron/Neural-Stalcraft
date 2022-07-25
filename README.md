# Neural-Stalcraft
An aimbot that uses Yolov5 and PyTorch to play Stalcraft [PAID-VER]
# How To Use
Currently, no one have to use this.
I suggest that the game is already open in the background before launching the model.

# How to train model
Python code:
  import pyautogui
  from win32api import GetKeyState
  from win32con import VK_CAPITAL
   
  i = 0
 
 
  while True:
      if GetKeyState(VK_CAPITAL) == 1:
          myScreenshot = pyautogui.screenshot()
          myScreenshot.save('E:/Ai Training/2/' + str(i) + '.png')
          myScreenshot.close()
 
          i += 1
