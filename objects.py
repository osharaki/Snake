from enum import Enum
import pygame.time as GAME_TIME
import random

class Direction(Enum):
    up = 1
    down = 2
    left = 3
    right = 4

# Represents the playing field. Essentially a list of lists.
class Field():

    def __init__(self, windowWidth, windowHeight):
        self.windowHeight = windowHeight
        self.windowWidth = windowWidth
        self.WIDTH = 10 # square width
        self.HEIGHT = 10 # square height
        self.MARGIN = 1  # distance between squares

        # Adjusts the screen size to make all grid blocks fit perfectly taking in regard margin size
        while self.windowHeight % (self.HEIGHT + self.MARGIN) != 0:
            self.windowHeight += 1
        self.blocksInCol = windowHeight//(self.HEIGHT + self.MARGIN)
        while self.windowWidth % (self.WIDTH + self.MARGIN) != 0:
            self.windowWidth += 1
        self.blocksInRow = windowWidth//(self.WIDTH + self.MARGIN)

        self.grid = [[0 for x in range(self.blocksInRow)] for y in range(self.blocksInCol)]

class Snake():

    def __init__(self, field, color):
        self.refreshFreq = 100  # The lower the value, the faster the snake
        self.hit = False
        self.body = []
        self.direction = Direction.left
        self.color = color
        self.lastMove = GAME_TIME.get_ticks()
        self.score = 0

        # dictionary containing tuples. Keys represent body blocks, while tuples are coordinates of said body blocks
        for i in range(5):
            if i == 0:
                self.body.append((field.blocksInRow//2, field.blocksInCol//2))    # if it's the head place it in the middle of the grid
            else:
                self.body.append((self.body[i-1][0], self.body[i-1][1] + 1))   # otherwise, each body block is to be placed one block right of its predecessor

    def move(self):
        if not self.hit:    # If snake hasn't hit anything yet he may move
            if GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                #self.hitTimer = GAME_TIME.get_ticks()
                # Each bb takes its target position from its predecessor, except for the head, its next position is calculated according to the direction
                if self.direction == Direction.left:
                    i = len(self.body) - 1
                    for bb in reversed(self.body):
                        if i == 0:
                            self.body[i] = (self.body[i][0], self.body[i][1] - 1)    # new position of head
                        else:
                            self.body[i] = self.body[i-1]
                        i -= 1
                if self.direction == Direction.right:
                    i = len(self.body) - 1
                    for bb in reversed(self.body):
                        if i == 0:
                            self.body[i] = (self.body[i][0], self.body[i][1] + 1)    # new position of head
                        else:
                            self.body[i] = self.body[i-1]
                        i -= 1
                if self.direction == Direction.up:
                    i = len(self.body) - 1
                    for bb in reversed(self.body):
                        if i == 0:
                            self.body[i] = (self.body[i][0] - 1, self.body[i][1])    # new position of head
                        else:
                            self.body[i] = self.body[i-1]
                        i -= 1
                if self.direction == Direction.down:
                    i = len(self.body) - 1
                    for bb in reversed(self.body):
                        if i == 0:
                            self.body[i] = (self.body[i][0] + 1, self.body[i][1])    # new position of head
                        else:
                            self.body[i] = self.body[i-1]
                        i -= 1
                self.lastMove = GAME_TIME.get_ticks()

    def checkImpact(self, grid):
        # Hit top
        if self.body[0][0] <= 0:
            if self.direction == Direction.up and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                self.hit = True
        # Hit bottom
        if self.body[0][0] >= grid.blocksInCol:
            if self.direction == Direction.down and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                self.hit = True
        # Hit left
        if self.body[0][1] <= 0:
            if self.direction == Direction.left and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                self.hit = True
        # Hit right
        if self.body[0][1] >= grid.blocksInRow:
            if self.direction == Direction.right and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                self.hit = True
        # check if snake hit itself
        for i in range(len(self.body)):
            # hit from the top ==> if colHead == colBB and rowHead + 1 == rowBB and direction == down and time limit reached
            if self.body[0][1] == self.body[i][1] and self.body[0][0] + 1 == self.body[i][0]:
                if self.direction == Direction.down and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                    self.hit = True
            # hit from the bottom ==> if colHead == colBB and rowHead - 1 == rowBB and direction == up and time limit reached
            elif self.body[0][1] == self.body[i][1] and self.body[0][0] - 1 == self.body[i][0]:
                if self.direction == Direction.up and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                    self.hit = True
            # hit from the left ==> if rowHead == rowBB and colHead + 1 == colBB and direction == right and time limit reached
            elif self.body[0][0] == self.body[i][0] and self.body[0][1] + 1 == self.body[i][1]:
                if self.direction == Direction.right and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                    self.hit = True
            # hit from the right ==> if rowHead == rowBB and colHead - 1 == colBB and direction == left and time limit reached
            elif self.body[0][0] == self.body[i][0] and self.body[0][1] - 1 == self.body[i][1]:
                if self.direction == Direction.left and GAME_TIME.get_ticks() - self.lastMove >= self.refreshFreq:
                    self.hit = True

class Dot():

    def __init__(self, field, snake, color):
        self.eaten = False  # has this dot been eaten yet
        self.numEaten = 0   # number of dots eaten
        self.color = color
        self.timeAllowed = snake.refreshFreq * 55   # max time allowed for dot to remain on the screen
        self.dotScore = 5
        randPos = (random.randint(0, len(field.grid[0]) - 1), random.randint(0, len(field.grid) - 1))
        for i in range(len(snake.body)):    # if dot's position will not collide with a bb, place it
            if randPos == snake.body[i]:
                randPos = (random.randint(0, len(field.grid[0]) - 1), random.randint(0, len(field.grid) - 1))
                i = 0
            else:
                i += 1
        self.pos = randPos
        self.timePlaced = GAME_TIME.get_ticks() # time dot was placed

    '''
    A new dot will be placed in one of two cases:
        1. Snake has eaten dot
        2. Dot timer has run out
    '''
    def place(self, field, snake):
        if self.eaten:
            randPos = (random.randint(0, len(field.grid[0]) - 1), random.randint(0, len(field.grid) - 1))
            for i in range(len(snake.body)):
                if randPos == snake.body[i]:
                    randPos = (random.randint(0, len(field.grid[0]) - 1), random.randint(0, len(field.grid) - 1))
                    i = 0
                else:
                    i += 1
            self.pos = randPos
            self.timePlaced = GAME_TIME.get_ticks()
            self.eaten = False
        
    def checkEaten(self, field, snake):
        # has dot been eaten?
        if snake.body[0][0] == self.pos[0] and snake.body[0][1] == self.pos[1]:
            self.eaten = True
            self.scoreCalc(snake)
            self.numEaten += 1
            if self.numEaten % 3 == 0:
                if snake.body[len(snake.body) - 1][0] > snake.body[len(snake.body) - 2][0] \
                        and snake.body[len(snake.body) - 1][1] == snake.body[len(snake.body) - 2][1]:
                    snake.body.append((snake.body[len(snake.body) - 1][0] + 1, snake.body[len(snake.body) - 1][1]))
                if snake.body[len(snake.body) - 1][0] == snake.body[len(snake.body) - 2][0] \
                        and snake.body[len(snake.body) - 1][1] > snake.body[len(snake.body) - 2][1]:
                    snake.body.append((snake.body[len(snake.body) - 1][0], snake.body[len(snake.body) - 1][1] + 1))
                if snake.body[len(snake.body) - 1][0] == snake.body[len(snake.body) - 2][0] \
                        and snake.body[len(snake.body) - 1][1] < snake.body[len(snake.body) - 2][1]:
                    snake.body.append((snake.body[len(snake.body) - 1][0], snake.body[len(snake.body) - 1][1] - 1))
                if snake.body[len(snake.body) - 1][0] < snake.body[len(snake.body) - 2][0] \
                        and snake.body[len(snake.body) - 1][1] == snake.body[len(snake.body) - 2][1]:
                    snake.body.append((snake.body[len(snake.body) - 1][0] - 1, snake.body[len(snake.body) - 1][1]))
                snake.refreshFreq -= 5
    def scoreCalc(self, snake):
        snake.score += self.dotScore
