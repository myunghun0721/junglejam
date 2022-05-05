import pygame
print('Path to module:',pygame.__file__)
 
screen = pygame.display.set_mode((640,320))
 
pygame.init()
width,height = 960,640
window = pygame.display.set_mode((width,height))

bg_img = pygame.image.load('venv/images/test.png')
bg_img = pygame.transform.scale(bg_img,(width,height))

img1 = pygame.image.load('venv/images/test1.png')
img2 = pygame.image.load('venv/images/test2.png')


runing = True
while runing:
    window.blit(bg_img,(0,0))
    window.blit(img1,(0,0))
    window.blit(img2,(0,0))
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            runing = False
    pygame.display.update()
pygame.quit()