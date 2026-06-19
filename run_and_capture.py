import subprocess
import time
import sys
import os

xvfb = subprocess.Popen(["Xvfb", ":99", "-screen", "0", "1024x768x24"])
time.sleep(2)

env = os.environ.copy()
env["DISPLAY"] = ":99"

app_proc = subprocess.Popen(["uv", "run", "python", "finalcif/finalcif_start.py"], env=env)
time.sleep(15)

screenshot_code = """
import sys
from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QGuiApplication
app = QApplication(sys.argv)
screen = QGuiApplication.primaryScreen()
if screen:
    pixmap = screen.grabWindow(0)
    pixmap.save('screenshot.png')
    print('Screenshot saved to screenshot.png')
"""

subprocess.run(["uv", "run", "python", "-c", screenshot_code], env=env)

app_proc.terminate()
xvfb.terminate()
