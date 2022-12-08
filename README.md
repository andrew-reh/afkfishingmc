# afkfishingmc

This script is a simple script and is intended to implement afk fishing in Minecraft versions 1.17 and 
below. It takes input from an OBS virtual camera and runs it through Tesseract OCR to look for the "fishing
bobber splashes" line in order to reel in the rod.


### Step 1
Turn on captions in Minecraft

### Step 2
Install [OBS](https://obsproject.com/download) and [OBS virtual camera](https://github.com/Fenrirthviti/obs-virtual-cam/releases) 
extension, as well as [Tesseract](https://digi.bib.uni-mannheim.de/tesseract/). Set up all of the above so they work as intended,
and so that the virtual camera is the "first" camera on your computer (or change the code to select the right camera).

### Step 3
Clone this repo, and make sure your python path that you're using (conda, venv, etc.) has all the required dependencies (mouse, pytesseract, cv2).

### Step 4
Open Minecraft and OBS, adjust the feed so it's almost entirely the captions, and then run this script while fishing! Enjoy your enchanted books.
