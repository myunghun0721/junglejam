from glob import glob
import pygame, sys
from button import Button
from pygame import mixer
import numpy as np
import cv2
import threading
from collections import deque
from time import sleep
from projection import Projection
from pygame_test import *
from audioop import cross
from pickle import TRUE
import random
from re import A
from pygame.locals import *

class Background(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()


class Tiger(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.center = [pos_x, pos_y]
        self.x = pos_x
        self.y = pos_y
    time = 0
    layer = 1
    # def update(self):
    # self.rect.center = pygame


class Fruit(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, spriteList):
        super().__init__()
        self.is_animating = False
        self.sprites = spriteList
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False

            self.image = self.sprites[int(self.current_sprite)]


class Crosshair(pygame.sprite.Sprite):
    def __init__(self, image):
        super().__init__()
        self.image = image
        self.rect = self.image.get_rect()
        # can play sounds here
        # self.gunshot = pygame.mixer.Sound('sound file')

    def shoot(self):
        pygame.sprite.spritecollide(crosshair, tiger_group, True)

    def update(self):
        self.rect.center = pygame.mouse.get_pos()

pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Jungle Jam")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("venv/assets/font.ttf", size)

BG = pygame.image.load("venv/images/jungle_jam.jpg")

music = mixer.music
music.load('venv/assets/Jungle_Beatz_V1.mp3')
# play music forever
music.play(-1)
score_value = 0
cap = cv2.VideoCapture(0)
projection = Projection(0,0,0,0)
crosshair = None
tiger_group = None


def leaderboard():
    buffer = 20

    pts = deque(maxlen=buffer)

    counter = 0

    (dX, dY) = (0, 0)

    direction = ''
    pts = deque(maxlen=buffer)

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

        # print(len(contours)) returns how many red is on SCREEN

        cv2.circle(frame, (200,400), 5, (0, 255, 0), -1)
        cv2.circle(frame, (200,500), 5, (0, 255, 0), -1)
        cv2.circle(frame, (300,400), 5, (0, 255, 0), -1) 
        cv2.circle(frame, (300,500), 5, (0, 255, 0), -1) 
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

                if 35 < radius <= 40:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    if(x < 300 and y < 500 and x > 200 and y > 400):
                        print(center)
                        cv2.destroyAllWindows()
                        main_menu()
                    


        # Show the output frame.
        cv2.imshow('Window- Direction Detection', frame)



        PLAY_MOUSE_POS = pygame.mouse.get_pos()

        SCREEN.fill("black")
        SCORE_TEXT = get_font(45).render("Your score : " + str(score_value), True, "#ffe600")
        SCORE_RECT = SCORE_TEXT.get_rect(center=(960, 560))
        SCREEN.blit(SCORE_TEXT, SCORE_RECT)

        PLAY_TEXT = get_font(45).render("This is the score screen.", True, "#ffe600")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 260))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        PLAY_BACK = Button(image=None, pos=(960, 1000), 
                            text_input="OK", font=get_font(75), base_color="#ffe600", hovering_color="White")

        PLAY_BACK.changeColor(PLAY_MOUSE_POS)
        PLAY_BACK.update(SCREEN)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BACK.checkForInput(PLAY_MOUSE_POS):
                    score_value = 0
                    main_menu()

        pygame.display.update()

def play():    
    startGame()
    #t = threading.Thread(target=startGame)
    # t.start()
    # t2 = threading.Thread(target=playTracking)
    # t2.start()


def playTracking():

    buffer = 20

    pts = deque(maxlen=buffer)

    counter = 0

    (dX, dY) = (0, 0)

    direction = ''
    pts = deque(maxlen=buffer)
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

        cv2.circle(frame, (200,200), 5, (0, 255, 0), -1)
        cv2.circle(frame, (200,300), 5, (0, 255, 0), -1)
        cv2.circle(frame, (300,200), 5, (0, 255, 0), -1) 
        cv2.circle(frame, (300,300), 5, (0, 255, 0), -1) 
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

                #if 35 < radius <= 40:
                #    print("hit the wall at x: " + str(x) + " y: " + str(y))
                #    if(x < 300 and y < 300 and x > 200 and y > 200):
                #        print(center)
                #        cv2.destroyAllWindows()
                #        leaderboard()
                    


        # Show the output frame.
        cv2.imshow('Window- Direction Detection', frame)
        pygame.display.update()

        
