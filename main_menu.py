import pygame, sys
from button import Button
from pygame import mixer

pygame.init()

SCREEN = pygame.display.set_mode((1920, 1080))
pygame.display.set_caption("Menu")

def get_font(size): # Returns Press-Start-2P in the desired size
    return pygame.font.Font("venv/assets/font.ttf", size)

BG = pygame.image.load("venv/images/jungle_jam.jpg")

music = mixer.music
music.load('venv/assets/Jungle_Beatz_V1.mp3')
# play music forever
music.play(-1)
score_value = 0

def leaderboard():
    global score_value
    while True:
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
    global score_value
    while True:
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
                    leaderboard()
                if UPSCORE.checkForInput(PLAY_MOUSE_POS):
                    score_value +=1

        pygame.display.update()

def main_menu():
    while True:
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
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if PLAY_BUTTON.checkForInput(MENU_MOUSE_POS):
                    play()

                if QUIT_BUTTON.checkForInput(MENU_MOUSE_POS):
                    pygame.quit()
                    sys.exit()

        pygame.display.update()

main_menu()