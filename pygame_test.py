from audioop import cross
from pickle import TRUE
import random
from re import A
import pygame
import sys
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
        self.rect.center = [pos_x, pos_y]

    def animate(self):
        self.is_animating = True

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.5

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
                self.kill()

            self.image = self.sprites[int(self.current_sprite)]


class Animation(pygame.sprite.Sprite):
    def __init__(self, pos_x, pos_y, spriteList):
        super().__init__()
        self.is_animating = False
        self.sprites = spriteList
        self.current_sprite = 0
        self.image = self.sprites[self.current_sprite]

        self.rect = self.image.get_rect()
        self.rect.topleft = [pos_x, pos_y]
        # self.time = 0.2

    def animate(self):
        self.is_animating = True
        # self.time = time

    def update(self):
        if self.is_animating == True:
            self.current_sprite += 0.2

            if self.current_sprite >= len(self.sprites):
                self.current_sprite = 0
                self.is_animating = False
                self.kill()

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

screen_width = 1440
screen_length = 900
screen = pygame.display.set_mode((screen_width, screen_length))
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
TIGER_ATTACK_15FPS_1 = pygame.transform.scale(TIGER_ATTACK_15FPS_1, (200, 300))
TIGER_ATTACK_15FPS_2 = pygame.transform.scale(TIGER_ATTACK_15FPS_2, (200, 300))
TIGER_ATTACK_15FPS_3 = pygame.transform.scale(TIGER_ATTACK_15FPS_3, (200, 300))
TIGER_ATTACK_15FPS_4 = pygame.transform.scale(TIGER_ATTACK_15FPS_4, (200, 300))
TIGER_ATTACK_15FPS_5 = pygame.transform.scale(TIGER_ATTACK_15FPS_5, (200, 300))
TIGER_ATTACK_15FPS_6 = pygame.transform.scale(TIGER_ATTACK_15FPS_6, (200, 300))
TIGER_ATTACK_15FPS_7 = pygame.transform.scale(TIGER_ATTACK_15FPS_7, (200, 300))
TIGER_ATTACK_15FPS_8 = pygame.transform.scale(TIGER_ATTACK_15FPS_8, (200, 300))
TIGER_ATTACK_15FPS_9 = pygame.transform.scale(TIGER_ATTACK_15FPS_9, (200, 300))
TIGER_ATTACK_15FPS_10 = pygame.transform.scale(TIGER_ATTACK_15FPS_10, (200, 300))
TIGER_ATTACK_15FPS_11 = pygame.transform.scale(TIGER_ATTACK_15FPS_11, (200, 300))
TIGER_ATTACK_15FPS_12 = pygame.transform.scale(TIGER_ATTACK_15FPS_12, (200, 300))
TIGER_ATTACK_15FPS_13 = pygame.transform.scale(TIGER_ATTACK_15FPS_13, (200, 300))
TIGER_ATTACK_15FPS_14 = pygame.transform.scale(TIGER_ATTACK_15FPS_14, (200, 300))
TIGER_ATTACK_15FPS_15 = pygame.transform.scale(TIGER_ATTACK_15FPS_15, (200, 300))
TIGER_ATTACK_15FPS_16 = pygame.transform.scale(TIGER_ATTACK_15FPS_16, (200, 300))
TIGER_ATTACK_15FPS_17 = pygame.transform.scale(TIGER_ATTACK_15FPS_17, (200, 300))
TIGER_ATTACK_15FPS_18 = pygame.transform.scale(TIGER_ATTACK_15FPS_18, (200, 300))
TIGER_ATTACK_15FPS_19 = pygame.transform.scale(TIGER_ATTACK_15FPS_19, (200, 300))
TIGER_ATTACK_15FPS_20 = pygame.transform.scale(TIGER_ATTACK_15FPS_20, (200, 300))
TIGER_ATTACK_15FPS_21 = pygame.transform.scale(TIGER_ATTACK_15FPS_21, (200, 300))
TIGER_ATTACK_15FPS_22 = pygame.transform.scale(TIGER_ATTACK_15FPS_22, (200, 300))
TIGER_ATTACK_15FPS_23 = pygame.transform.scale(TIGER_ATTACK_15FPS_23, (200, 300))
TIGER_ATTACK_15FPS_24 = pygame.transform.scale(TIGER_ATTACK_15FPS_24, (200, 300))
TIGER_ATTACK_15FPS_25 = pygame.transform.scale(TIGER_ATTACK_15FPS_25, (200, 300))
TIGER_ATTACK_15FPS_26 = pygame.transform.scale(TIGER_ATTACK_15FPS_26, (200, 300))
TIGER_ATTACK_15FPS_27 = pygame.transform.scale(TIGER_ATTACK_15FPS_27, (200, 300))
TIGER_ATTACK_15FPS_28 = pygame.transform.scale(TIGER_ATTACK_15FPS_28, (200, 300))
TIGER_ATTACK_15FPS_29 = pygame.transform.scale(TIGER_ATTACK_15FPS_29, (200, 300))
TIGER_ATTACK_15FPS_30 = pygame.transform.scale(TIGER_ATTACK_15FPS_30, (200, 300))
TIGER_ATTACK_15FPS_31 = pygame.transform.scale(TIGER_ATTACK_15FPS_31, (200, 300))
TIGER_ATTACK_15FPS_32 = pygame.transform.scale(TIGER_ATTACK_15FPS_32, (200, 300))
TIGER_ATTACK_15FPS_33 = pygame.transform.scale(TIGER_ATTACK_15FPS_33, (200, 300))
TIGER_ATTACK_15FPS_34 = pygame.transform.scale(TIGER_ATTACK_15FPS_34, (200, 300))
TIGER_ATTACK_15FPS_35 = pygame.transform.scale(TIGER_ATTACK_15FPS_35, (200, 300))
TIGER_ATTACK_15FPS_36 = pygame.transform.scale(TIGER_ATTACK_15FPS_36, (200, 300))
TIGER_ATTACK_15FPS_37 = pygame.transform.scale(TIGER_ATTACK_15FPS_37, (200, 300))
TIGER_ATTACK_15FPS_38 = pygame.transform.scale(TIGER_ATTACK_15FPS_38, (200, 300))
TIGER_ATTACK_15FPS_39 = pygame.transform.scale(TIGER_ATTACK_15FPS_39, (200, 300))
TIGER_ATTACK_15FPS_40 = pygame.transform.scale(TIGER_ATTACK_15FPS_40, (200, 300))
TIGER_ATTACK_15FPS_41 = pygame.transform.scale(TIGER_ATTACK_15FPS_41, (200, 300))
TIGER_ATTACK_15FPS_42 = pygame.transform.scale(TIGER_ATTACK_15FPS_42, (200, 300))
TIGER_ATTACK_15FPS_43 = pygame.transform.scale(TIGER_ATTACK_15FPS_43, (200, 300))
TIGER_ATTACK_15FPS_44 = pygame.transform.scale(TIGER_ATTACK_15FPS_44, (200, 300))
TIGER_ATTACK_15FPS_45 = pygame.transform.scale(TIGER_ATTACK_15FPS_45, (200, 300))
TIGER_ATTACK_15FPS_46 = pygame.transform.scale(TIGER_ATTACK_15FPS_46, (200, 300))
TIGER_ATTACK_15FPS_47 = pygame.transform.scale(TIGER_ATTACK_15FPS_47, (200, 300))
TIGER_ATTACK_15FPS_48 = pygame.transform.scale(TIGER_ATTACK_15FPS_48, (200, 300))
TIGER_ATTACK_15FPS_49 = pygame.transform.scale(TIGER_ATTACK_15FPS_49, (200, 300))
TIGER_ATTACK_15FPS_50 = pygame.transform.scale(TIGER_ATTACK_15FPS_50, (200, 300))

