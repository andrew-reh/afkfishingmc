import cv2 as cv
import numpy as np
import pytesseract as pytess
from PIL import Image, ImageEnhance
import time
import mouse

#Need Tesseract installed (This is the path there)
pytess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

#Open video capture at camera 0 (OBS virtualcam)
cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("cannot open camera")
    exit()

#Initializing variables to be used in the loop
oldtime = time.perf_counter()
prev_frame = cv.cvtColor(cap.read()[1], cv.COLOR_BGR2GRAY)
prev_frame = cv.addWeighted(prev_frame, 1.9, prev_frame, 0, 0)
prev_frame = cv.threshold(prev_frame, 127, 255, cv.THRESH_BINARY)[1]

while True:
    #Performance tester variable
    tic = time.perf_counter()

    #Capture frame-by-frame
    ret, new_frame = cap.read()

    #if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break

    #Initial input in grayscale
    gray = cv.cvtColor(new_frame, cv.COLOR_BGR2GRAY)
    
    #Increase contrast/saturation
    gray_sat = cv.addWeighted(gray, 1.9, gray, 0, 0)

    #Make black and white
    im_bw = cv.threshold(gray_sat, 127, 255, cv.THRESH_BINARY)[1]

    #Check difference between this frame and previous frame
    diff = cv.norm(im_bw, prev_frame, normType = cv.NORM_L1)


    if diff >= 5000000:
        #print(diff)
        teststring = pytess.image_to_string(im_bw)
        #print(teststring)
        if "obber splashe" in teststring:
            #If at least 3.5 seconds have passed since last reel
            if time.perf_counter()-oldtime > 3.5:
                #Reel in bobber, wait, send out bobber
                mouse.click('right')
                oldtime = time.perf_counter()
                time.sleep(1)
                mouse.click('right')
    #Performance counter option
    toc = time.perf_counter()
    #print(toc-tic)

    #Store previous frame
    prev_frame = im_bw

    cv.imshow('image', gray)
    if cv.waitKey(1) == ord('i'):
        print('test')
        break

cap.release()
cv.destroyAllWindows()