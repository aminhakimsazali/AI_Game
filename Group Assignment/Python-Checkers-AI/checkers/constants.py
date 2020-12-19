import pygame

WIDTH, HEIGHT = 600, 600
ROWS, COLS = 8, 8
SQUARE_SIZE =  WIDTH//COLS

# rgb
RED = (255, 0, 0)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREY = (128,128,128)
WOODEN = (160, 64, 0)
ORANGE = (255, 156, 0)
GREY = (253, 235, 208)

CROWN = pygame.transform.scale(pygame.image.load('assets/crown.png'), (44, 25))
