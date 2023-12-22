import pygame
from pygame.locals import *
import random

# CONSTANTS ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
FPS_CAP = 60
SCREEN_BG = (20,20,20)
WINDOW_NAME = 'WORDLE'
WINDOW_WIDTH = 800
WINDOW_HEIGHT =800
TITLE_NAME = 'WORDLE'
TITLE_REGION_HEIGHT = 65
TITLE_FONT_SIZE = 32
BORDER_COLOR = (100,100,100)
FONT_COLOR = (255,255,255)
FONT = "./assets/Helvetica-Neue-67-Medium-Condensed.ttf"
SQUARE_SIZE = 60
SQUARE_THICKNESS = 2
SQUARE_GAP = 5
BOARD_NUM_LETTER = 5
BOARD_NUM_ATTEMPT = 6
WORD_DICTIONARY = "./assets/wordle-La.txt"
CORRECT_COLOR = (50,205,50)
PARTIAL_COLOR = (204,204,0)


# GAME CLASS ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
class Game():

    def __init__(self, board):
        pygame.init()
        pygame.font.init()
        pygame.display.set_caption(WINDOW_NAME)
        self.screen = pygame.display.set_mode((WINDOW_WIDTH,WINDOW_HEIGHT))
        self.font = pygame.font.Font(FONT, TITLE_FONT_SIZE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.board = board
        self.set_screen()
        self.draw_title()
        self.draw_board()
        
    def draw_board(self):
        x = (WINDOW_WIDTH - ((SQUARE_SIZE + SQUARE_GAP) * (BOARD_NUM_LETTER)))/2
        y= 100
        for row in range(BOARD_NUM_ATTEMPT):
            for letter in range(BOARD_NUM_LETTER):
                self.draw_square(x,y,self.board.getLetter(row,letter),self.board.getColor(row,letter))
                x += SQUARE_SIZE + SQUARE_GAP
            x = (WINDOW_WIDTH - ((SQUARE_SIZE + SQUARE_GAP) * (BOARD_NUM_LETTER)))/2
            y += SQUARE_SIZE + SQUARE_GAP
    
    def draw_title(self):
        pygame.draw.line(self.screen, BORDER_COLOR, (0,TITLE_REGION_HEIGHT),(WINDOW_WIDTH,TITLE_REGION_HEIGHT))
        text = self.font.render(TITLE_NAME, True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (WINDOW_WIDTH/2,TITLE_REGION_HEIGHT/2)
        self.screen.blit(text, textRect)

    def set_screen(self):
        pygame.display.set_caption(WINDOW_NAME)
        self.screen.fill(SCREEN_BG)

    def draw_square(self,x,y,text,color):
        pygame.draw.rect(self.screen,BORDER_COLOR,(x,y,SQUARE_SIZE,SQUARE_SIZE))
        pygame.draw.rect(self.screen,color,(x + SQUARE_THICKNESS,y+ SQUARE_THICKNESS,SQUARE_SIZE - SQUARE_THICKNESS * 2,SQUARE_SIZE- SQUARE_THICKNESS*2))
        text = self.font.render(text, True, FONT_COLOR)
        textRect = text.get_rect()
        textRect.center = (x + SQUARE_SIZE/2,y + SQUARE_SIZE/2)
        self.screen.blit(text, textRect)

# GAMEBOARD CLASS |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
class Board:
    gameboard = []
    line_index = 0
    row_index = 0
    line_num = 0
    row_num = 0
    word = ""

    def __init__(self,word): 
        self.line_num = BOARD_NUM_LETTER
        self.row_num = BOARD_NUM_ATTEMPT
        self.word = word
        for _ in range(self.row_num):
            row = []
            for _ in range(self.line_num):
                row.append(['',SCREEN_BG])
            self.gameboard.append(row)
    
    def add(self,letter):
        if(self.line_index < self.line_num):
            if (self.line_index < self.line_num):
                self.gameboard[self.row_index][self.line_index] = [letter,SCREEN_BG]
                self.line_index += 1
        return
    
    def backspace(self):
        if(self.line_index >= 0):
            if (self.line_index != 0):
                self.line_index -= 1
            self.gameboard[self.row_index][self.line_index] = ['',SCREEN_BG]
        return
        
    def compare(self, letter, index):
        if(letter == self.word[index]):
            return CORRECT_COLOR
        elif (letter in self.word):
            return PARTIAL_COLOR
        else: return BORDER_COLOR
            
    def assign_color(self):
        for index in range(self.line_num):
            self.gameboard[self.row_index][index][1] = self.compare(self.gameboard[self.row_index][index][0], index)

    def checkWin(self):
        flag = True
        for s in self.gameboard[self.row_index]:
            if (s[1] != CORRECT_COLOR):
                flag = False
        return flag
    
    def getLetter(self,row,index):
        return self.gameboard[row][index][0]
    
    def getColor(self,row,index):
        return self.gameboard[row][index][1]
        
    def isValidWord(self):
        if (self.line_index >= self.line_num -1):
            word = ""
            for s in self.gameboard[self.row_index]:
                word += s[0].lower()
            with open(WORD_DICTIONARY,'r') as dictionary:
                for line in dictionary.readlines():
                    if word in line:
                        return True
        else: 
            return False

    def enter(self):
        if(self.line_index > self.line_num - 1 and self.isValidWord()):
            self.assign_color()
            if self.checkWin():
                print("game is over")
                return
            self.line_index = 0
            if (self.row_index < self.row_num - 1):
                self.row_index += 1
                return
            else:
                print("game is over")
                return
        return



    def print_board(self):
        print(self.gameboard)


# MAIN PROGRAM ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def generate_board():
    lines = open(WORD_DICTIONARY).read().splitlines()
    word = random.choice(lines).upper()
    print(word)
    return Board(word)

def main():
    game = Game(generate_board())
    
    while game.running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game.running = False
            if event.type == pygame.KEYDOWN:
                if(event.key == pygame.K_RETURN):
                    game.board.enter()
                if(event.key == pygame.K_BACKSPACE):
                    game.board.backspace()
                for i in range( pygame.K_a, pygame.K_z +1): 
                    if event.key == i:
                        game.board.add(event.unicode.upper()) 
                
                game.draw_board()

        pygame.display.flip()
        game.clock.tick(FPS_CAP)
    
    pygame.quit()

if __name__ == "__main__":
    main()
