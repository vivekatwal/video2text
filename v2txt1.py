import cv2
import numpy as np
import pytesseract
from PIL import Image
import multiprocessing as mp
import time
from fuzzywuzzy import fuzz
from multiprocessing import queues



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

    if string1[m - 1] == string2[n - 1]:
        return isSubSequence(string1, string2, m - 1, n - 1)

        # If last characters are not matching
    return isSubSequence(string1, string2, m, n - 1)


# Check if camera opened successfully
if (cap.isOpened() == False):
    print("Error opening video stream or file")


count = {}
cnt = 1
jobs = []
final_string = []
# Read until video is completed
prev_string = ''
start = time.time()
while (cap.isOpened()):
    # Capture frame-by-frame
    ret, frame = cap.read()
    if ret == True:



        y, h, x, w = 660, 30, 650, 1200
        crop_img = frame[y:y + h, x:x + w]
        gray = cv2.cvtColor(crop_img, cv2.COLOR_BGR2GRAY)

        cur_string = getText(gray)

        # if cur_string == '':
        #     print('blank')

        try:
            if not prev_string:
                prev_string = cur_string
                initial_list = (prev_string + '.')[:-1]
                final_string.extend(initial_list.split()[:-1])
                continue

            # for lists
            prev_string_list = prev_string.split()
            cur_string_list = cur_string.split()

            if prev_string_list == cur_string_list:
                continue
            elif prev_string_list[-2] == cur_string_list[-2]:
                prev_string = cur_string
                continue
            elif final_string[-1] == cur_string_list[-2]:
                prev_string = cur_string
                continue
            else:
                if cur_string_list[-2] in final_string[:]:
                    pass
                else:
                    final_string.append(cur_string_list[-2])
                print(final_string)
                prev_string = cur_string
        except:
            # print(i)
            continue

        # dictionary to keep count of all the extracted text, this will help to avoid noise in the text
        if cur_string in count:
            count[cur_string] = count[cur_string] + 1
        else:
            count[cur_string] = 1


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