def main_menu():
    buffer = 20

    pts = deque(maxlen=buffer)

    counter = 0

    (dX, dY) = (0, 0)

    direction = ''
    pts = deque(maxlen=buffer)
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

        cv2.circle(frame, (400,200), 5, (0, 255, 0), -1)
        cv2.circle(frame, (400,300), 5, (0, 255, 0), -1)
        cv2.circle(frame, (500,200), 5, (0, 255, 0), -1) 
        cv2.circle(frame, (500,300), 5, (0, 255, 0), -1) 
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
                if 35 < radius <= 40:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    if(x < 500 and y < 300 and x > 400 and y > 200):
                        cv2.destroyAllWindows()
                        play()
        # Show the output frame.
        cv2.imshow('Window- Direction Detection', frame)

        SCREEN.blit(BG, (0, 0))
        MENU_MOUSE_POS = pygame.mouse.get_pos()


        PLAY_BUTTON = Button(image=pygame.image.load("venv/assets/Play Rect.png"), pos=(960, 800), 
                            text_input="PLAY", font=get_font(75), base_color="#ffe600", hovering_color="White")

        QUIT_BUTTON = Button(image=pygame.image.load("venv/assets/Quit Rect.png"), pos=(960, 950), 
                            text_input="QUIT", font=get_font(75), base_color="#ffe600", hovering_color="White")


        for button in [PLAY_BUTTON, QUIT_BUTTON]:
            button.changeColor(MENU_MOUSE_POS)
            button.update(SCREEN)
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                # cv2.destroyAllWindows()
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    # cv2.destroyAllWindows()
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

def start():

    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    SCREEN.fill("#04F404")

    pygame.display.update()

    count = 0
        
    while count < 10:

        ret, frame = cap.read()

        hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        lower_green = np.array([50, 100, 100])
        upper_green = np.array([70, 255, 255])
        mask = cv2.inRange(hsv, lower_green, upper_green)

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
            if(projection.w > w and projection.h > h):
                projection = Projection(cX, cY, h, w)

        count += 1

    sleep(3)

    #print("x: " + projection.x + "    y: " + projection.y)

    main_menu()

