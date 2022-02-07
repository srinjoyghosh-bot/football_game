import pygame
import math

HEIGHT = 600
GROUND_HEIGHT = 500
WIDTH = 800
PLAYER_RADIUS = 32
BALL_RADIUS = 16
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
WHITE = (255, 255, 255)

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))

background = pygame.image.load("ground.png")

score_1 = 0
score_2 = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_text_x = WIDTH / 2 - 30
score_text_y = HEIGHT - GROUND_HEIGHT - 80

clock = pygame.time.Clock()
counter = 180
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

player1_x = WIDTH - 20 - PLAYER_RADIUS
player1_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
player1_x_change = 0
player1_y_change = 0

player2_x = 20 + PLAYER_RADIUS
player2_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
player2_x_change = 0
player2_y_change = 0

ball_x = WIDTH / 2
ball_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
ball_x_change = 6
ball_y_change = 6

game_over = False


def show_ball(x, y):
    pygame.draw.circle(screen, (0, 0, 0), (x, y), 20)


def show_player1(x, y):
    pygame.draw.circle(screen, RED, (x, y), 32)


def show_player2(x, y):
    pygame.draw.circle(screen, BLUE, (x, y), 32)


def is_ball_collision(x1, y1, x2, y2):
    distance = math.sqrt((math.pow(x1 - x2, 2)) + math.pow(y1 - y2, 2))
    if distance <= BALL_RADIUS + PLAYER_RADIUS:
        return True
    else:
        return False


def check_goal(x, y):
    global score_1
    global score_2
    if HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 98 - BALL_RADIUS > y > HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 98 + BALL_RADIUS:
        if x <= BALL_RADIUS:
            score_1 += 1
            print(f'team 1 {score_1}')
            # show_score(score_text_x, score_text_y)
        elif x >= WIDTH - BALL_RADIUS:
            score_2 += 1
            print(f'team 2 {score_2}')
            # show_score(score_text_x, score_text_y)


def show_score(x, y):
    global score_1
    global score_2
    score = score_font.render(f"{score_2} - {score_1}", True, WHITE)
    pygame.draw.rect(screen, BLACK, (x, y, 80, 30))
    screen.blit(score, (x, y))


def show_time(time_left, x, y):
    min_left = time_left // 60
    sec_left = time_left - (60 * min_left)
    min_left_text = "0" + str(min_left)
    sec_left_text = str(sec_left)
    if sec_left < 10:
        sec_left_text = "0" + sec_left_text

    time_text = score_font.render(min_left_text + " : " + sec_left_text, True, WHITE)
    pygame.draw.rect(screen, BLACK, (x, y, 110, 30))
    screen.blit(time_text, (x, y))


while not game_over:
    screen.blit(background, (0, 100))
    clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                player1_y_change = -4
            if event.key == pygame.K_DOWN:
                player1_y_change = 4
            if event.key == pygame.K_LEFT:
                player1_x_change = -4
            if event.key == pygame.K_RIGHT:
                player1_x_change = 4
            if event.key == pygame.K_w:
                player2_y_change = -4
            if event.key == pygame.K_s:
                player2_y_change = 4
            if event.key == pygame.K_a:
                player2_x_change = -4
            if event.key == pygame.K_d:
                player2_x_change = 4
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player1_x_change = 0
            if event.key == pygame.K_UP or event.key == pygame.K_DOWN:
                player1_y_change = 0
            if event.key == pygame.K_a or event.key == pygame.K_d:
                player2_x_change = 0
            if event.key == pygame.K_w or event.key == pygame.K_s:
                player2_y_change = 0
        if event.type == timer_event:
            if counter >= 0:
                show_time(counter, score_text_x - 20, score_text_y + 40)
            counter -= 1

    collision1 = is_ball_collision(player1_x, player1_y, ball_x, ball_y)
    if collision1:
        if (ball_x < player1_x and ball_y > player1_y) or (ball_x > player1_x and ball_y < player1_y):
            ball_y_change *= -1
        if (ball_x > player1_x and ball_y > player1_y) or (ball_x < player1_x and ball_y < player1_y):
            ball_x_change *= -1
    collision2 = is_ball_collision(player2_x, player2_y, ball_x, ball_y)
    if collision2:
        if (ball_x > player2_x and ball_y > player2_y) or (ball_x < player2_x and ball_y < player2_y):
            ball_x_change *= -1
        if (ball_x > player2_x and ball_y < player2_y) or (ball_x < player2_x and ball_y > player2_y):
            ball_y_change *= -1

    # if ball_x == BALL_RADIUS:
    #     score_1 += 1
    #     print(score_1)
    player1_x += player1_x_change
    if player1_x <= WIDTH / 2 + PLAYER_RADIUS:
        player1_x = WIDTH / 2 + PLAYER_RADIUS
    elif player1_x >= WIDTH - PLAYER_RADIUS:
        player1_x = WIDTH - PLAYER_RADIUS

    player1_y += player1_y_change
    if player1_y <= HEIGHT - GROUND_HEIGHT + PLAYER_RADIUS:
        player1_y = HEIGHT - GROUND_HEIGHT + PLAYER_RADIUS
    elif player1_y >= HEIGHT - PLAYER_RADIUS:
        player1_y = HEIGHT - PLAYER_RADIUS

    player2_x += player2_x_change
    if player2_x <= PLAYER_RADIUS:
        player2_x = PLAYER_RADIUS
    elif player2_x >= WIDTH / 2 - PLAYER_RADIUS:
        player2_x = WIDTH / 2 - PLAYER_RADIUS

    player2_y += player2_y_change
    if player2_y <= HEIGHT - GROUND_HEIGHT + PLAYER_RADIUS:
        player2_y = HEIGHT - GROUND_HEIGHT + PLAYER_RADIUS
    elif player2_y >= HEIGHT - PLAYER_RADIUS:
        player2_y = HEIGHT - PLAYER_RADIUS

    ball_x += ball_x_change
    if ball_x <= BALL_RADIUS or ball_x >= WIDTH - BALL_RADIUS:
        ball_x_change *= -1

    ball_y += ball_y_change
    if ball_y <= HEIGHT - GROUND_HEIGHT + BALL_RADIUS or ball_y >= HEIGHT - BALL_RADIUS:
        ball_y_change *= -1

    check_goal(ball_x, ball_y)
    show_ball(ball_x, ball_y)
    show_player1(player1_x, player1_y)
    show_player2(player2_x, player2_y)
    show_score(score_text_x, score_text_y)
    # show_time(score_text_x,score_text_y+40)

    pygame.display.update()
