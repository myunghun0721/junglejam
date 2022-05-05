from asyncio import proactor_events
from hashlib import new
from turtle import onrelease
import pygame
import sys
from button import Button
from pygame import mixer
import numpy as np
import cv2
import threading
from time import sleep
from collections import deque
from projection import Projection
from audioop import cross
from pickle import TRUE
import random
from re import A
import pygame
import sys
from pygame.locals import *
from moviepy.editor import VideoFileClip


pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
apple_one = False
pygame.display.set_caption("Jungle Jam")


def get_font(size):  # Returns Press-Start-2P in the desired size
    return pygame.font.Font("venv/assets/Montserrat-VariableFont_wght.ttf", size, bold=True)


BG = pygame.image.load("venv/images/jungle_jam.jpg")


# Sound / music / background
music = pygame.mixer.Sound('venv/assets/Jungle_Beatz_V1.mp3')
menuMusic = pygame.mixer.Sound('venv/assets/wav/CapstoneMenu.wav')
foodhit = pygame.mixer.Sound('venv/assets/wav/FruitSplat-Hard.wav')
tigerroar = pygame.mixer.Sound('venv/assets/wav/TigerRoar.wav')
win = pygame.mixer.Sound('venv/assets/wav/CapstoneWin.wav')
lose = pygame.mixer.Sound('venv/assets/wav/CapstoneLose.wav')
firecrackle = pygame.mixer.Sound('venv/assets/wav/FireCrackle.wav')
Ambience = pygame.mixer.Sound('venv/assets/wav/Ambience.wav')
# menuMusic.play()
# foodhit.play()
# tigerroar.play()
# win.play()
# lose.play()
# firecrackle.play()





score_value = 0
cap = cv2.VideoCapture(0, cv2.CAP_DSHOW)

buffer = 20

pts = deque(maxlen=buffer)

counter = 0

(dX, dY) = (0, 0)

direction = ''
pts = deque(maxlen=buffer)

projection = Projection(0, 0, 1, 1)


def leaderboard(status):

    if status:
        clip = VideoFileClip('venv/assets/Win-Screen.mp4')
    else:
        clip = VideoFileClip('venv/assets/Lose-Screen.mp4')

    elapsed_time = 0
    clock = pygame.time.Clock()
    global score_value

    clip.preview()

    while True:

        dt = clock.tick()

        elapsed_time += dt

        if elapsed_time > 20000:
            return main_menu()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()