tigerAttack15FPSarr = [TIGER_ATTACK_15FPS_1, TIGER_ATTACK_15FPS_2, TIGER_ATTACK_15FPS_3, TIGER_ATTACK_15FPS_4, TIGER_ATTACK_15FPS_5, TIGER_ATTACK_15FPS_6, TIGER_ATTACK_15FPS_7, TIGER_ATTACK_15FPS_8, TIGER_ATTACK_15FPS_9, TIGER_ATTACK_15FPS_10, TIGER_ATTACK_15FPS_11, TIGER_ATTACK_15FPS_12, TIGER_ATTACK_15FPS_13, TIGER_ATTACK_15FPS_14, TIGER_ATTACK_15FPS_15, TIGER_ATTACK_15FPS_16, TIGER_ATTACK_15FPS_17, TIGER_ATTACK_15FPS_18, TIGER_ATTACK_15FPS_19, TIGER_ATTACK_15FPS_20, TIGER_ATTACK_15FPS_21, TIGER_ATTACK_15FPS_22, TIGER_ATTACK_15FPS_23, TIGER_ATTACK_15FPS_24, TIGER_ATTACK_15FPS_25,
                       TIGER_ATTACK_15FPS_26, TIGER_ATTACK_15FPS_27, TIGER_ATTACK_15FPS_28, TIGER_ATTACK_15FPS_29, TIGER_ATTACK_15FPS_30, TIGER_ATTACK_15FPS_31, TIGER_ATTACK_15FPS_32, TIGER_ATTACK_15FPS_33, TIGER_ATTACK_15FPS_34, TIGER_ATTACK_15FPS_35, TIGER_ATTACK_15FPS_36, TIGER_ATTACK_15FPS_37, TIGER_ATTACK_15FPS_38, TIGER_ATTACK_15FPS_39, TIGER_ATTACK_15FPS_40, TIGER_ATTACK_15FPS_41, TIGER_ATTACK_15FPS_42, TIGER_ATTACK_15FPS_43, TIGER_ATTACK_15FPS_44, TIGER_ATTACK_15FPS_45, TIGER_ATTACK_15FPS_46, TIGER_ATTACK_15FPS_47, TIGER_ATTACK_15FPS_48, TIGER_ATTACK_15FPS_49, TIGER_ATTACK_15FPS_50, ]


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
attack_group = pygame.sprite.Group()

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
            apple_group.draw(screen)
            apple.animate()

            if apple.is_animating == False:
                apple_group = pygame.sprite.Group()

    # if apple.is_animating == False:
    #     apple_group = pygame.sprite.Group()

    apple = Fruit(pygame.mouse.get_pos()[0], pygame.mouse.get_pos()[1], appleARR)

    if len(tiger_group) < 5:
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
                apple_group.draw(screen)
                apple.animate()

        # if apple.is_animating == False:
        #     apple_group = pygame.sprite.Group()

        if len(tiger_group) < 5:
            tiger_image = pygame.transform.scale(tiger_image, (random.randint(150, 200), random.randint(150, 200)))
            new_tiger = Tiger(random.randint(100, 900), random.randint(50, 670), tiger_image)
            tiger_group.add(new_tiger)
            layer1_group.add(new_tiger)

        pygame.display.flip()
        screen.blit(background, (0, 0))

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
                if x.layer == 4:
                    layer5_group.remove(x)
                    attacktiger = Animation(0, 0, tigerAttack15FPSarr)
                    attack_group.add(attacktiger)
                    attack_group.draw(screen)
                    attacktiger.animate()

                x.layer += 1
                x.time = 0

        # draws in order
        layer1_group.draw(screen)
        layer2_group.draw(screen)
        layer3_group.draw(screen)
        layer4_group.draw(screen)
        layer5_group.draw(screen)

        crosshair_group.draw(screen)
        crosshair_group.update()

        attack_group.draw(screen)
        attack_group.update()

        apple_group.draw(screen)
        apple_group.update()

        clock.tick(60)

# to do:
# location of tigers
# try putting it in to a function to collide
#
