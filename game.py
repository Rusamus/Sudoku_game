import pygame as p
from pygame.locals import *
import time
import random
import sys
import numpy as np

GRID_SIZE = 40
SCREEN_WIDTH = GRID_SIZE*9
SCREEN_HIGHT = GRID_SIZE*9
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
BLUE = (0,0,255)
BUTTONS = [K_0,K_1,K_2,K_3,K_4,K_5,K_6,K_7,K_8,K_9]
ENTER = 13
class Grid:
    def __init__(self,size,pams):
        self.pams = pams
        self.size = size
        self.table_base = np.zeros([self.size, self.size], dtype = int)

    def show(self):
        for i in range(root.get_height() // GRID_SIZE):
            for j in range(root.get_width() // GRID_SIZE):
                rect = p.Rect(j * GRID_SIZE, i * GRID_SIZE, GRID_SIZE, GRID_SIZE)
                font = p.font.Font(None, GRID_SIZE - 5)
                if (i + j) % 2 == 0:
                    p.draw.rect(root, BLACK, rect)
                    text = font.render('{}'.format(self.table_base[i][j]), True, BLUE)
                else:
                    p.draw.rect(root, WHITE, rect)
                    text = font.render('{}'.format(self.table_base[i][j]), True, BLUE)
                place = text.get_rect(center=(j * GRID_SIZE+20, i * GRID_SIZE+20))
                root.blit(text, place)

    #generating table-pattern
    def start_table(self):
        for i in range(self.size):
            for j in range(self.size):
                self.table_base[i][j] = (i * 3 + i // 3 + j) % self.size + 1

    #deleting given number of digits
    def sift(self):
        seen = []
        for k in range(self.size*self.size - self.pams):
            i = random.choice(range(self.size))
            j = random.choice(range(self.size))
            while (i,j) in seen:
                i = random.choice(range(self.size))
                j = random.choice(range(self.size))
            seen.append((i,j))
            self.table_base[i][j] = 0

    def fill(self,position,key):
        j,i = position
        self.table_base[i][j] = key

def screen_text_write(root,text, pams = None):
    font = p.font.Font(None, 25)
    text = font.render(text, True, (180, 0, 0))
    place = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2))
    root.blit(text, place)
    p.display.flip()



if __name__ == '__main__':
    p.init()
    root = p.display.set_mode((SCREEN_WIDTH, SCREEN_HIGHT))
    root.fill(WHITE)
    screen_text_write(root,'CHOOSE DIFFICULT')

    pams = ''
    event_happened = True
    while event_happened:
        for event in p.event.get():
            event_wait = p.event.wait()
            if event_wait.type == p.KEYDOWN:
                if event_wait.key in BUTTONS:
                    pams += str(event_wait.key - 48)
                if event_wait.key == ENTER:
                    event_happened = False
                    break
    pams = int(pams)
    root.fill(WHITE)
    font = p.font.Font(None, 25)
    text = font.render('DIFFICULT:{}'.format(pams), True, (180, 0, 0))
    place = text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HIGHT // 2))
    root.blit(text, place)
    p.display.flip()
    time.sleep(1)


    grid = Grid(9,pams)
    grid.start_table()
    grid.sift()
    while 1:
        root.fill(WHITE)
        grid.show()
        for event in p.event.get():
            if event.type == QUIT:
                quit()
                sys.exit()
            if event.type == p.MOUSEBUTTONDOWN:
                if event.button == 1:
                    i,j = event.pos
                    i = i//GRID_SIZE
                    j = j//GRID_SIZE

                    event_happened = True
                    while event_happened:
                        event_wait = p.event.wait()
                        if event_wait.type == p.KEYDOWN:
                            if event_wait.key in BUTTONS:
                                key = event_wait.key - 48
                                event_happened = False


                    grid.fill((i,j),key)

        p.display.update()
