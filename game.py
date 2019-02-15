import pygame
import sys
from pygame.locals import *

BOARDWIDTH = 4  # Кол-во рядов
BOARDHEIGHT = 4  # Кол-во столбцов
TILESIZE = 100  # Размер клетки
WINDOWWIDTH = 800  # Ширина экрана
WINDOWHEIGHT = 600  # Высота экрана
FPS = 30  # Частота обновления
BLANK = None  # Пусто пространство

# Определение цветов объектов
BGCOLOR = (0, 0, 0)
TILECOLOR = (0, 200, 100)
TEXTCOLOR = (255, 255, 255)
BORDERCOLOR = (0, 125, 125)
MESSAGECOLOR = (255, 255, 255)

BASICFONTSIZE = 30  # Размер шрифта

XMARGIN = int((WINDOWWIDTH - (TILESIZE * BOARDWIDTH + (BOARDWIDTH - 1))) / 2)
YMARGIN = int(
    (WINDOWHEIGHT - (TILESIZE * BOARDHEIGHT + (BOARDHEIGHT - 1))) / 2)

# Направления
UP = 'up'
DOWN = 'down'
LEFT = 'left'
RIGHT = 'right'


def main():
    global FPSCLOCK, SCREEN, BASICFONT

    # Основные настройки параметров экрана
    pygame.init()
    FPSCLOCK = pygame.time.Clock()
    SCREEN = pygame.display.set_mode((WINDOWWIDTH, WINDOWHEIGHT))
    pygame.display.set_caption('Slide Puzzle')
    BASICFONT = pygame.font.Font('freesansbold.ttf', BASICFONTSIZE)

    mainBoard = getStartingBoard()

    while True:  # основной игровой цикл
        slideTo = None
        msg = 'Нажмите на плитку что бы переместить её.'

        drawBoard(mainBoard, msg)

        checkForQuit()
        for event in pygame.event.get():  # цикл обработки событий
            if event.type == MOUSEBUTTONUP:
                spotx, spoty = getSpotClicked(
                    mainBoard, event.pos[0], event.pos[1])
                blankx, blanky = getBlankPosition(mainBoard)
                if spotx == blankx + 1 and spoty == blanky:
                    slideTo = LEFT
                elif spotx == blankx - 1 and spoty == blanky:
                    slideTo = RIGHT
                elif spotx == blankx and spoty == blanky + 1:
                    slideTo = UP
                elif spotx == blankx and spoty == blanky - 1:
                    slideTo = DOWN

        if slideTo:
            # Анимация пкередвижения плитки
            slideAnimation(mainBoard, slideTo,
                           'Нажмите на плитку что бы переместить её.', 8)
            makeMove(mainBoard, slideTo)
        pygame.display.update()
        FPSCLOCK.tick(FPS)


def terminate():
    """Функция выхода"""
    pygame.quit()
    sys.exit()


def checkForQuit():
    """Функция проверки выхода"""
    for event in pygame.event.get(QUIT):
        terminate()


def getStartingBoard():
    """Функция рисования стартового игрового поля"""
    counter = 1
    board = []
    for x in range(BOARDWIDTH):
        column = []
        for y in range(BOARDHEIGHT):
            column.append(counter)
            counter += BOARDWIDTH
        board.append(column)
        counter -= BOARDWIDTH * (BOARDHEIGHT - 1) + BOARDWIDTH - 1

    board[BOARDWIDTH - 1][BOARDHEIGHT - 1] = BLANK
    return board


def getBlankPosition(board):
    """Функция возвращающая x и y координаты пустого места"""
    for x in range(BOARDWIDTH):
        for y in range(BOARDHEIGHT):
            if board[x][y] == BLANK:
                return (x, y)


def makeMove(board, move):
    """Функция выполнения хода"""
    blankx, blanky = getBlankPosition(board)

    if move == UP:
        board[blankx][blanky], board[blankx][blanky + 1] =\
            board[blankx][blanky + 1], board[blankx][blanky]
    elif move == DOWN:
        board[blankx][blanky], board[blankx][blanky - 1] =\
            board[blankx][blanky - 1], board[blankx][blanky]
    elif move == LEFT:
        board[blankx][blanky], board[blankx + 1][blanky] =\
            board[blankx + 1][blanky], board[blankx][blanky]
    elif move == RIGHT:
        board[blankx][blanky], board[blankx - 1][blanky] =\
            board[blankx - 1][blanky], board[blankx][blanky]


