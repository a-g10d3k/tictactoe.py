from pynput import keyboard
from copy import deepcopy
from os import system
import random

class Board:
    def __init__(self):
        self.reset()
    def reset(self):
        self.board = []
        for y in range(3):
            self.board.append([])
            for x in range(3):
                self.board[y].append(' ')
    def getBoardState(self): #returns 0: game ongoing, 1: X victory, 2: O victory, 3: draw
        draw = True
        #horizontals
        for row in self.board:
            X = O = 0
            for tile in row:
                if tile == 'X':
                    X += 1
                elif tile == 'O':
                    O += 1
            if X + O == X:
                draw = False
            if X == 3:
                return 1
            elif O == 3:
                return 2
        #verticals
        for column in range(3):
            X = O = 0
            for row in range(3):
                tile = self.board[row][column]
                if tile == 'X':
                    X += 1
                elif tile == 'O':
                    O += 1
            if X + O == X:
                draw = False
            if X == 3:
                return 1
            if O == 3:
                return 2
        #diagonals
        for k in range(2):
            X = O = 0
            for i in range(3):
                tile = self.board[i][i if k is 0 else -i - 1]
                if tile == 'X':
                     X += 1
                elif tile == 'O':
                      O += 1
            if X + O == X:
                draw = False
            if X == 3:
                return 1
            if O == 3:
                return 2
        if draw:
            return 3
        return 0
        

class GameController:
    def __init__(self):
        self.board = Board()
        self.cursor = Cursor()
        self.AI = AI()
        self.turn = 0
    def start(self):
        while True:
            if self.gameLoop() == False:
                return
    def restart(self):
        self.board.reset()
        self.turn = 0
    def gameLoop(self, stop = False):
        system('cls')
        boardState = self.board.getBoardState()
        if boardState != 0:
            print ('It\'s a draw!' if boardState == 3 else 'X wins!' if boardState == 1 else 'O wins!')
        self.displayBoard(self.board.board)
        key = self.getInput()
        if boardState != 0:
            self.restart()
            return True
        self.moveCursor(key)
        self.place(key)
        boardState = self.board.getBoardState()
        if boardState != 0:
            return True
        if self.turn == 1:
            self.AI.place(self.board.board)
            self.turn = 0
        if key == keyboard.Key.esc:
            return False
        return True
    def moveCursor(self, key):
        if key == keyboard.Key.right:
            self.cursor.x += 1
        elif key == keyboard.Key.left:
            self.cursor.x -= 1
        elif key == keyboard.Key.up:
            self.cursor.y -= 1
        elif key == keyboard.Key.down:
            self.cursor.y += 1
    def place(self, key):
        if key == keyboard.Key.enter:
            board = self.board.board
            if board[self.cursor.y][self.cursor.x] == ' ':
                board[self.cursor.y][self.cursor.x] = 'X'
                self.turn = 1
            #self.cursor.x = 0
            #self.cursor.y = 0
            self.cursor.display = False
    def displayBoard(self, board):
        displayedBoard = deepcopy(board)
        for row, y in enumerate(displayedBoard):
            if self.cursor != None and self.cursor.display:
                displayedBoard[self.cursor.y][self.cursor.x] = '*'
            print(y[0], y[1], y[2], sep='#', end='\n#####\n' if row != 2 else '\n')
    def getInput(self):
        class ret:
            value = None
        def onpress(key):
            ret.value = key
            return False
        with keyboard.Listener(
            on_press = onpress
            ) as listener:
            listener.join()
        return ret.value

class Cursor:
    def __init__(self):
        self.displayOnMove = True
        self.x = 0
        self.y = 0
        self.display = True
        
    @property
    def x(self):
        return self.__x
    @x.setter
    def x(self, value):
        if self.displayOnMove:
            self.display = True
        if value > 2:
            self.__x = 2
        elif value < 0:
            self.__x = 0
        else:
            self.__x = value
        
    @property
    def y(self):
        return self.__y
    @y.setter
    def y(self, value):
        if self.displayOnMove:
            self.display = True
        if value > 2:
            self.__y = 2
        elif value < 0:
            self.__y = 0
        else:
            self.__y = value
class AI:
    def place(self, board):
        random.seed()
        offset = random.randrange(9)
        for i in range(9):
            if board[(offset - i) // 3][(offset - i) % 3] == ' ':
                board[(offset - i) // 3][(offset - i) % 3] = 'O'
                return

game = GameController()
game.start()
