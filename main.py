import cv2 as cv
import pytesseract as pytess
import time
import mouse


def main():
    # Need Tesseract installed, put the path here
    pytess.pytesseract.tesseract_cmd = r'C:\\Program Files\\Tesseract-OCR\\tesseract.exe'

    test_perf = False

    # Open video capture at camera 0 (OBS virtualcam)
    cap = cv.VideoCapture(0)
    if not cap.isOpened():
        print("cannot open camera")
        exit()

    # Initializing variables to be used in the loop
    if test_perf:
        old_time = time.perf_counter()
    prev_frame = cv.cvtColor(cap.read()[1], cv.COLOR_BGR2GRAY)
    prev_frame = cv.addWeighted(prev_frame, 1.9, prev_frame, 0, 0)
    prev_frame = cv.threshold(prev_frame, 127, 255, cv.THRESH_BINARY)[1]

    while True:
        if test_perf:
            tic = time.perf_counter()

        # Capture frame-by-frame
        ret, new_frame = cap.read()

        if not ret:
            print("Can't receive frame (stream end?). Exiting...")
            break

        # Color filtering
        gray = cv.cvtColor(new_frame, cv.COLOR_BGR2GRAY)
        gray_sat = cv.addWeighted(gray, 1.9, gray, 0, 0)
        im_bw = cv.threshold(gray_sat, 127, 255, cv.THRESH_BINARY)[1]

        # Check difference between this frame and previous frame
        diff = cv.norm(im_bw, prev_frame, normType=cv.NORM_L1)

        if diff >= 5000000:
            teststring = pytess.image_to_string(im_bw)
            if "obber splashe" in teststring:
                # If at least 3.5 seconds have passed since last reel
                if time.perf_counter() - old_time > 3.5:
                    # Reel in bobber, wait, send out bobber
                    mouse.click('right')
                    old_time = time.perf_counter()
                    time.sleep(1)
                    mouse.click('right')

        if test_perf:
            toc = time.perf_counter()
            print(toc - tic)

        # Store previous frame
        prev_frame = im_bw

        cv.imshow('image', gray)
        if cv.waitKey(1) == ord('i'):
            print('test')
            break

    cap.release()
    cv.destroyAllWindows()


if __name__ == "__main__":
    main()
