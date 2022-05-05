import cv2
from collections import deque
from object_detector import *
import numpy as np
from object_tracking import Object_Tracking
import threading
from projection import Projection

# projection = None
projection = Projection(0, 0, 600, 600)

class Project_Area():

    def __init__(self):
        
        # load cap
        self.cap = cv2.VideoCapture(0)
        self.cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
        self.cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

       # t = threading.Thread(target=self.Find_Projection)
       # t.start()
        t2 = threading.Thread(target=self.Find_Projectile)
        t2.start()

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
        cv2.destroyAllWindows()

    def Find_Projection(self):
        # Load Aruco detector
        parameters = cv2.aruco.DetectorParameters_create()
        aruco_dict = cv2.aruco.Dictionary_get(cv2.aruco.DICT_5X5_50)

        # Load Object Dector
        detector = HomogeneousBgDetector()

        # load img
        # img = cv2.imread('venv/assets/phone_aruco_marker.jpg')
        while True:
            _, img = self.cap.read()

            # get aruco marker
            corners, _, _ = cv2.aruco.detectMarkers(img, aruco_dict, parameters=parameters)
            if corners: 
            
                # Draw line around marker
                int_corners = np.int0(corners)
                cv2.polylines(img, int_corners, True, (0,255,0), 5)

                # aruco perimeter
                aruco_perimeter = cv2.arcLength(corners[0], True)
                # print(aruco_perimeter)

                # pixel to cm ratio
                pixel_cm_ratio = aruco_perimeter / 40


                contours = detector.detect_objects(img)
                # print(contours)

                # Draw objects boundaries
                for cnt in contours:

                    # getting  rect
                    rect = cv2.minAreaRect(cnt)
                    (x,y), (w, h), angle = rect

                    # Get width and height of the object by applying the ratio px to cm
                    object_width = h / pixel_cm_ratio
                    object_height = w / pixel_cm_ratio

                    global projection
                    projection = Projection(x, y, w, h)

                    print(projection.x)


                    # Display rect
                    box = cv2.boxPoints(rect)
                    box = np.int0(box)


                    # for color -> (blue, yellow, red)
                    cv2.circle(img, (int(x), int(y)), 5, (0, 0, 255), -1)
                    # Draw outer line
                    cv2.polylines(img, [box], True, (255, 0, 0), 2)
                    cv2.putText(img, "Width {} cm".format(round(object_width, 1)), (int(x - 100), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)
                    cv2.putText(img, "Height {} cm".format(round(object_height, 1)), (int(x - 100), int(y + 15)), cv2.FONT_HERSHEY_PLAIN, 2, (100, 200, 0), 2)

                # print(box)

                # print(x, y)
                # print(w, h)
                # print(angle)

            cv2.imshow('Image', img)

            if(cv2.waitKey(1) & 0xFF == ord('q')):
                break

        cv2.destroyAllWindows()

Project_Area()