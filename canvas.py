import pygame, sys
import pygame.locals as GAME_GLOBALS
import pygame.event as GAME_EVENTS
import objects



windowHeight = 500
windowWidth = 500
#dirChangeDelay = 30
myGrid = objects.Field(windowWidth, windowHeight)
'''
WIDTH = 10 # square width
HEIGHT = 10 # square height
MARGIN = 0  # distance between squares
'''


pygame.init()
pygame.font.init()

surface = pygame.display.set_mode((myGrid.windowWidth, myGrid.windowHeight))
pygame.display.set_caption('Snake!')

#Mouse Variables
mousePosition = (0,0)
mouseStates = None
mouseDown = False

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# screen text
font = pygame.font.Font(None, 30)
#size = font.size("koko!")


snake = objects.Snake(myGrid, GREEN)
dot = objects.Dot(myGrid, snake, WHITE)

def updateGame():

  global mouseDown, gameOver, ren
  
  ren = font.render(str(snake.score), 0, RED)
  snake.checkImpact(myGrid)
  snake.move()
  dot.checkEaten(myGrid, snake)
  dot.place(myGrid, snake)

def drawGame():

    surface.fill(BLACK)

    if snake.hit:
        snake.color = RED
    # Draw the snake
    for bb in snake.body:
        pygame.draw.rect(surface,
                             snake.color,
                             [(myGrid.MARGIN + myGrid.WIDTH) * bb[1] + myGrid.MARGIN,
                              (myGrid.MARGIN + myGrid.HEIGHT) * bb[0] + myGrid.MARGIN,
                              myGrid.WIDTH,
                              myGrid.HEIGHT])
    pygame.draw.rect(surface,
                             dot.color,
                             [(myGrid.MARGIN + myGrid.WIDTH) * dot.pos[1] + myGrid.MARGIN,
                              (myGrid.MARGIN + myGrid.HEIGHT) * dot.pos[0] + myGrid.MARGIN,
                              myGrid.WIDTH,
                              myGrid.HEIGHT])
    surface.blit(ren, (10, 10))

def quitGame():
  pygame.quit()
  sys.exit()

clock = pygame.time.Clock()

while True:

    mousePosition = pygame.mouse.get_pos()
    mouseStates = pygame.mouse.get_pressed()

    updateGame()
    drawGame()

    if mouseStates[0] is 0 and mouseDown is True:
      mouseDown = False

    # Handle user and system events
    for event in GAME_EVENTS.get():

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:  # while moving right, pressing left should have no effect, we also prevent the snake from phasing into itself
                if snake.direction != objects.Direction.right \
                        and not ((snake.body[0][0] == snake.body[1][0])
                                and (snake.body[0][1] - 1 == snake.body[1][1])):
                    snake.direction = objects.Direction.left
            if event.key == pygame.K_RIGHT: # while moving left, pressing right should have no effect, we also prevent the snake from phasing into itself
                if snake.direction != objects.Direction.left \
                        and not ((snake.body[0][0] == snake.body[1][0])
                                and (snake.body[0][1] + 1 == snake.body[1][1])):
                    snake.direction = objects.Direction.right
            if event.key == pygame.K_UP:    # while moving down, pressing up should have no effect, we also prevent the snake from phasing into itself
                if snake.direction != objects.Direction.down\
                        and not ((snake.body[0][0] - 1 == snake.body[1][0])
                                and (snake.body[0][1] == snake.body[1][1])):
                    snake.direction = objects.Direction.up
            if event.key == pygame.K_DOWN:  # while moving up, pressing down should have no effect, we also prevent the snake from phasing into itself
                if snake.direction != objects.Direction.up\
                        and not ((snake.body[0][0] + 1 == snake.body[1][0])
                                and (snake.body[0][1] == snake.body[1][1])):
                    snake.direction = objects.Direction.down
            if event.key == pygame.K_ESCAPE:
                quitGame()

        if event.type == GAME_GLOBALS.QUIT:
            quitGame()


    clock.tick(60)
    pygame.display.update()