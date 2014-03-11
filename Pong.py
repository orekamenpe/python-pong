__author__ = 'orekamenpe'

import pygame, random, math

# game settings
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480

COLOR_BLACK = 0, 0, 0
COLOR_GREEN = 166, 206, 57

TEXT_PADDING = 25
PADDLE_SPEED = 5
PADDLE_OFFSET = 10
BALL_SPEED = 3  # initial speed
SPIN_PERCENT = 0.5

# classes

class Vector2:
    def __init__(self, x = 0, y = 0):
        self.x = x
        self.y = y

    def __add__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x + other.x,
                           self.y + other.y)
        else:
            return Vector2(self.x + other,
                           self.y + other)

    def __mul__(self, other):
        if isinstance(other, Vector2):
            return Vector2(self.x * other.x,
                           self.y * other.y)
        else:
            return Vector2(self.x * other,
                           self.y * other)

    def set_zero(self):
        self.x = 0
        self.y = 0

class Actor:
    def __init__(self, texture):
        self.position = Vector2()
        self.velocity = Vector2()
        self.texture = texture

    def get_bounds(self):
        return pygame.Rect(self.position.x,
                           self.position.y,
                           self.texture.get_rect().width,
                           self.texture.get_rect().height)

    def move(self, amount):
        self.position += amount

    def center_y(self):
        self.position.y = SCREEN_HEIGHT / 2 - self.texture.get_rect().height / 2

    def center_xy(self):
        self.position = Vector2(SCREEN_WIDTH / 2 - self.texture.get_rect().width / 2,
                                SCREEN_HEIGHT / 2 - self.texture.get_rect().height / 2)

class Ball(Actor):
    def move(self, amount):
        Actor.move(self, amount)

        if self.position.y < 0:
            self.velocity.y = math.fabs(self.velocity.y)  # do not get stuck
        elif self.position.y > SCREEN_HEIGHT - self.get_bounds().height:
            self.velocity.y = - math.fabs(self.velocity.y)

        if self.get_bounds().right < 0:
            self.launch(BALL_SPEED)  # call launch method
        elif self.get_bounds().left > SCREEN_WIDTH:
            self.launch(BALL_SPEED)  # call launch method

    def launch(self, speed):
        self.center_xy()
        var = random.uniform(-1, 1)

        angle = math.pi / 2 + var
        if random.randint(0, 1) == 0:
            angle += math.pi

        self.velocity.x = math.sin(angle)
        self.velocity.y = math.cos(angle)

        self.velocity *= speed


# functions
def update(elapsedTime):
    timeFactor = elapseTime * 0.05  # redimension the time
    ball.move(ball.velocity * timeFactor)

def draw():
    screen.fill(COLOR_BLACK)
    screen.blit(ball.texture, ball.get_bounds())
    pygame.display.flip()


# initialization
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# textures
ballTexture = pygame.image.load("ball.png")
playerTexture = pygame.image.load("compass.png")

# game objects
ball = Ball(ballTexture)
ball.launch(BALL_SPEED)

player = Actor(playerTexture)

# loop control & timing
gameover = False

lastTick = pygame.time.get_ticks()
elapseTime = 0


# gameloop
while not gameover:
    events = pygame.event.get()
    for event in events:
        if event.type == pygame.QUIT:
            gameover = True
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            gameover = True

    elapseTime = pygame.time.get_ticks() - lastTick
    lastTick = pygame.time.get_ticks()

    update(elapseTime)
    draw()

pygame.quit()



