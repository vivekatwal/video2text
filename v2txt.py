import cv2
import numpy as np
import pytesseract
from PIL import Image
import multiprocessing as mp
import time
from fuzzywuzzy import fuzz
from multiprocessing import queues

streaming = 0
# Create a VideoCapture object and read from input file
# If the input is the camera, pass 0 instead of the video file name
cap = cv2.VideoCapture('media.mp4')

def getText(crop_img):
    img = Image.fromarray(crop_img)
    text = pytesseract.image_to_string(img)
    # print(text)
    return text

def isSubSequence(string1, string2, m, n):
    # Base Cases
    if m == 0:    return True
    if n == 0:    return False

    # If last characters of two strings are matching
    if string1[m - 1] == string2[n - 1]:
        return isSubSequence(string1, string2, m - 1, n - 1)

        # If last characters are not matching
    return isSubSequence(string1, string2, m, n - 1)


# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")

manager = mp.Manager()
return_dict = manager.dict()
count = {}
cnt = 1
jobs = []
# Read until video is completed
string1 = ''
start = time.time()
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:


        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        y, h, x, w = 660, 100, 0, 1200
        crop_img = gray[y:y + h, x:x + w]

        text = getText(crop_img)
        # print(text)

        # dictionary to keep count of all the extracted text, this will help to avoid noise in the text
        if text in count:
            count[text] = count[text] + 1
        else:
            count[text] = 1

        if not string1:
            string1 = text
            continue

        if streaming:
            # for streaming text
            op = isSubSequence(string1, text, len(string1), len(text))
            op1 = isSubSequence(text, string1, len(text), len(string1))

            # print(op)
            if op or op1:
                string1 = text
                continue
            else:
                print('string1')
                print(string1)
                print('text')
                print(text)
                print(op, op1)
                # print(string1)
                continue

        else:
            ## for full text
            op = fuzz.ratio(string1, text)
            if op < 90:

                if len(text) > 5:
                    print(text)
                    end = time.time()
                    diff_time = end - start
                    start = time.time()
                    print('time taken :', diff_time)
                    print('count: ', count[string1])
                string1 = text

        # p = mp.Process(target=getText, args=(crop_img,))
        #
        # if cnt < 3:
        #     jobs.append(p)
        #     p.start()
        # else:
        #     jobs = []
        #
        #     for proc in jobs:
        #         proc.join()
        #     print(return_dict.values())
        #
        #     time.sleep(60)
        # Display the resulting frame
        cv2.imshow('Frame', crop_img)

        # Press Q on keyboard to  exit
        if cv2.waitKey(25) & 0xFF == ord('q'):
            break

    # Break the loop
    else:
        break

# When everything done, release the video capture object
cap.release()

# Closes all the frames
cv2.destroyAllWindows()