def play():

    global score_value
    global apple_one

    lost = False

    class Background(pygame.sprite.Sprite):
        def __init__(self, image):
            super().__init__()
            self.image = image
            self.rect = self.image.get_rect()

    # class Tiger(pygame.sprite.Sprite):
    #     def __init__(self, pos_x, pos_y, image):
    #         super().__init__()
    #         self.image = image
    #         self.rect = self.image.get_rect()
    #         self.rect.center = [pos_x, pos_y]
    #         self.x = pos_x
    #         self.y = pos_y
    #         self.xpos = pos_x
    #         self.ypos = pos_y

    #     time = 0
    #     layer = 1
    #     # def update(self):
    #     # self.rect.center = pygame

    class Fruit(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, spriteList):
            super().__init__()
            self.is_animating = False

            self.sprites = spriteList
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.center = [pos_x, pos_y]

        def animate(self):
            self.is_animating = True

        def shoot(self):
            pygame.sprite.spritecollide(apple, tiger_group, True)
            
            

        def update(self):
            if self.is_animating == True:
                self.current_sprite += 1

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                    self.is_animating = False
                    self.kill()

                self.image = self.sprites[int(self.current_sprite)]

    class Animation(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, spriteList):
            super().__init__()
            self.is_animating = True
            self.sprites = spriteList
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [pos_x, pos_y]
            self.xpos = pos_x
            self.ypos = pos_y

        time = 0
        layer = 1

        def animate(self):
            self.is_animating = True

        def update(self):
            if self.is_animating == True:
                self.current_sprite += 1

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                    

                self.image = self.sprites[int(self.current_sprite)]
    
    class Tiger(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, spriteList, layer):
            super().__init__()
            self.is_animating = True
            self.sprites = spriteList
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]
            self.rect = self.image.get_rect()
            self.rect.topleft = [pos_x, pos_y]
            self.xpos = pos_x
            self.ypos = pos_y
            self.layer = layer

        time = 0

        def animate(self):
            self.is_animating = True

        def update(self):
            if self.is_animating == True:
                self.current_sprite += 1

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0
                    

                self.image = self.sprites[int(self.current_sprite)]

    class Plant(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, spriteList):
            super().__init__()
            self.is_animating = True
            self.sprites = spriteList
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.center = [pos_x, pos_y]

    class Animal(pygame.sprite.Sprite):
        def __init__(self, pos_x, pos_y, spriteList):
            super().__init__()
            self.is_animating = True
            self.sprites = spriteList
            self.current_sprite = 0
            self.image = self.sprites[self.current_sprite]

            self.rect = self.image.get_rect()
            self.rect.center = [pos_x, pos_y]

        def update(self):
            if self.is_animating == True:
                self.current_sprite += 1

                if self.current_sprite >= len(self.sprites):
                    self.current_sprite = 0

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
    clock = pygame.time.Clock()

    time_elapsed = 0

    screen_width = 1920
    screen_length = 1080
    screen = pygame.display.set_mode((screen_width, screen_length))
    background = pygame.image.load("pics/black.jpg")

    # disable pygame mouse
    pygame.mouse.set_visible(False)

    # setting background to resolution
    BG_IMAGE_1 = pygame.image.load("pics/background images/jungle_Background_6.png")
    BG_IMAGE_1 = pygame.transform.scale(BG_IMAGE_1, (1920, 1080))
    BG_IMAGE_2 = pygame.image.load("pics/background images/jungle_Background_5.png")
    BG_IMAGE_2 = pygame.transform.scale(BG_IMAGE_2, (1920, 1080))
    BG_IMAGE_3 = pygame.image.load("pics/background images/jungle_Background_4.png")
    BG_IMAGE_3 = pygame.transform.scale(BG_IMAGE_3, (1920, 1080))
    BG_IMAGE_4 = pygame.image.load("pics/background images/jungle_Background_3.png")
    BG_IMAGE_4 = pygame.transform.scale(BG_IMAGE_4, (1920, 1080))
    BG_IMAGE_5 = pygame.image.load("pics/background images/jungle_Background_2.png")
    BG_IMAGE_5 = pygame.transform.scale(BG_IMAGE_5, (1920, 1080))

    # setting fruit to resolution
    FRUIT_IMAGE_1 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_1.png")
    FRUIT_IMAGE_2 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_2.png")
    FRUIT_IMAGE_3 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_3.png")
    FRUIT_IMAGE_4 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_4.png")
    FRUIT_IMAGE_5 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_5.png")
    FRUIT_IMAGE_6 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_6.png")
    FRUIT_IMAGE_7 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_7.png")
    FRUIT_IMAGE_8 = pygame.image.load("pics/final pics/Fruit/Apple-8-Frames/Apple_8.png")

    appleARR = [FRUIT_IMAGE_1, FRUIT_IMAGE_2, FRUIT_IMAGE_3,FRUIT_IMAGE_4, FRUIT_IMAGE_5, FRUIT_IMAGE_6,FRUIT_IMAGE_7, FRUIT_IMAGE_8]


    FRUIT_IMAGE1_1 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_1.png")
    FRUIT_IMAGE1_2 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_2.png")
    FRUIT_IMAGE1_3 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_3.png")
    FRUIT_IMAGE1_4 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_4.png")
    FRUIT_IMAGE1_5 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_5.png")
    FRUIT_IMAGE1_6 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_6.png")
    FRUIT_IMAGE1_7 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_7.png")
    FRUIT_IMAGE1_8 = pygame.image.load("pics/final pics/Fruit/Mango-8-Frames/Mango_8.png")

    mangoARR = [FRUIT_IMAGE1_1, FRUIT_IMAGE1_2, FRUIT_IMAGE1_3,FRUIT_IMAGE1_4, FRUIT_IMAGE1_5, FRUIT_IMAGE1_6,FRUIT_IMAGE1_7, FRUIT_IMAGE1_8]

    FRUIT_IMAGE2_1 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_1.png")
    FRUIT_IMAGE2_2 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_2.png")
    FRUIT_IMAGE2_3 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_3.png")
    FRUIT_IMAGE2_4 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_4.png")
    FRUIT_IMAGE2_5 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_5.png")
    FRUIT_IMAGE2_6 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_6.png")
    FRUIT_IMAGE2_7 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_7.png")
    FRUIT_IMAGE2_8 = pygame.image.load("pics/final pics/Fruit/Orange-8-Frames/orange_8.png")

    orangeARR = [FRUIT_IMAGE2_1, FRUIT_IMAGE2_2, FRUIT_IMAGE2_3,FRUIT_IMAGE2_4, FRUIT_IMAGE2_5, FRUIT_IMAGE2_6,FRUIT_IMAGE2_7, FRUIT_IMAGE2_8]

    FRUIT_IMAGE3_1 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_1.png")
    FRUIT_IMAGE3_2 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_2.png")
    FRUIT_IMAGE3_3 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_3.png")
    FRUIT_IMAGE3_4 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_4.png")
    FRUIT_IMAGE3_5 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_5.png")
    FRUIT_IMAGE3_6 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_6.png")
    FRUIT_IMAGE3_7 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_7.png")
    FRUIT_IMAGE3_8 = pygame.image.load("pics/final pics/Fruit/Pie-8-Frames/Pie_8.png")

    pieARR = [FRUIT_IMAGE3_1, FRUIT_IMAGE3_2, FRUIT_IMAGE3_3,FRUIT_IMAGE3_4, FRUIT_IMAGE3_5, FRUIT_IMAGE3_6,FRUIT_IMAGE3_7, FRUIT_IMAGE3_8]

    FRUIT_IMAGE4_1 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_1.png")
    FRUIT_IMAGE4_2 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_2.png")
    FRUIT_IMAGE4_3 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_3.png")
    FRUIT_IMAGE4_4 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_4.png")
    FRUIT_IMAGE4_5 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_5.png")
    FRUIT_IMAGE4_6 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_6.png")
    FRUIT_IMAGE4_7 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_7.png")
    FRUIT_IMAGE4_8 = pygame.image.load("pics/final pics/Fruit/Pineapple-8-Frames/Pineapple_8.png")

    pineappleARR = [FRUIT_IMAGE4_1, FRUIT_IMAGE4_2, FRUIT_IMAGE4_3,FRUIT_IMAGE4_4, FRUIT_IMAGE4_5, FRUIT_IMAGE4_6,FRUIT_IMAGE4_7, FRUIT_IMAGE4_8]

    FRUIT_IMAGE5_1 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_1.png")
    FRUIT_IMAGE5_2 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_2.png")
    FRUIT_IMAGE5_3 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_3.png")
    FRUIT_IMAGE5_4 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_4.png")
    FRUIT_IMAGE5_5 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_5.png")
    FRUIT_IMAGE5_6 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_6.png")
    FRUIT_IMAGE5_7 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_7.png")
    FRUIT_IMAGE5_8 = pygame.image.load("pics/final pics/Fruit/Pizza-8-Frames/Pizza_8.png")

    pizzaARR = [FRUIT_IMAGE5_1, FRUIT_IMAGE5_2, FRUIT_IMAGE5_3,FRUIT_IMAGE5_4, FRUIT_IMAGE5_5, FRUIT_IMAGE5_6,FRUIT_IMAGE5_7, FRUIT_IMAGE5_8]

    FRUIT_IMAGE6_1 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_1.png")
    FRUIT_IMAGE6_2 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_2.png")
    FRUIT_IMAGE6_3 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_3.png")
    FRUIT_IMAGE6_4 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_4.png")
    FRUIT_IMAGE6_5 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_5.png")
    FRUIT_IMAGE6_6 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_6.png")
    FRUIT_IMAGE6_7 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_7.png")
    FRUIT_IMAGE6_8 = pygame.image.load("pics/final pics/Fruit/Watermelon-8-Frames/Watermelon_8.png")

    watermelonARR = [FRUIT_IMAGE6_1, FRUIT_IMAGE6_2, FRUIT_IMAGE6_3,FRUIT_IMAGE6_4, FRUIT_IMAGE6_5, FRUIT_IMAGE6_6,FRUIT_IMAGE6_7, FRUIT_IMAGE6_8]

    fruits = [appleARR, mangoARR, orangeARR, pieARR, pineappleARR, pizzaARR, watermelonARR]

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
    

    background_arr = [layer1_group, layer2_group, layer3_group, layer4_group, layer5_group]

    # init tiger attack at the end
    TIGER_ATTACK_15FPS_1 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_306.png")
    TIGER_ATTACK_15FPS_2 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_307.png")
    TIGER_ATTACK_15FPS_3 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_308.png")
    TIGER_ATTACK_15FPS_4 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_309.png")
    TIGER_ATTACK_15FPS_5 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_310.png")
    TIGER_ATTACK_15FPS_6 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_311.png")
    TIGER_ATTACK_15FPS_7 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_312.png")
    TIGER_ATTACK_15FPS_8 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_313.png")
    TIGER_ATTACK_15FPS_9 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_314.png")
    TIGER_ATTACK_15FPS_10 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_315.png")
    TIGER_ATTACK_15FPS_11 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_316.png")
    TIGER_ATTACK_15FPS_12 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_317.png")
    TIGER_ATTACK_15FPS_13 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_318.png")
    TIGER_ATTACK_15FPS_14 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_319.png")
    TIGER_ATTACK_15FPS_15 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_320.png")
    TIGER_ATTACK_15FPS_16 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_321.png")
    TIGER_ATTACK_15FPS_17 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_322.png")
    TIGER_ATTACK_15FPS_18 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_323.png")
    TIGER_ATTACK_15FPS_19 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_324.png")
    TIGER_ATTACK_15FPS_20 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_325.png")
    TIGER_ATTACK_15FPS_21 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_326.png")
    TIGER_ATTACK_15FPS_22 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_327.png")
    TIGER_ATTACK_15FPS_23 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_328.png")
    TIGER_ATTACK_15FPS_24 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_329.png")
    TIGER_ATTACK_15FPS_25 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_330.png")
    TIGER_ATTACK_15FPS_26 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_331.png")
    TIGER_ATTACK_15FPS_27 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_332.png")
    TIGER_ATTACK_15FPS_28 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_333.png")
    TIGER_ATTACK_15FPS_29 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_334.png")
    TIGER_ATTACK_15FPS_30 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_335.png")
    TIGER_ATTACK_15FPS_31 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_336.png")
    TIGER_ATTACK_15FPS_32 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_337.png")
    TIGER_ATTACK_15FPS_33 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_338.png")
    TIGER_ATTACK_15FPS_34 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_339.png")
    TIGER_ATTACK_15FPS_35 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_340.png")
    TIGER_ATTACK_15FPS_36 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_341.png")
    TIGER_ATTACK_15FPS_37 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_342.png")
    TIGER_ATTACK_15FPS_38 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_343.png")
    TIGER_ATTACK_15FPS_39 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_344.png")
    TIGER_ATTACK_15FPS_40 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_345.png")
    TIGER_ATTACK_15FPS_41 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_346.png")
    TIGER_ATTACK_15FPS_42 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_347.png")
    TIGER_ATTACK_15FPS_43 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_348.png")
    TIGER_ATTACK_15FPS_44 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_349.png")
    TIGER_ATTACK_15FPS_45 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_350.png")
    TIGER_ATTACK_15FPS_46 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_351.png")
    TIGER_ATTACK_15FPS_47 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_352.png")
    TIGER_ATTACK_15FPS_48 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_353.png")
    TIGER_ATTACK_15FPS_49 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_354.png")
    TIGER_ATTACK_15FPS_50 = pygame.image.load("pics/Tiger_Attack_15fps/Tiger full 2_355.png")

    tigerAttack15FPSarr = [TIGER_ATTACK_15FPS_1, TIGER_ATTACK_15FPS_2, TIGER_ATTACK_15FPS_3, TIGER_ATTACK_15FPS_4, TIGER_ATTACK_15FPS_5, TIGER_ATTACK_15FPS_6, TIGER_ATTACK_15FPS_7, TIGER_ATTACK_15FPS_8, TIGER_ATTACK_15FPS_9, TIGER_ATTACK_15FPS_10, TIGER_ATTACK_15FPS_11, TIGER_ATTACK_15FPS_12, TIGER_ATTACK_15FPS_13, TIGER_ATTACK_15FPS_14, TIGER_ATTACK_15FPS_15, TIGER_ATTACK_15FPS_16, TIGER_ATTACK_15FPS_17, TIGER_ATTACK_15FPS_18, TIGER_ATTACK_15FPS_19, TIGER_ATTACK_15FPS_20, TIGER_ATTACK_15FPS_21, TIGER_ATTACK_15FPS_22, TIGER_ATTACK_15FPS_23, TIGER_ATTACK_15FPS_24, TIGER_ATTACK_15FPS_25,
                           TIGER_ATTACK_15FPS_26, TIGER_ATTACK_15FPS_27, TIGER_ATTACK_15FPS_28, TIGER_ATTACK_15FPS_29, TIGER_ATTACK_15FPS_30, TIGER_ATTACK_15FPS_31, TIGER_ATTACK_15FPS_32, TIGER_ATTACK_15FPS_33, TIGER_ATTACK_15FPS_34, TIGER_ATTACK_15FPS_35, TIGER_ATTACK_15FPS_36, TIGER_ATTACK_15FPS_37, TIGER_ATTACK_15FPS_38, TIGER_ATTACK_15FPS_39, TIGER_ATTACK_15FPS_40, TIGER_ATTACK_15FPS_41, TIGER_ATTACK_15FPS_42, TIGER_ATTACK_15FPS_43, TIGER_ATTACK_15FPS_44, TIGER_ATTACK_15FPS_45, TIGER_ATTACK_15FPS_46, TIGER_ATTACK_15FPS_47, TIGER_ATTACK_15FPS_48, TIGER_ATTACK_15FPS_49, TIGER_ATTACK_15FPS_50, ]

    BUSH1 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 201.png")
    BUSH2 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 202.png")
    BUSH3 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 203.png")
    BUSH4 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 204.png")
    BUSH5 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 205.png")
    BUSH6 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 206.png")
    BUSH7 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 207.png")
    BUSH8 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 208.png")
    BUSH9 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 209.png")
    BUSH10 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 210.png")
    BUSH11 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 211.png")
    BUSH12 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 212.png")
    BUSH13 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 213.png")
    BUSH14 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 214.png")
    BUSH15 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 215.png")
    BUSH16 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 216.png")
    BUSH17 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 217.png")
    BUSH18 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 218.png")
    BUSH19 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 219.png")
    BUSH20 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 220.png")
    BUSH21 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 221.png")
    BUSH22 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 222.png")
    BUSH23 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 223.png")
    BUSH24 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 224.png")
    BUSH25 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 225.png")
    BUSH26 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 226.png")
    BUSH27 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 227.png")
    BUSH28 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 228.png")
    BUSH29 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 229.png")
    BUSH30 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 230.png")
    BUSH31 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 231.png")
    BUSH32 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 232.png")
    BUSH33 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 233.png")
    BUSH34 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 234.png")
    BUSH35 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 235.png")
    BUSH36 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 236.png")
    BUSH37 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 237.png")
    BUSH38 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 238.png")
    BUSH39 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 239.png")
    BUSH40 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 240.png")
    BUSH41 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 241.png")
    BUSH42 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 242.png")
    BUSH43 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 243.png")
    BUSH44 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 244.png")
    BUSH45 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 245.png")
    BUSH46 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 246.png")
    BUSH47 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 247.png")
    BUSH48 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 248.png")
    BUSH49 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 249.png")
    BUSH50 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 250.png")
    BUSH51 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 251.png")
    BUSH52 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 252.png")
    BUSH53 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 253.png")
    BUSH54 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 254.png")
    BUSH55 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 255.png")
    BUSH56 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 256.png")
    BUSH57 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 257.png")
    BUSH58 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 258.png")
    BUSH59 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 259.png")
    BUSH60 = pygame.image.load("pics/final pics/Plants/Bush Animation 15 frames/Bush-Groups 260.png")

    bushArr = [BUSH1, BUSH2, BUSH3, BUSH4, BUSH5, BUSH6, BUSH7, BUSH8, BUSH9, BUSH10, BUSH11, BUSH12, BUSH13, BUSH14, BUSH15, BUSH16, BUSH17, BUSH18, BUSH19, BUSH20, BUSH21, BUSH22, BUSH23, BUSH24, BUSH25, BUSH26, BUSH27, BUSH28, BUSH29, BUSH30,
               BUSH31, BUSH32, BUSH33, BUSH34, BUSH35, BUSH36, BUSH37, BUSH38, BUSH39, BUSH40, BUSH41, BUSH42, BUSH43, BUSH44, BUSH45, BUSH46, BUSH47, BUSH48, BUSH49, BUSH50, BUSH51, BUSH52, BUSH53, BUSH54, BUSH55, BUSH56, BUSH57, BUSH58, BUSH59, BUSH60]

    GRASS1 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group01.png")
    GRASS2 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group02.png")
    GRASS3 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group03.png")
    GRASS4 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group04.png")
    GRASS5 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group05.png")
    GRASS6 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group06.png")
    GRASS7 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group07.png")
    GRASS8 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group08.png")
    GRASS9 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group09.png")
    GRASS10 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group10.png")
    GRASS11 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group11.png")
    GRASS12 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group12.png")
    GRASS13 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group13.png")
    GRASS14 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group14.png")
    GRASS15 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group15.png")
    GRASS16 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group16.png")
    GRASS17 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group17.png")
    GRASS18 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group18.png")
    GRASS19 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group19.png")
    GRASS20 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group20.png")
    GRASS21 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group21.png")
    GRASS22 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group22.png")
    GRASS23 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group23.png")
    GRASS24 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group24.png")
    GRASS25 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group25.png")
    GRASS26 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group26.png")
    GRASS27 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group27.png")
    GRASS28 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group28.png")
    GRASS29 = pygame.image.load("pics/final pics/Plants/Tall grass Animation 15 frames/Tall-Grass-Group29.png")

    grassArr = [GRASS1, GRASS2, GRASS3, GRASS4, GRASS5, GRASS6, GRASS7, GRASS8, GRASS9, GRASS10, GRASS11, GRASS12, GRASS13, GRASS14, GRASS15,
                GRASS16, GRASS17, GRASS18, GRASS19, GRASS20, GRASS21, GRASS22, GRASS23, GRASS24, GRASS25, GRASS26, GRASS27, GRASS28, GRASS29]

    VINE1 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group01.png")
    VINE2 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group02.png")
    VINE3 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group03.png")
    VINE4 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group04.png")
    VINE5 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group05.png")
    VINE6 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group06.png")
    VINE7 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group07.png")
    VINE8 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group08.png")
    VINE9 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group09.png")
    VINE10 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group10.png")
    VINE11 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group11.png")
    VINE12 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group12.png")
    VINE13 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group13.png")
    VINE14 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group14.png")
    VINE15 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group15.png")
    VINE16 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group16.png")
    VINE17 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group17.png")
    VINE18 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group18.png")
    VINE19 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group19.png")
    VINE20 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group20.png")
    VINE21 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group21.png")
    VINE22 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group22.png")
    VINE23 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group23.png")
    VINE24 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group24.png")
    VINE25 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group25.png")
    VINE26 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group26.png")
    VINE27 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group27.png")
    VINE28 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group28.png")
    VINE29 = pygame.image.load("pics/final pics/Plants/Vine animation 15 frames/Vine-Group29.png")

    vineArr = [VINE1, VINE2, VINE3, VINE4, VINE5, VINE6, VINE7, VINE8, VINE9, VINE10, VINE11, VINE12, VINE13, VINE14, VINE15,
               VINE16, VINE17, VINE18, VINE19, VINE20, VINE21, VINE22, VINE23, VINE24, VINE25, VINE26, VINE27, VINE28, VINE29, ]

    TIGER_SHADOW1 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full01.png")
    TIGER_SHADOW2 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full02.png")
    TIGER_SHADOW3 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full03.png")
    TIGER_SHADOW4 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full04.png")
    TIGER_SHADOW5 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full05.png")
    TIGER_SHADOW6 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full06.png")
    TIGER_SHADOW7 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full07.png")
    TIGER_SHADOW8 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full08.png")
    TIGER_SHADOW9 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full09.png")
    TIGER_SHADOW10 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full10.png")
    TIGER_SHADOW11 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full11.png")
    TIGER_SHADOW12 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full12.png")
    TIGER_SHADOW13 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full13.png")
    TIGER_SHADOW14 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full14.png")
    TIGER_SHADOW15 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full15.png")
    TIGER_SHADOW16 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full16.png")
    TIGER_SHADOW17 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full17.png")
    TIGER_SHADOW18 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full18.png")
    TIGER_SHADOW19 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full19.png")
    TIGER_SHADOW20 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full20.png")
    TIGER_SHADOW21 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full21.png")
    TIGER_SHADOW22 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full22.png")
    TIGER_SHADOW23 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full23.png")
    TIGER_SHADOW24 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full24.png")
    TIGER_SHADOW25 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full25.png")
    TIGER_SHADOW26 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full26.png")
    TIGER_SHADOW27 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full27.png")
    TIGER_SHADOW28 = pygame.image.load("pics/final pics/Tiger/Tiger Shadow No Glowing Eyes 15 frames/Tiger full28.png")
    
    tigershadowArr = [TIGER_SHADOW1, TIGER_SHADOW2, TIGER_SHADOW3, TIGER_SHADOW4, TIGER_SHADOW5, TIGER_SHADOW6, TIGER_SHADOW7, TIGER_SHADOW8, TIGER_SHADOW9, TIGER_SHADOW10, TIGER_SHADOW11, TIGER_SHADOW12, TIGER_SHADOW13, TIGER_SHADOW14,
                    TIGER_SHADOW15, TIGER_SHADOW16, TIGER_SHADOW17, TIGER_SHADOW18, TIGER_SHADOW19, TIGER_SHADOW20, TIGER_SHADOW21, TIGER_SHADOW22, TIGER_SHADOW23, TIGER_SHADOW24, TIGER_SHADOW25, TIGER_SHADOW26, TIGER_SHADOW27, TIGER_SHADOW28, ]
    


    TIGER_EYES1 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 501.png")
    TIGER_EYES2 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 502.png")
    TIGER_EYES3 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 503.png")
    TIGER_EYES4 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 504.png")
    TIGER_EYES5 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 505.png")
    TIGER_EYES6 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 506.png")
    TIGER_EYES7 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 507.png")
    TIGER_EYES8 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 508.png")
    TIGER_EYES9 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 509.png")
    TIGER_EYES10 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 510.png")
    TIGER_EYES11 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 511.png")
    TIGER_EYES12 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 512.png")
    TIGER_EYES13 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 513.png")
    TIGER_EYES14 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 514.png")
    TIGER_EYES15 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 515.png")
    TIGER_EYES16 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 516.png")
    TIGER_EYES17 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 517.png")
    TIGER_EYES18 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 518.png")
    TIGER_EYES19 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 519.png")
    TIGER_EYES20 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 520.png")
    TIGER_EYES21 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 521.png")
    TIGER_EYES22 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 522.png")
    TIGER_EYES23 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 523.png")
    TIGER_EYES24 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 524.png")
    TIGER_EYES25 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 525.png")
    TIGER_EYES26 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 526.png")
    TIGER_EYES27 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 527.png")
    TIGER_EYES28 = pygame.image.load("pics/final pics/Tiger/Tiger Glowing Eyes 15 Frames/Pre-comp 528.png")
    
    tigereyesArr = [TIGER_EYES1, TIGER_EYES2, TIGER_EYES3, TIGER_EYES4, TIGER_EYES5, TIGER_EYES6, TIGER_EYES7, TIGER_EYES8, TIGER_EYES9, TIGER_EYES10, TIGER_EYES11, TIGER_EYES12, TIGER_EYES13, TIGER_EYES14,
                TIGER_EYES15, TIGER_EYES16, TIGER_EYES17, TIGER_EYES18, TIGER_EYES19, TIGER_EYES20, TIGER_EYES21, TIGER_EYES22, TIGER_EYES23, TIGER_EYES24, TIGER_EYES25, TIGER_EYES26, TIGER_EYES27, TIGER_EYES28, ]
    
    TIGER_IDLE1 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle01.png")
    TIGER_IDLE2 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle02.png")
    TIGER_IDLE3 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle03.png")
    TIGER_IDLE4 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle04.png")
    TIGER_IDLE5 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle05.png")
    TIGER_IDLE6 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle06.png")
    TIGER_IDLE7 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle07.png")
    TIGER_IDLE8 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle08.png")
    TIGER_IDLE9 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle09.png")
    TIGER_IDLE10 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle10.png")
    TIGER_IDLE11 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle11.png")
    TIGER_IDLE12 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle12.png")
    TIGER_IDLE13 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle13.png")
    TIGER_IDLE14 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle14.png")
    TIGER_IDLE15 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle15.png")
    TIGER_IDLE16 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle16.png")
    TIGER_IDLE17 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle17.png")
    TIGER_IDLE18 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle18.png")
    TIGER_IDLE19 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle19.png")
    TIGER_IDLE20 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle20.png")
    TIGER_IDLE21 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle21.png")
    TIGER_IDLE22 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle22.png")
    TIGER_IDLE23 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle23.png")
    TIGER_IDLE24 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle24.png")
    TIGER_IDLE25 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle25.png")
    TIGER_IDLE26 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle26.png")
    TIGER_IDLE27 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle27.png")
    TIGER_IDLE28 = pygame.image.load("pics/final pics/Tiger/Idle Tiger 15 frames/Tiger Idle28.png")
    
    tigeridleArr = [TIGER_IDLE1, TIGER_IDLE2, TIGER_IDLE3, TIGER_IDLE4, TIGER_IDLE5, TIGER_IDLE6, TIGER_IDLE7, TIGER_IDLE8, TIGER_IDLE9, TIGER_IDLE10, TIGER_IDLE11, TIGER_IDLE12, TIGER_IDLE13, TIGER_IDLE14,
                TIGER_IDLE15, TIGER_IDLE16, TIGER_IDLE17, TIGER_IDLE18, TIGER_IDLE19, TIGER_IDLE20, TIGER_IDLE21, TIGER_IDLE22, TIGER_IDLE23, TIGER_IDLE24, TIGER_IDLE25, TIGER_IDLE26, TIGER_IDLE27, TIGER_IDLE28, ]
    
    TIGER_IMP1 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_101.png")
    TIGER_IMP2 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_102.png")
    TIGER_IMP3 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_103.png")
    TIGER_IMP4 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_104.png")
    TIGER_IMP5 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_105.png")
    TIGER_IMP6 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_106.png")
    TIGER_IMP7 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_107.png")
    TIGER_IMP8 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_108.png")
    TIGER_IMP9 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_109.png")
    TIGER_IMP10 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_110.png")
    TIGER_IMP11 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_111.png")
    TIGER_IMP12 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_112.png")
    TIGER_IMP13 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_113.png")
    TIGER_IMP14 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_114.png")
    TIGER_IMP15 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_115.png")
    TIGER_IMP16 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_116.png")
    TIGER_IMP17 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_117.png")
    TIGER_IMP18 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_118.png")
    TIGER_IMP19 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_119.png")
    TIGER_IMP20 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_120.png")
    TIGER_IMP21 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_121.png")
    TIGER_IMP22 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_122.png")
    TIGER_IMP23 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_123.png")
    TIGER_IMP24 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_124.png")
    TIGER_IMP25 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_125.png")
    TIGER_IMP26 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_126.png")
    TIGER_IMP27 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_127.png")
    TIGER_IMP28 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_128.png")
    TIGER_IMP29 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_129.png")
    TIGER_IMP30 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_130.png")
    TIGER_IMP31 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_131.png")
    TIGER_IMP32 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_132.png")
    TIGER_IMP33 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_133.png")
    TIGER_IMP34 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_134.png")
    TIGER_IMP35 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_135.png")
    TIGER_IMP36 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_136.png")
    TIGER_IMP37 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_137.png")
    TIGER_IMP38 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_138.png")
    TIGER_IMP39 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_139.png")
    TIGER_IMP40 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_140.png")
    TIGER_IMP41 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_141.png")
    TIGER_IMP42 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_142.png")
    TIGER_IMP43 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_143.png")
    TIGER_IMP44 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_144.png")
    TIGER_IMP45 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_145.png")
    TIGER_IMP46 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_146.png")
    TIGER_IMP47 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_147.png")
    TIGER_IMP48 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_148.png")
    TIGER_IMP49 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_149.png")
    TIGER_IMP50 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_150.png")
    TIGER_IMP51 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_151.png")
    TIGER_IMP52 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_152.png")
    TIGER_IMP53 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_153.png")
    TIGER_IMP54 = pygame.image.load("pics/final pics/Tiger/Idle Tiger Impatient 15 frames/Tiger full 2_154.png")
    
    tigerimpArr = [TIGER_IMP1, TIGER_IMP2, TIGER_IMP3, TIGER_IMP4, TIGER_IMP5, TIGER_IMP6, TIGER_IMP7, TIGER_IMP8, TIGER_IMP9, TIGER_IMP10, TIGER_IMP11, TIGER_IMP12, TIGER_IMP13, TIGER_IMP14, TIGER_IMP15, TIGER_IMP16, TIGER_IMP17, TIGER_IMP18, TIGER_IMP19, TIGER_IMP20, TIGER_IMP21, TIGER_IMP22, TIGER_IMP23, TIGER_IMP24, TIGER_IMP25, TIGER_IMP26, TIGER_IMP27,
                TIGER_IMP28, TIGER_IMP29, TIGER_IMP30, TIGER_IMP31, TIGER_IMP32, TIGER_IMP33, TIGER_IMP34, TIGER_IMP35, TIGER_IMP36, TIGER_IMP37, TIGER_IMP38, TIGER_IMP39, TIGER_IMP40, TIGER_IMP41, TIGER_IMP42, TIGER_IMP43, TIGER_IMP44, TIGER_IMP45, TIGER_IMP46, TIGER_IMP47, TIGER_IMP48, TIGER_IMP49, TIGER_IMP50, TIGER_IMP51, TIGER_IMP52, TIGER_IMP53, TIGER_IMP54, ]

    Toucan1 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_101.png")
    Toucan2 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_102.png")
    Toucan3 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_103.png")
    Toucan4 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_104.png")
    Toucan5 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_105.png")
    Toucan6 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_106.png")
    Toucan7 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_107.png")
    Toucan8 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_108.png")
    Toucan9 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_109.png")
    Toucan10 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_110.png")
    Toucan11 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_111.png")
    Toucan12 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_112.png")
    Toucan13 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_113.png")
    Toucan14 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_114.png")
    Toucan15 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_115.png")
    Toucan16 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_116.png")
    Toucan17 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_117.png")
    Toucan18 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_118.png")
    Toucan19 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_119.png")
    Toucan20 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_120.png")
    Toucan21 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_121.png")
    Toucan22 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_122.png")
    Toucan23 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_123.png")
    Toucan24 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_124.png")
    Toucan25 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_125.png")
    Toucan26 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_126.png")
    Toucan27 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_127.png")
    Toucan28 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_128.png")
    Toucan29 = pygame.image.load("pics/Toucan/Tucan Sprite ai 2_129.png")


    

    toucanARR = [Toucan1,Toucan2,Toucan3,Toucan4,Toucan5,Toucan6,Toucan7,Toucan8,Toucan9,Toucan10,Toucan11,Toucan12,Toucan13,Toucan14,Toucan15,Toucan16,Toucan17,Toucan18,Toucan19,Toucan20,Toucan21,Toucan22,Toucan23,Toucan24,Toucan25,Toucan26,Toucan27,Toucan28,Toucan29,]
    # toucanARR = [Toucan_IMP1,Toucan_IMP2,Toucan_IMP3,Toucan_IMP4,Toucan_IMP5,Toucan_IMP6,Toucan_IMP7,Toucan_IMP8,Toucan_IMP9,Toucan_IMP10,Toucan_IMP11,Toucan_IMP12,Toucan_IMP13,Toucan_IMP14,Toucan_IMP15,Toucan_IMP16,Toucan_IMP17,Toucan_IMP18,Toucan_IMP19,Toucan_IMP20,Toucan_IMP21,Toucan_IMP22,Toucan_IMP23,Toucan_IMP24,Toucan_IMP25,Toucan_IMP26,Toucan_IMP27,Toucan_IMP28,Toucan_IMP29,Toucan_IMP30]
 
    Lemur1 = pygame.image.load("pics/Lemur/lemur-sprite-small00.png")
    Lemur2 = pygame.image.load("pics/Lemur/lemur-sprite-small01.png")
    Lemur3 = pygame.image.load("pics/Lemur/lemur-sprite-small02.png")
    Lemur4 = pygame.image.load("pics/Lemur/lemur-sprite-small03.png")
    Lemur5 = pygame.image.load("pics/Lemur/lemur-sprite-small04.png")
    Lemur6 = pygame.image.load("pics/Lemur/lemur-sprite-small05.png")
    Lemur7 = pygame.image.load("pics/Lemur/lemur-sprite-small06.png")
    Lemur8 = pygame.image.load("pics/Lemur/lemur-sprite-small07.png")
    Lemur9 = pygame.image.load("pics/Lemur/lemur-sprite-small08.png")
    Lemur10 = pygame.image.load("pics/Lemur/lemur-sprite-small09.png")
    Lemur11 = pygame.image.load("pics/Lemur/lemur-sprite-small10.png")
    Lemur12 = pygame.image.load("pics/Lemur/lemur-sprite-small11.png")
    Lemur13 = pygame.image.load("pics/Lemur/lemur-sprite-small12.png")
    Lemur14 = pygame.image.load("pics/Lemur/lemur-sprite-small13.png")
    Lemur15 = pygame.image.load("pics/Lemur/lemur-sprite-small14.png")
    Lemur16 = pygame.image.load("pics/Lemur/lemur-sprite-small15.png")
    Lemur17 = pygame.image.load("pics/Lemur/lemur-sprite-small16.png")
    Lemur18 = pygame.image.load("pics/Lemur/lemur-sprite-small17.png")
    Lemur19 = pygame.image.load("pics/Lemur/lemur-sprite-small18.png")
    Lemur20 = pygame.image.load("pics/Lemur/lemur-sprite-small19.png")
    Lemur21 = pygame.image.load("pics/Lemur/lemur-sprite-small20.png")
    Lemur22 = pygame.image.load("pics/Lemur/lemur-sprite-small21.png")
    Lemur23 = pygame.image.load("pics/Lemur/lemur-sprite-small22.png")
    Lemur24 = pygame.image.load("pics/Lemur/lemur-sprite-small23.png")
    Lemur25 = pygame.image.load("pics/Lemur/lemur-sprite-small24.png")
    Lemur26 = pygame.image.load("pics/Lemur/lemur-sprite-small25.png")
    Lemur27 = pygame.image.load("pics/Lemur/lemur-sprite-small26.png")
    Lemur28 = pygame.image.load("pics/Lemur/lemur-sprite-small27.png")
    Lemur29 = pygame.image.load("pics/Lemur/lemur-sprite-small28.png")
    Lemur30 = pygame.image.load("pics/Lemur/lemur-sprite-small29.png")
    Lemur31 = pygame.image.load("pics/Lemur/lemur-sprite-small30.png")
    Lemur32 = pygame.image.load("pics/Lemur/lemur-sprite-small31.png")
    Lemur33 = pygame.image.load("pics/Lemur/lemur-sprite-small32.png")
    Lemur34 = pygame.image.load("pics/Lemur/lemur-sprite-small33.png")
    Lemur35 = pygame.image.load("pics/Lemur/lemur-sprite-small34.png")
    Lemur36 = pygame.image.load("pics/Lemur/lemur-sprite-small35.png")
    Lemur37 = pygame.image.load("pics/Lemur/lemur-sprite-small36.png")
    Lemur38 = pygame.image.load("pics/Lemur/lemur-sprite-small37.png")
    Lemur39 = pygame.image.load("pics/Lemur/lemur-sprite-small38.png")
    Lemur40 = pygame.image.load("pics/Lemur/lemur-sprite-small39.png")
    Lemur41 = pygame.image.load("pics/Lemur/lemur-sprite-small40.png")
    Lemur42 = pygame.image.load("pics/Lemur/lemur-sprite-small41.png")
    Lemur43 = pygame.image.load("pics/Lemur/lemur-sprite-small42.png")
    Lemur44 = pygame.image.load("pics/Lemur/lemur-sprite-small43.png")
    Lemur45 = pygame.image.load("pics/Lemur/lemur-sprite-small44.png")
   
    lemurARR = [Lemur1,Lemur2,Lemur3,Lemur4,Lemur5,Lemur6,Lemur7,Lemur8,Lemur9,Lemur10,Lemur11,Lemur12,Lemur13,Lemur14,Lemur15,Lemur16,Lemur17,Lemur18,Lemur19,Lemur20,Lemur21,Lemur22,Lemur23,Lemur24,Lemur25,Lemur26,Lemur27,Lemur28,Lemur29,Lemur30,Lemur31,Lemur32,Lemur33,Lemur34,Lemur35,Lemur36,Lemur37,Lemur38,Lemur39,Lemur40,Lemur41,Lemur42,Lemur43,Lemur44,Lemur45,]
    
 # init tigers and put them to the group can for loop this?
    tiger_group = pygame.sprite.Group()

    toucan_group = pygame.sprite.Group()


   # to do: have to find out the exact place where the tigers cannot be seen so that it cant spawn there
    for tiger in range(3):
        new_tiger = Tiger(random.randint(200, 1500), random.randint(400, 500), tigershadowArr, 1)
        tiger_group.add(new_tiger)
        layer1_group.add(new_tiger)

    # init crosshair and add to group
    crosshair_image = pygame.image.load("pics/crosshair-target-interface.png")
    crosshair_image = pygame.transform.scale(crosshair_image, (50, 50))
    crosshair = Crosshair(crosshair_image)
    crosshair_group = pygame.sprite.Group()
    crosshair_group.add(crosshair)

    apple_group = pygame.sprite.Group()
    attack_group = pygame.sprite.Group()

    bush = Plant(1700, 900, bushArr)
    grass = Plant(920, 900, grassArr)
    vine = Plant(200, 900, vineArr)

    plant_group = pygame.sprite.Group()
    plant_group.add(bush, grass, vine)

    toucan = Animal(550,200, toucanARR)
    lemur = Animal(400, 750, lemurARR)
    toucan_group.add(toucan)
    toucan_group.add(lemur)
    

    while True:

        time_elapsed += 1

        print(time_elapsed)

        if time_elapsed > 700:
            return leaderboard(True)


        ret, frame = cap.read()

        # Blur the frame using a Gaussian blur. Removes excess noise.
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

        # Convert frame to HSV, HSV allows better segmentation
        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)

        # Create a mask for all red elements in capture
        lower_red = np.array([0, 80, 80])
        upper_red = np.array([5, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red = np.array([175, 80, 80])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask = mask0+mask1


        # Create a mask for all red elements in capture
        # lower_red = np.array([50 ,80, 80])
        # upper_red = np.array([50, 255, 255])
        # mask0 = cv2.inRange(hsv, lower_red, upper_red)
        # mask = mask0

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
            if 15 > radius > 1:
                # Draw circles around the object as well as its centre
                cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 2)
                cv2.circle(frame, center, 5, (0, 255, 255), -1)
                cv2.putText(frame, "Center: {}".format(center), (int(x - 20), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
                # cv2.putText(frame, "Y: {}".format(int(y)), (int(x - 20), int(y+ 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255,255,255))

                # cv2.rectangle(frame, (400,200), (500,300), (255,0,0), 2)

                # Append the detected object in the frame to pts deque structure
                pts.appendleft(center)

                print(radius)

                # print(x, y, radius)
            # print(radius)

                if 1 < radius <= 9:
                    if projection.collision(x, y):
                        print("hit the wall at x: " + str(x) + " y: " + str(y))

                        projx = [0,1920]
                        projy = [0,1080]
                        camerax = [0, projection.w]
                        cameray = [0, projection.h]

                        x = np.interp(x, camerax, projx)
                        y = np.interp(y, cameray, projy)

                        # print(x,y)
                        if not apple_one:
                            ranNum = random.randint(0, 5)
                            apple_one = True
                            apple = Fruit(x, y, fruits[ranNum])
                            apple.animate()
                            apple.shoot()
                            apple_group.add(apple)
                            apple_group.draw(screen)
                            foodhit.play()

                           

        # Show the output frame.
        # cv2.imshow('Window- Direction Detection', frame)
        apple_one = False

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                ranNum = random.randint(0, 5)
                crosshair.shoot()
                apple = Fruit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], fruits[ranNum])
                apple_group.add(apple)
                apple_group.draw(screen)
                apple.animate()

        # can change 5 to become the difficulty as time goes on by thousands and just / 1000 for the number
        # if len(tiger_group) < 3:
        #     new_tiger = Animation(random.randint(300, 1700), random.randint(700, 800), tigershadowArr)
        #     tiger_group.add(new_tiger)
        #     layer1_group.add(new_tiger)

        pygame.display.flip()
        screen.blit(background, (0, 0))

        if len(tiger_group) < 3:
            # print(len(tiger_group))
            new_tiger = Tiger(random.randint(200, 1500), random.randint(400, 500), tigershadowArr, 1)
            tiger_group.add(new_tiger)
            layer1_group.add(new_tiger)

        # can use this logic to increase the layers of the tiger
        for x in tiger_group:
            x.time += 1
            if x.time >= 50:
                if x.layer == 1:
                    layer1_group.remove(x)
                    tiger_group.remove(x)
                    x.kill()
                    xp = x.xpos
                    yp = x.ypos
                    new_tiger = Tiger(xp, yp, tigereyesArr, 2)
                    tiger_group.add(new_tiger)
                    layer2_group.add(new_tiger)
                if x.layer == 2:
                    tiger_group.remove(x)
                    layer2_group.remove(x)
                    x.kill()
                    xp = x.xpos
                    yp = x.ypos
                    new_tiger = Tiger(xp, yp, tigeridleArr, 3)
                    tiger_group.add(new_tiger)
                    layer3_group.add(new_tiger)
                    tigerroar.play()
                if x.layer == 3:
                    tiger_group.remove(x)
                    layer3_group.remove(x)
                    x.kill()
                    xp = x.xpos
                    yp = x.ypos
                    new_tiger = Tiger(xp, yp, tigerimpArr, 4)
                    tiger_group.add(new_tiger)
                    layer4_group.add(new_tiger)
                if x.layer == 4:
                    tiger_group.remove(x)
                    layer4_group.remove(x)
                    x.kill()
                    tiger_group.add(x)
                    layer5_group.add(x)
                    return leaderboard(False)

                x.time = 0 




        # draws in order
        layer1_group.draw(screen)
        layer2_group.draw(screen)
        layer3_group.draw(screen)
        layer4_group.draw(screen)
        layer5_group.draw(screen)

        # tiger_group.draw(screen)
        tiger_group.update()
        

        plant_group.draw(screen)
        plant_group.update()

        crosshair_group.draw(screen)
        crosshair_group.update()

        attack_group.draw(screen)
        attack_group.update()

        apple_group.draw(screen)
        apple_group.update()

        toucan_group.draw(screen)
        toucan_group.update()

        clock.tick()

        cv2.imshow('Window- Direction Detection', frame)


def main_menu():
    # prevents jumping to the play screen
    sleep(0.7)
    Ambience.play()
    music.play()
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
                cv2.putText(frame, "Center: {}".format(center), (int(x - 20), int(y - 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))

                # Append the detected object in the frame to pts deque structure
                pts.appendleft(center)

                # print(x, y, radius)
            # print(radius)
                if 5 < radius <= 40:
                    print("hit the wall at x: " + str(x) + " y: " + str(y))
                    # if(x < 500 and y < 300 and x > 400 and y > 200):
                    cv2.destroyAllWindows()
                    foodhit.play()
                    play()
                    return

        # Show the output frame.
        cv2.imshow('Window- Direction Detection', frame)

        SCREEN.blit(BG, (0, 0))
        PLAY_TEXT = get_font(48).render("aim anywhere to start", True, "#ffffff")
        PLAY_RECT = PLAY_TEXT.get_rect(center=(960, 800))
        SCREEN.blit(PLAY_TEXT, PLAY_RECT)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.display.update()


def start():
    PLAY_MOUSE_POS = pygame.mouse.get_pos()

    SCREEN.fill("red")

    pygame.display.update()

    count = 0

    while count < 10:

        ret, frame = cap.read()

        # Blur the frame using a Gaussian blur. Removes excess noise.
        blurred_frame = cv2.GaussianBlur(frame, (5, 5), 0)

        hsv = cv2.cvtColor(blurred_frame, cv2.COLOR_BGR2HSV)
        lower_red = np.array([0, 80, 80])
        upper_red = np.array([5, 255, 255])
        mask0 = cv2.inRange(hsv, lower_red, upper_red)
        lower_red = np.array([175, 80, 80])
        upper_red = np.array([180, 255, 255])
        mask1 = cv2.inRange(hsv, lower_red, upper_red)
        mask = mask0+mask1

        # hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
        # lower_green = np.array([50, 100, 100])
        # upper_green = np.array([70, 255, 255])
        # mask = cv2.inRange(hsv, lower_green, upper_green)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        sleep(1)

        if len(contours) > 0:
            # cv2.drawContours(frame, contours, -1, (0,255,0), 5)

            # find the biggest countour (c) by the area
            c = max(contours, key=cv2.contourArea)
            x, y, w, h = cv2.boundingRect(c)

            # draw the biggest contour (c) in green
            rect = cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 0), 2)

            # find center of object
            M = cv2.moments(c)
            divider = M["m00"]
            if(divider == 0):
                divider = 1
            cX = int(M["m10"] / divider)
            cY = int(M["m01"] / divider)

            # display center object with white color
            cv2.circle(frame, (cX, cY), 7, (255, 255, 255), -1)
            cv2.putText(frame, "X: {}".format(cX), (int(cX - 20), int(cY - 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            cv2.putText(frame, "Y: {}".format(cY), (int(cX - 20), int(cY + 20)), cv2.FONT_HERSHEY_PLAIN, 1, (255, 255, 255))
            global projection
            projection = Projection(cX, cY, w, h)

        count += 1
        cv2.imshow('frame', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    #print("x: " + projection.x + "    y: " + projection.y)

    print(projection.x)
    print(projection.y)

    # leaderboard()
    main_menu()
    # play()

# play()
start()
