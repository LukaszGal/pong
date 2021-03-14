import pygame
import random
from math import copysign
from time import sleep

pygame.init()
pygame.font.init()


global LIFE
LIFE = 10

WIDTH, HIGH = 1200, 700
TABLE_WIDTH, TABLE_HIGH = 20, 150
MENU_WIDTH, MENU_HIGH = WIDTH, 200

FPS = 60
APP = pygame.display.set_mode((WIDTH, HIGH + MENU_HIGH))
pygame.display.set_caption("PONG")
TABLE_SPEED = 16


# colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (65,152,10)

BIG_FONT = pygame.font.SysFont("Times", 150)


class Ball:
    speed = 8
    radius = 20
    color = RED
    ball_speed_x = random.randint(4,speed)
    ball_speed_y = speed - ball_speed_x

    def __init__ (self):
        self.coordinates = [WIDTH // 2, HIGH // 2]
        self.resetGoal()


    def get_coordinates(self):
        return self.coordinates


    def get_color(self):
        return self.color

    def move(self):
        self.coordinates[0] += int(self.ball_speed_x)
        self.coordinates[1] += int(self.ball_speed_y)
        if self.coordinates[1] > HIGH - self.radius or self.coordinates[1] < self.radius:
            self.ball_speed_y *= -1


    def hit(self):
        self.ball_speed_x *= -1
        print(f"BEFORE change: x={self.ball_speed_x}, y= {self.ball_speed_y}")
        self.ball_speed_x = copysign(random.randint(4, self.speed), self.ball_speed_x)
        self.ball_speed_y = copysign(self.speed - abs(self.ball_speed_x), self.ball_speed_y)
        print(f"AFTER change: x={self.ball_speed_x}, y= {self.ball_speed_y}")

    def resetGoal(self):
        print(self.get_coordinates())
        self.coordinates = [WIDTH // 2,  HIGH // 2]
        self.ball_speed_x = copysign(random.randint(4, self.speed), self.ball_speed_x)
        self.ball_speed_y = copysign(self.speed - abs(self.ball_speed_x), self.ball_speed_y)
        sleep(1)

    def checkGoal(self):
        if self.coordinates[0] < - self.radius:
            self.resetGoal()
            return "left"

        if self.coordinates[0] > WIDTH + self.radius:
            self.resetGoal()
            return "right"





class Player:
    table_pointlist_ver = []
    life = 10
    def __init__(self, side, color):
        self.side = side
        self.color = color
        if side == 'left':
            self.coordinates = [10, HIGH//2 - TABLE_HIGH//2]
        elif side == 'right':
            self.coordinates = [WIDTH - TABLE_WIDTH - 10, HIGH//2 - TABLE_HIGH//2]
        self.life = LIFE
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], TABLE_WIDTH, TABLE_HIGH)
        self.updatePointList()

    def get_side(self):
        return self.side

    def get_life(self):
        return self.life

    def get_coordinates(self):
        return self.coordinates

    def decrease_life(self, num=1):
        self.life -= num

    def get_life(self):
        return self.life

    def getPointList(self):
        return self.table_pointlist_ver

    def get_rect(self):
        return self.rect

    def update_rect(self):
        self.rect = pygame.Rect(self.coordinates[0], self.coordinates[1], TABLE_WIDTH, TABLE_HIGH)

    def move_up(self):
        self.coordinates[1] -= TABLE_SPEED
        if self.coordinates[1] < 0:
            self.coordinates[1] = 0
        self.update_rect()
        self.updatePointList()

    def move_down(self):
        self.coordinates[1] += TABLE_SPEED
        if self.coordinates[1] > HIGH - TABLE_HIGH:
            self.coordinates[1] = HIGH - TABLE_HIGH
        self.update_rect()
        self.updatePointList()

    def updatePointList(self):
        self.table_pointlist_ver.clear()
        for i in range(0, TABLE_HIGH):
            self.table_pointlist_ver.append((int(self.coordinates[0] + (int(self.get_side() == "left") * TABLE_WIDTH)), int(self.coordinates[1] + i)))

def drawBoard(players, ball, winner):
    APP.fill(GREEN)
    pygame.draw.rect(APP,BLACK,(0,HIGH, WIDTH, HIGH + MENU_HIGH))

    # draw lines
    pygame.draw.lines(APP, WHITE, True, [(0, 0), (WIDTH, 0), (WIDTH, HIGH), (0, HIGH)], 10)
    pygame.draw.line(APP, WHITE, (WIDTH // 2, 0), ( WIDTH // 2, HIGH),  5)
    pygame.draw.circle(APP, WHITE, (WIDTH // 2,  HIGH // 2), 100, 5)
    pygame.draw.circle(APP, WHITE, (WIDTH // 2, HIGH // 2), 15)

    for player in players:
        pygame.draw.rect(APP, player.color, player.get_rect())

    pygame.draw.circle(APP, ball.get_color(), ball.get_coordinates(), ball.radius)
    # text = GIFT_FONT.render("LAS", True, BLACK)
    # APP.blit(text, (gift[0].x + GIFT_SIZE / 2 - text.get_width()/2, gift[0].y + GIFT_SIZE / 2 - text.get_height()/2))
    TEXT1 = BIG_FONT.render(str(players[0].get_life()), True, WHITE)
    APP.blit(TEXT1, (WIDTH // 4 - TEXT1.get_width()//2 , HIGH + MENU_HIGH // 2 - TEXT1.get_height() // 2) )
    TEXT2 = BIG_FONT.render(":", True, WHITE)
    APP.blit(TEXT2, (WIDTH // 2, HIGH + MENU_HIGH // 2 - TEXT1.get_height() // 2))
    TEXT3 = BIG_FONT.render(str(players[1].get_life()), True, WHITE)
    APP.blit(TEXT3, (WIDTH // 4 * 3 - TEXT3.get_width()//2, HIGH + MENU_HIGH // 2 - TEXT1.get_height() // 2))

    pygame.display.update()



def drawMenu():
    pygame.display.update()


def main():
    winner = ' '
    count_to_next_hit = 0
    i = 0
    menu = True
    run = True
    clock = pygame.time.Clock()
    players = []
    players.append(Player('left', WHITE))
    players.append(Player('right', BLACK))
    ball = Ball()


    while run:
        hit = 0

        count_to_next_hit += 1
        i += 1

        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
                quit()

        keys_pressed = pygame.key.get_pressed()
        for player in players:
            if keys_pressed[pygame.K_UP] and player.get_side() == 'right':
                player.move_up()
            if keys_pressed[pygame.K_DOWN] and player.get_side() == 'right':
                player.move_down()
            if keys_pressed [pygame.K_w] and player.get_side() == 'left':
                player.move_up()
            if keys_pressed [pygame.K_s] and player.get_side() == 'left':
                player.move_down()

        ball.move()
        goal = ball.checkGoal()
        for player in players:
            if player.get_side() == goal:
                player.decrease_life()
                if player.get_life() == 0:
                    run = False #end game
                    if goal == 'left':
                        winner = 'right'
                    elif goal == 'right':
                        winner = 'left'


        for player in players:
            for point in player.getPointList():

                x1, x2 = point
                b1, b2 = ball.get_coordinates()
                if (x1 - b1)**2 + (x2 - b2)**2 <= ball.radius**2:
                    hit = 1
                    a,b,c,d = x1, x2, b1, b2

        print(players[1].getPointList())
        if hit == 1 and count_to_next_hit > FPS:
            count_to_next_hit = 0
            ball.hit()
            print(a,b,c,d)

        drawBoard(players, ball, winner)

    main()


if __name__ == '__main__':
    main()

