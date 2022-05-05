import pygame, sys
from button import Button
from pygame import mixer
import numpy as np
import cv2
import threading
from time import sleep
from collections import deque


pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Jungle Jam")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("venv/assets/font.ttf", size)

BG = pygame.image.load("venv/images/jungle_jam.jpg")

music = pygame.mixer.Sound('venv/assets/Jungle_Beatz_V1.mp3')
# play music forever
music.play(-1)
foodhit = pygame.mixer.Sound('venv/assets/Splat3.mp3')
score_value = 0
cap = cv2.VideoCapture(1)

buffer = 20

pts = deque(maxlen=buffer)

counter = 0

(dX, dY) = (0, 0)

direction = ''
pts = deque(maxlen=buffer)

def leaderboard():
    sleep(0.7)
    global score_value
    while True:
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
                cv2.putText(frame, "Center: {}".format(center), (int(x - 20), int(y- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
                # cv2.putText(frame, "Y: {}".format(int(y)), (int(x - 20), int(y+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))

                # cv2.rectangle(frame, (400,200), (500,300), (255,0,0), 2)
 
                # Append the detected object in the frame to pts deque structure
                pts.appendleft(center)

                # print(x, y, radius)
            # print(radius)

                if 20 < radius <= 30:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    # if(x < 300 and y < 500 and x > 200 and y > 400):
                    cv2.destroyAllWindows()
                    foodhit.play()
                    main_menu()
                    
                    


        # Show the output frame.
        # cv2.imshow('Window- Direction Detection', frame)


        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the score screen.", True, "#ffe600")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)


        SCORE_TEXT = get_font(45).render("Your score : " + str(score_value), True, "#ffe600")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(960, 560))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        MAIN_TEXT = get_font(45).render("HIT THE WALL TO GO BACK TO MAIN MENU", True, "#ffe600")
        MAIN_RECT = MAIN_TEXT.get_rect(center=(960, 800))
        SCREEN.blit(MAIN_TEXT, MAIN_RECT)





        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def play():
    sleep(0.7)
    # cv2.destroyAllWindows()
    global score_value
    while True:
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
                cv2.putText(frame, "Center: {}".format(center), (int(x - 20), int(y- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
                # cv2.putText(frame, "Y: {}".format(int(y)), (int(x - 20), int(y+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))

                # cv2.rectangle(frame, (400,200), (500,300), (255,0,0), 2)
 
                # Append the detected object in the frame to pts deque structure
                pts.appendleft(center)

                # print(x, y, radius)
            # print(radius)

                if 20 < radius <= 30:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    # if(x < 300 and y < 300 and x > 200 and y > 200):
                    #     print(center)
                    #     cv2.destroyAllWindows()
                    #     leaderboard()
                    


        # Show the output frame.
        # cv2.imshow('Window- Direction Detection', frame)

        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")

        PLAY_TEXT = get_font(45).render("This is the PLAY screen.", True, "#ffe600")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        TOSCORE = Button(image=None, pos=(960, 460), 
                            text_input="OK", font=get_font(75), base_color="#ffe600", hovering_color="White")
        UPSCORE = Button(image=None, pos=(960, 860), 
                            text_input="+1 score button", font=get_font(75), base_color="#ffe600", hovering_color="White")

        # TOSCORE.changeColor(PLAY_MOUSE_POS)
        # TOSCORE.update(SCREEN)
        for button in [TOSCORE, UPSCORE]:
            button.changeColor(PLAY_MOUSE_POS)
            button.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if TOSCORE.checkForInput(PLAY_MOUSE_POS):
                    cv2.destroyAllWindows()
                    leaderboard()
                if UPSCORE.checkForInput(PLAY_MOUSE_POS):
                    score_value +=1

        pygame.display.update()

def main_menu():
    # prevents jumping to the play screen
    sleep(0.7)
    while True:
        ret, frame = cap.read()

        # Blur the frame using a Gaussian blur. Removes excess noise.
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # Convert frame to HSV, HSV allows better segmentation
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Create a mask for all red elements in capture
        lower_red = np.array([0, 60, 60])
        upper_red = np.array([10, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red = np.array([170, 60, 60])
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
                cv2.putText(frame, "Center: {}".format(center), (int(x - 20), int(y- 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))
                # cv2.putText(frame, "Y: {}".format(int(y)), (int(x - 20), int(y+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))

                # cv2.rectangle(frame, (400,200), (500,300), (255,0,0), 2)
 
                # Append the detected object in the frame to pts deque structure
                pts.appendleft(center)

                # print(x, y, radius)
            # print(radius)
                if 20 < radius <= 30:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    # if(x < 500 and y < 300 and x > 400 and y > 200):
                    cv2.destroyAllWindows()
                    foodhit.play()
                    play()
                        
                    


        # Show the output frame.
        cv2.imshow('Window- Direction Detection', frame)

        SCREEN.blit(BG, (0, 0))
        # MENU_MOUSE_POS = pygame.mouse.get_pos()


        # PLAY_BUTTON = Button(image=pygame.image.load("venv/assets/Play Rect.png"), pos=(960, 800), 
        #                     text_input="PLAY", font=get_font(75), base_color="#ffe600", hovering_color="White")



        # QUIT_BUTTON = Button(image=pygame.image.load("venv/assets/Quit Rect.png"), pos=(960, 950), 
        #                     text_input="QUIT", font=get_font(75), base_color="#ffe600", hovering_color="White")


        # for button in [PLAY_BUTTON]:
        #     button.changeColor(MENU_MOUSE_POS)
        #     button.update(SCREEN)
        
        # for event in pygame.event.get():
        #     if event.type == pygame.QUIT:
        #         # cv2.destroyAllWindows()
        #         pygame.quit()
        #         sys.exit()
        #     if event.type == pygame.MOUSEBUTTONDOWN:
        #         if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
        #             play()

                # if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                #     # cv2.destroyAllWindows()
                #     pygame.quit()
                #     sys.exit()
        PLAY_TEXT = get_font(45).render("HIT THE WALL TO PLAY", True, "#ffe600")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 800))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()

        pygame.display.update()

main_menu()