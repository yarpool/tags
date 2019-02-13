import pygame
import sys
from pygame.locals import *


BOARDWIDTH = 4  # Кол-во рядов
BOARDHEIGHT = 4  # Кол-во строк
WINDOWWIDTH = 640  # Ширина экрана
WINDOWHEIGHT = 480  # Высота экрана


def main():
    global FPSCLOCK, screen

    pygame.init()
    FPSCLOCK = pygame.time.Clock()  # Определение обновления экрана
    screen = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT))  # Определение поверхности экрана
    pygame.display.set_caption('Пятнашки')  # Определение названия окна

    while True:  # Основной цикл игры
        checkForQuit()
        pygame.display.update()
        FPSCLOCK.tick(30)


def terminate():
    """Функция выхода из игры"""
    pygame.quit()
    sys.exit()


def checkForQuit():
    """Функция определения выхода из игры"""
    for event in pygame.event.get(QUIT):
        terminate()


if __name__ == '__main__':
    main()
