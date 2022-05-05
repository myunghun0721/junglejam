import numpy as np
import cv2

cap = cv2.VideoCapture(0)
kernel = np.ones((2,2),np.uint8)
while(True):
    # Capture frame-by-frame
    ret, frame = cap.read()
   

    # # Our operations on the frame come here
    # gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    # gray = cv2.GaussianBlur(gray, (7, 7), 0)
    # gray= cv2.medianBlur(gray, 3)   #to remove salt and paper noise
    # #to binary
    # ret,thresh = cv2.threshold(gray,200,255,0)  #to detect white objects
    # #to get outer boundery only     
    # thresh = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)
    # #to strength week pixels
    # thresh = cv2.dilate(thresh,kernel,iterations = 5)

    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    lower_red = np.array([0, 50, 50])
    upper_red = np.array([10, 255, 255])
    mask0 = cv2.inRange(hsv, lower_red, upper_red)
    lower_red = np.array([170, 50, 50])
    upper_red = np.array([180, 255, 255])
    mask1 = cv2.inRange(hsv, lower_red, upper_red)
    mask = mask0+mask1

    # result = cv2.bitwise_and(frame, frame, mask=mask)
    


    contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    
    if len(contours) > 0:
        cv2.drawContours(frame, contours, -1, (0,255,0), 5)
        # find the biggest countour (c) by the area
        c = max(contours, key = cv2.contourArea)
        x,y,w,h = cv2.boundingRect(c)

        # draw the biggest contour (c) in green
        cv2.rectangle(frame,(x,y),(x+w,y+h),(255,0,0),2)
    # Display the resulting frame

    cv2.imshow('frame',frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()