def startGame():
    clock = pygame.time.Clock()

    global SCREEN
    global crosshair
    global tiger_group

    background = pygame.image.load("pics/black.jpg")

    # disable pygame mouse
    pygame.mouse.set_visible(False)

    # setting background to resolution
    BG_IMAGE_1 = pygame.image.load("pics/background images/jungle_Background_6.png")
    BG_IMAGE_1 = pygame.transform.scale(BG_IMAGE_1, (1440, 900))
    BG_IMAGE_2 = pygame.image.load("pics/background images/jungle_Background_5.png")
    BG_IMAGE_2 = pygame.transform.scale(BG_IMAGE_2, (1440, 900))
    BG_IMAGE_3 = pygame.image.load("pics/background images/jungle_Background_4.png")
    BG_IMAGE_3 = pygame.transform.scale(BG_IMAGE_3, (1440, 900))
    BG_IMAGE_4 = pygame.image.load("pics/background images/jungle_Background_3.png")
    BG_IMAGE_4 = pygame.transform.scale(BG_IMAGE_4, (1440, 900))
    BG_IMAGE_5 = pygame.image.load("pics/background images/jungle_Background_2.png")
    BG_IMAGE_5 = pygame.transform.scale(BG_IMAGE_5, (1440, 900))

    # setting fruit to resolution
    FRUIT_IMAGE_1 = pygame.image.load("pics/apple animation/apple_1.png")
    FRUIT_IMAGE_1 = pygame.transform.scale(FRUIT_IMAGE_1, (75, 75))
    FRUIT_IMAGE_2 = pygame.image.load("pics/apple animation/apple_2.png")
    FRUIT_IMAGE_2 = pygame.transform.scale(FRUIT_IMAGE_2, (75, 75))
    FRUIT_IMAGE_3 = pygame.image.load("pics/apple animation/apple_3.png")
    FRUIT_IMAGE_3 = pygame.transform.scale(FRUIT_IMAGE_3, (75, 75))
    appleARR = [FRUIT_IMAGE_1, FRUIT_IMAGE_2, FRUIT_IMAGE_3]


    # get a hold of all the background layers
    BG_LAYER_1 = Background(BG_IMAGE_1)
    BG_LAYER_2 = Background(BG_IMAGE_2)
    BG_LAYER_3 = Background(BG_IMAGE_3)
    BG_LAYER_4 = Background(BG_IMAGE_4)
    BG_LAYER_5 = Background(BG_IMAGE_5)


    layer1_group = pygame.sprite.Group()
    layer1_group.add(BG_LAYER_1)
    layer2_group = pygame.sprite.Group()
    layer2_group.add(BG_LAYER_2)
    layer3_group = pygame.sprite.Group()
    layer3_group.add(BG_LAYER_3)
    layer4_group = pygame.sprite.Group()
    layer4_group.add(BG_LAYER_4)
    layer5_group = pygame.sprite.Group()
    layer5_group.add(BG_LAYER_5)

    background_arr = [layer1_group, layer2_group, layer3_group, layer4_group, layer5_group]

    # init tigers and put them to the group can for loop this?
    tiger_image = pygame.image.load("pics/tiger.png")
    tiger_group = pygame.sprite.Group()

    # to do: have to find out the exact place where the tigers cannot be seen so that it cant spawn there
    for tiger in range(5):
        tiger_image = pygame.transform.scale(tiger_image, (random.randint(150, 200), random.randint(150, 200)))
        new_tiger = Tiger(random.randint(100, 900), random.randint(50, 670), tiger_image)
        tiger_group.add(new_tiger)
        layer1_group.add(new_tiger)

    tiger_image = pygame.transform.scale(tiger_image, (random.randint(150, 200), random.randint(150, 200)))
    new_tiger = Tiger(random.randint(100, 900), random.randint(50, 670), tiger_image)
    tiger_group.add(new_tiger)
    tiger_group.add(new_tiger)


    # init crosshair and add to group
    crosshair_image = pygame.image.load("pics/crosshair-target-interface.png")
    crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))
    crosshair = Crosshair(crosshair_image)
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    apple_group = pygame.sprite.Group()

    # to do: have to do tiger moving up in the layers as time goes on
    while True:

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                crosshair.shoot()
                apple = Fruit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], appleARR)
                apple_group.add(apple)
                apple_group.draw(SCREEN)
                apple.animate()

        # if apple.is_animating == False:
        #     apple_group = pygame.sprite.Group()

        if len(tiger_group) < 5:
            tiger_image = pygame.transform.scale(tiger_image, (random.randint(150, 200), random.randint(150, 200)))
            new_tiger = Tiger(random.randint(100, 900), random.randint(50, 670), tiger_image)
            tiger_group.add(new_tiger)
            layer1_group.add(new_tiger)

        pygame.display.flip()
        SCREEN.blit(background, (0, 0))

        # can use this logic to increase the layers of the tiger
        for x in tiger_group:
            x.time += 1
            if x.time > 100:
                if x.layer == 1:
                    layer1_group.remove(x)
                    layer2_group.add(x)
                if x.layer == 2:
                    layer2_group.remove(x)
                    layer3_group.add(x)
                if x.layer == 3:
                    layer3_group.remove(x)
                    layer4_group.add(x)
                if x.layer == 3:
                    layer4_group.remove(x)
                    layer5_group.add(x)
                x.layer += 1
                x.time = 0

        # draws in order
        layer1_group.draw(SCREEN)
        layer2_group.draw(SCREEN)
        layer3_group.draw(SCREEN)
        layer4_group.draw(SCREEN)
        layer5_group.draw(SCREEN)

        crosshair_group.draw(SCREEN)
        crosshair_group.update()

        apple_group.draw(SCREEN)
        apple_group.update()

        clock.tick(60)


start()