from asyncore import write
from collections import deque
from cv2 import destroyAllWindows, log
import numpy as np
import cv2

class Object_Tracking():
    def __init__(self, proj):   

        cap = cv2.VideoCapture(0)

        buffer = 20

        pts = deque(maxlen=buffer)

        counter = 0

        (dX, dY) = (0, 0)

        direction = ''
        
        projection = proj
        while(1):
            # Store current frame
            ret, frame = cap.read()

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
                    if 35 < radius <= 40:
                        print("hit the wall at x: " + str(x) + " y: " + str(y))
                        projection.collision(x, y)
                # can use radius to see if the ball is at the wall cause the wall
                # distace from wall to camera is constant and the radius of the ball is constant
                # if radius > ballradius:
                #   its hit the wall
                #   x, y = the position
                #   if x,y =  where animal is then:
                #       animal moves backwards

            # Using numpy arange function for better performance. Loop till all detected points
            for i in np.arange(1, len(pts)):
                # If no points are detected, move on.
                if(pts[i-1] == None or pts[i] == None):
                    continue

                # If atleast 10 frames have direction change, proceed
                if counter >= 10 and i == 1 and pts[-10] is not None:
                    # Calculate the distance between the current frame and 10th frame before
                    dX = pts[-10][0] - pts[i][0]
                    dY = pts[-10][1] - pts[i][1]
                    (dirX, dirY) = ('', '')

                    # If distance is greater than 100 pixels, considerable direction change has occured.
                    if np.abs(dX) > 100:
                        dirX = 'West' if np.sign(dX) == 1 else 'East'

                    if np.abs(dY) > 100:
                        dirY = 'North' if np.sign(dY) == 1 else 'South'

                    # Set direction variable to the detected direction
                    direction = dirX if dirX != '' else dirY

                # Draw a trailing red line to depict motion of the object.
                thickness = int(np.sqrt(buffer / float(i + 1)) * 2.5)
                cv2.line(frame, pts[i - 1], pts[i], (0, 0, 255), thickness)

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
        cap.release()
        cv2.destroyAllWindows()
Object_Tracking()