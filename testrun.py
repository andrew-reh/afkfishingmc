import cv2 as cv
import numpy as np
import pytesseract as pytess
from PIL import Image, ImageEnhance
import time
import mouse

pytess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

cap = cv.VideoCapture(0)
if not cap.isOpened():
    print("cannot open camera")
    exit()

oldtime = time.perf_counter()
prev_frame = cv.cvtColor(cap.read()[1], cv.COLOR_BGR2GRAY)
prev_frame = cv.addWeighted(prev_frame, 1.9, prev_frame, 0, 0)
prev_frame = cv.threshold(prev_frame, 127, 255, cv.THRESH_BINARY)[1]

while True:
    #Capture frame-by-frame
    tic = time.perf_counter()
    ret, new_frame = cap.read()

    #if frame is read correctly ret is True
    if not ret:
        print("Can't receive frame (stream end?). Exiting...")
        break
    gray = cv.cvtColor(new_frame, cv.COLOR_BGR2GRAY)
    #im = Image.open(frame)
    #enhancer = ImageEnhance.Contrast(gray)
    #im_output = enhancer.enhance(1.9)
    gray_sat = cv.addWeighted(gray, 1.9, gray, 0, 0)
    im_bw = cv.threshold(gray_sat, 127, 255, cv.THRESH_BINARY)[1]
    diff = cv.norm(im_bw, prev_frame, normType = cv.NORM_L1)
    if diff >= 5000000:
        #print(diff)
        teststring = pytess.image_to_string(im_bw)
        #print(teststring)
        if "obber splashe" in teststring:
            if time.perf_counter()-oldtime > 3.5:
                mouse.click('right')
                oldtime = time.perf_counter()
                time.sleep(1)
                mouse.click('right')

    toc = time.perf_counter()
    #print(toc-tic)
    prev_frame = im_bw
    if cv.waitKey(1) == ord('i'):
        break

cap.release()
cv.destroyAllWindows()