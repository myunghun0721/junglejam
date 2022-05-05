
from multiprocessing.dummy import Array
from turtle import screensize
import pygame
import sys
pygame.init()


class Grid():

    def __init__(self) -> None:
        pass

    def begin(self):
        self.screen = pygame.display.set_mode((1280, 720))
        self.gridArray = [[0]*16 for _ in range(100)]
        done = False

        self.color = (255, 0, 0)

        while done == False:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True

            # Create a grid starting at the first, parameter, going to the second parameter with a size of blocks as the third parameter.
            for x in range(80, 1280, 80):
                pygame.draw.line(self.screen, self.color, (0, x), (1280, x), 2)
                pygame.draw.line(self.screen, self.color, (x, 0), (x, 720), 2)
                pygame.display.update()

    def collision(self, x, y):
        self.x = int(x/80)
        self.y = int(y/80)
        # self.gridArray[self.x][self.y]
        pygame.draw.rect(self.screen, self.color, (x, y, 80, 80))
        # Set the appropiate grid location to 1 representing a hit
        self.gridArray[self.x][self.y] = 1

        print('Reached!')
