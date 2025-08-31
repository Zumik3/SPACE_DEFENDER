import pygame
pygame.font.init()

from utils.constants import init_fonts
init_fonts()

from game import Game

if __name__ == "__main__":
    game = Game()
    game.run()