def isValidMove(board, move):
    """Функция проверки возможности хода"""
    blankx, blanky = getBlankPosition(board)
    return (move == UP and blanky != len(board[0]) - 1) or \
           (move == DOWN and blanky != 0) or \
           (move == LEFT and blankx != len(board) - 1) or \
           (move == RIGHT and blankx != 0)


def getLeftTopOfTile(tileX, tileY):
    """Функция получения отступа"""
    left = XMARGIN + (tileX * TILESIZE) + (tileX - 1)
    top = YMARGIN + (tileY * TILESIZE) + (tileY - 1)
    return (left, top)


def getSpotClicked(board, x, y):
    """Функция получения от x & y координат x & y координат игрового поля"""
    for tileX in range(len(board)):
        for tileY in range(len(board[0])):
            left, top = getLeftTopOfTile(tileX, tileY)
            tileRect = pygame.Rect(left, top, TILESIZE, TILESIZE)
            if tileRect.collidepoint(x, y):
                return (tileX, tileY)
    return (None, None)


def drawTile(tilex, tiley, number, adjx=0, adjy=0):
    """Функция рисования плитки в координатах доски tilex и tiley"""
    left, top = getLeftTopOfTile(tilex, tiley)
    pygame.draw.rect(SCREEN, TILECOLOR,
                     (left + adjx, top + adjy, TILESIZE, TILESIZE))
    textSurf = BASICFONT.render(str(number), True, TEXTCOLOR)
    textRect = textSurf.get_rect()
    textRect.center = left + int(TILESIZE / 2) + \
        adjx, top + int(TILESIZE / 2) + adjy
    SCREEN.blit(textSurf, textRect)


def makeText(text, color, bgcolor, top, left):
    """Функция рисование текста на поверхности"""
    textSurf = BASICFONT.render(text, True, color, bgcolor)
    textRect = textSurf.get_rect()
    textRect.topleft = (top, left)
    return (textSurf, textRect)


def drawBoard(board, message):
    """Функция рисования игровой доски"""
    SCREEN.fill(BGCOLOR)
    if message:
        textSurf, textRect = makeText(message, MESSAGECOLOR, BGCOLOR, 5, 5)
        SCREEN.blit(textSurf, textRect)

    for tilex in range(len(board)):
        for tiley in range(len(board[0])):
            if board[tilex][tiley]:
                drawTile(tilex, tiley, board[tilex][tiley])

    left, top = getLeftTopOfTile(0, 0)
    width = BOARDWIDTH * TILESIZE
    height = BOARDHEIGHT * TILESIZE
    pygame.draw.rect(SCREEN, BORDERCOLOR, (left - 4, top - 4,
                                           width + 11, height + 11), 4)


def slideAnimation(board, direction, message, animationSpeed):
    """Функция анимирования передвижения одного элемента"""
    blankx, blanky = getBlankPosition(board)
    if direction == UP:
        movex = blankx
        movey = blanky + 1
    elif direction == DOWN:
        movex = blankx
        movey = blanky - 1
    elif direction == LEFT:
        movex = blankx + 1
        movey = blanky
    elif direction == RIGHT:
        movex = blankx - 1
        movey = blanky

    # подготовка базовой поверхности
    drawBoard(board, message)
    baseSurf = SCREEN.copy()
    # рисование пустого пространства над движущейся плиткой
    # на основной поверхности
    moveLeft, moveTop = getLeftTopOfTile(movex, movey)
    pygame.draw.rect(baseSurf, BGCOLOR, (moveLeft,
                                         moveTop, TILESIZE, TILESIZE))

    for i in range(0, TILESIZE, animationSpeed):
        # анимация скольжения плитки
        checkForQuit()
        SCREEN.blit(baseSurf, (0, 0))
        if direction == UP:
            drawTile(movex, movey, board[movex][movey], 0, -i)
        if direction == DOWN:
            drawTile(movex, movey, board[movex][movey], 0, i)
        if direction == LEFT:
            drawTile(movex, movey, board[movex][movey], -i, 0)
        if direction == RIGHT:
            drawTile(movex, movey, board[movex][movey], i, 0)

        pygame.display.update()
        FPSCLOCK.tick(FPS)


if __name__ == '__main__':
    main()
