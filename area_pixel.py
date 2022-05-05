from asyncio.windows_events import NULL
# from curses.ascii import NUL
import cv2
from collections import deque
import numpy as np
from object_tracking import Object_Tracking
import threading
from projection import Projection
from grid import Grid
from time import sleep

object_width = 0
object_height = 0

# projection = None
projection = None
grid = Grid()

class Project_Area():

    def __init__(self):
        
        # load cap
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

        t = threading.Thread(target=self.Find_Projection)
        t.start()
        sleep(5)
        t2 = threading.Thread(target=self.Find_Projectile)
        t2.start()
        t3 = threading.Thread(target=self.Load_Grid)
        t3.start()

    def Load_Grid(self):
        global grid
        grid.begin()

    def Find_Projectile(self): 

        buffer = 20

        pts = deque(maxlen=buffer)

        counter = 0

        (dX, dY) = (0, 0)

        direction = ''
        while(1):
            # Store current frame
            ret, frame = self.cap.read()

            # Blur the frame using a Gaussian blur. Removes excess noise.
            blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

            # Convert frame to HSV, HSV allows better segmentation
            hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

            # Create a mask for all red elements in capture
            lower_red = np.array([0, 50, 50])
            upper_red = np.array([10, 255, 255])
            mask0 = cv2.inRange(hsv, lower_red, upper_red)
            lower_red = np.array([170, 50, 50])
            upper_red = np.array([180, 255, 255])
            mask1 = cv2.inRange(hsv, lower_red, upper_red)
            mask = mask0+mask1

            # Erode masked output to delete small white dots present in image
            mask = cv2.erode(mask, None, iterations=2)

            # Dilate the resultant image to restore target
            mask = cv2.dilate(mask, None, iterations=2)

            # Find all controus in the mask
            contours, hierachy = cv2.findContours(
                mask.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

            center = None

            # print(len(contours)) returns how many red is on screen

            # If any object is detected, then only proceed
            if(len(contours) > 0):
                # Find the contour with maximum area
                c = max(contours, key=cv2.contourArea)

                # Find the center of the circle, and its radius of the largest detected contour.
                ((x, y), radius) = cv2.minEnclosingCircle(c)
                # Calculate the centroid of the ball, as we need to draw a circle around it.
                M = cv2.moments(c)
                center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))

                # Proceed only if a ball of considerable size is detected
                if radius > 10:
                    # Draw circles around the object as well as its centre
                    cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                    cv2.circle(frame, center, 5, (0, 255, 255), -1)
                    # Append the detected object in the frame to pts deque structure
                    pts.appendleft(center)

                    # print(x, y, radius)
                # print(radius)
                    if 15 < radius <= 20:
                        print("hit the wall at x: " + str(x) + " y: " + str(y))
                        if projection.collision(x, y):
                            grid.collision(x,y)
                # can use radius to see if the ball is at the wall cause the wall
                # distace from wall to camera is constant and the radius of the ball is constant
                # if radius > ballradius:
                #   its hit the wall
                #   x, y = the position
                #   if x,y =  where animal is then:
                #       animal moves backwards

            # Using numpy arange function for better performance. Loop till all detected points
            #for i in np.arange(1, len(pts)):
                # If no points are detected, move on.
            #    if(pts[i-1] == None or pts[i] == None):
            #        continue

                # If atleast 10 frames have direction change, proceed
            #    if counter >= 10 and i == 1 and pts[-10] is not None:
                    # Calculate the distance between the current frame and 10th frame before
            #        dX = pts[-10][0] - pts[i][0]
            #        dY = pts[-10][1] - pts[i][1]
            #        (dirX, dirY) = ('', '')

                    # If distance is greater than 100 pixels, considerable direction change has occured.
            #        if np.abs(dX) > 100:
            #            dirX = 'West' if np.sign(dX) == 1 else 'East'

            #        if np.abs(dY) > 100:
            #            dirY = 'North' if np.sign(dY) == 1 else 'South'

                    # Set direction variable to the detected direction
            #        direction = dirX if dirX != '' else dirY

                # Draw a trailing red line to depict motion of the object.
            #    thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
            #    cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

            # Write the detected direction on the frame.
            cv2.putText(frame, direction, (20, 40),
                        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 3)

            # Show the output frame.
            cv2.imshow('Window- Direction Detection', frame)
            cv2.imshow('Mask', mask)
            key = cv2.waitKey(1) & 0xFF
            # Update counter as the direction change has been detected.
            counter += 1

            # If q is pressed, close the window
            if(key == ord('q')):
                break
        # After all the processing, release webcam and destroy all windows
        cv2.destroyAllWindows()

    def Find_Projection(self):
        while True:
            # Capture frame-by-frame
            ret, frame = self.cap.read()
        

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
            lower_blue = np.array([90, 100, 100])
            upper_blue = np.array([150, 255, 255])
            mask = cv2.inRange(hsv, lower_blue, upper_blue)

            # result = cv2.bitwise_and(frame, frame, mask=mask)
            


            contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
            
            if len(contours) > 0:
                # cv2.drawContours(frame, contours, -1, (0,255,0), 5)

                # find the biggest countour (c) by the area
                c = max(contours, key = cv2.contourArea)
                x,y,w,h = cv2.boundingRect(c)

                # draw the biggest contour (c) in green
                rect = cv2.rectangle(frame,(x,y),(x+w,y+h),(0,255,0),2)

                # find center of object
                M = cv2.moments(c)
                divider = M["m00"]
                if(divider == 0):
                    divider = 1
                cX = int(M["m10"] / divider)
                cY = int(M["m01"] / divider)

                # display center object with white color
                cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
                cv2.putText(frame, "X: {}".format(cX), (int(cX - 20), int(cY- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
                cv2.putText(frame, "Y: {}".format(cY), (int(cX - 20), int(cY+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
                global projection
                projection = Projection(cX, cY, h, w)
                # testing coord for object with red color
                # cv2.circle(frame, (100, 100), 7, (0, 0, 255), -1)
                # cv2.putText(frame, "X: {}".format(100), (int(100 - 20), int(100- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))
                # cv2.putText(frame, "Y: {}".format(100), (int(100 - 20), int(100+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))
                # cv2.circle(frame, (300, 300), 7, (0, 0, 255), -1)
                # cv2.putText(frame, "X: {}".format(300), (int(300 - 20), int(300- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))
                # cv2.putText(frame, "Y: {}".format(300), (int(300 - 20), int(300+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (0,0,255))

            # Display the resulting frame
            cv2.imshow('frame',frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cv2.destroyAllWindows()

Project_Area()