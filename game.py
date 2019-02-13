import pygame
import sys
from pygame.locals import *


BOARDWIDTH = 4  # Кол-во рядов
BOARDHEIGHT = 4  # Кол-во строк
WINDOWWIDTH = 800  # Ширина экрана
WINDOWHEIGHT = 600  # Высота экрана
TILESIZE = 100  # Размер одной клетки
BLANK = None  # Пустое пространство
BASICFONTSIZE = 30  # Размер шрифта

BGCOLOR = (0, 0, 0)  # Фоновый цвет
TILECOLOR = (0, 123, 123)  # Цвет пятнашки
BORDERCOLOR = (0, 255, 255)  # Цвет обводки поля
TEXTCOLOR = (255, 255, 255)  # Цвет текста

# X-координата верхнего левого угла поля
XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int(
    (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)  # Y-координата верхнего левого угла поля


def main():
    """Главная функция"""
    global FPSCLOCK, screen, TILESIZE, BLANK, BASICFONT

    pygame.init()
    FPSCLOCK = pygame.time.Clock()  # Определение обновления экрана
    screen = pygame.display.set_mode(
        (WINDOWWIDTH, WINDOWHEIGHT))  # Определение поверхности экрана
    pygame.display.set_caption('Пятнашки')  # Определение названия окна
    BASICFONT = pygame.font.Font(
        'freesansbold.ttf', BASICFONTSIZE)  # Определение шрифта
    board = getStartingBoard()
    while True:  # Основной цикл игры
        drawBoard(board)
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


def drawBoard(board):
    """Функция рисования игрового поля"""
    screen.fill(BGCOLOR)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(screen, BORDERCOLOR, (left, top, width, height), 4)


def getStartingBoard():
    """Функция определения игрового поля"""
    board = []
    counter = 1
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def getLeftTopOfTile(tileX, tileY):
    """Определения отступа сверху слева"""
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def drawTile(tilex, tiley, number):
    """Функция рисования отдельной пятнашки"""
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(screen, TILECOLOR,
                     (left, top, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2), top + int(TILESIZE / 2)
    screen.blit(textSurf, textRect)


if __name__ == '__main__':
    main()
