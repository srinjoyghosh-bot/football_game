import pygame
import math

# Constants
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

# Score board
score_1 = 0
score_2 = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_text_x = WIDTH / 2 - 30
score_text_y = HEIGHT - GROUND_HEIGHT - 80

# countdown clock
clock = pygame.time.Clock()
counter = 180
timer_event = pygame.USEREVENT + 1
pygame.time.set_timer(timer_event, 1000)

pause_text_font = pygame.font.Font('freesansbold.ttf', 64)

# Player 1
player1_x = WIDTH - 20 - PLAYER_RADIUS
player1_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
player1_x_change = 0
player1_y_change = 0

# Player 2
player2_x = 20 + PLAYER_RADIUS
player2_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
player2_x_change = 0
player2_y_change = 0

# Football
ball_x = WIDTH / 2
ball_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
ball_x_change = 6
ball_y_change = 6

game_over = False
is_paused = False
is_first_half = True
is_half_time = False
is_full_time = False


def reset_player_conditions():
    global player1_x, player1_y, player1_x_change, player1_y_change, player2_y, player2_x, player2_x_change, player2_y_change

    # Player 1
    player1_x = WIDTH - 20 - PLAYER_RADIUS
    player1_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
    player1_x_change = 0
    player1_y_change = 0

    # Player 2
    player2_x = 20 + PLAYER_RADIUS
    player2_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
    player2_x_change = 0
    player2_y_change = 0


def reset_ball_conditions():
    global ball_x, ball_y, ball_x_change, ball_y_change

    ball_x = WIDTH / 2
    ball_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
    ball_x_change = 6
    ball_y_change = 6


def reset_game_conditions():
    global game_over, is_paused, is_first_half, is_half_time, is_full_time, score_1, score_2, counter
    game_over = False
    is_paused = False
    is_first_half = True
    is_half_time = False
    is_full_time = False
    score_1 = 0
    score_2 = 0
    counter = 180


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
            return True, -1
        elif x >= WIDTH - BALL_RADIUS:
            score_2 += 1
            return True, 1
    return False, 0


def show_score(x, y):
    global score_1
    global score_2
    score = score_font.render(f"{score_2} - {score_1}", True, WHITE)
    pygame.draw.rect(screen, BLACK, (x, y, 100, 30))
    screen.blit(score, (x, y))


def show_half_name():
    global is_first_half
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))
    if is_first_half:
        half_name = score_font.render("First Half", True, WHITE)
        screen.blit(half_name, (0, 0))
    else:
        half_name = score_font.render("Second Half", True, WHITE)
        screen.blit(half_name, (0, 0))


def get_time_text(time_left):
    min_left = time_left // 60
    sec_left = time_left - (60 * min_left)
    min_left_text = "0" + str(min_left)
    sec_left_text = str(sec_left)
    if sec_left < 10:
        sec_left_text = "0" + sec_left_text
    return min_left_text + " : " + sec_left_text


def show_time(time_left, x, y):
    time_text = get_time_text(time_left)
    time_text = score_font.render(time_text, True, WHITE)
    pygame.draw.rect(screen, BLACK, (x, y, 110, 30))
    screen.blit(time_text, (x, y))


def show_paused_screen(score_a, score_b, time_left):
    time_text_string = get_time_text(time_left + 1)
    pause_text_string = "GAME PAUSED !!"
    score_text_string = f"{score_b} - {score_a}"
    resume_text_string = "Press SPACE to resume game"
    pause_text = pause_text_font.render(pause_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    time_text = pause_text_font.render(time_text_string, True, BLACK)
    resume_text = score_font.render(resume_text_string, True, BLACK)

    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name

    screen.blit(pause_text, (WIDTH / 2 - 250, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(time_text, (WIDTH / 2 - 110, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    screen.blit(resume_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 80))


def show_half_end_screen(score_a, score_b):
    pause_text_string = "HALF TIME !!"
    score_text_string = f"{score_b} - {score_a}"
    resume_text_string = "Press SPACE to start 2nd Half"
    pause_text = pause_text_font.render(pause_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    resume_text = score_font.render(resume_text_string, True, BLACK)
    screen.blit(pause_text, (WIDTH / 2 - 180, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(resume_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name


def check_winner(score_a, score_b):
    if score_a > score_b:
        return "Team A WON !!"
    elif score_b > score_a:
        return "Team B WON !!"
    else:
        return "MATCH TIED !!"


def show_full_time_screen(score_a, score_b):
    winner_text_string = check_winner(score_a, score_b)
    score_text_string = f"{score_b} - {score_a}"
    restart_text_string = "Press R to restart match"
    winner_text = pause_text_font.render(winner_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    restart_text = score_font.render(restart_text_string, True, BLACK)
    screen.blit(winner_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(restart_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name


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
            if event.key == pygame.K_SPACE:
                if not is_paused:
                    if not is_half_time and not is_full_time:
                        is_paused = True
                    else:
                        is_half_time = False
                else:
                    is_paused = False
            if event.key == pygame.K_r and is_full_time:
                reset_game_conditions()
                reset_ball_conditions()
                reset_player_conditions()
        if event.type == timer_event:
            if counter > 0 and not is_paused:
                show_time(counter, score_text_x - 20, score_text_y + 40)
            elif counter == 0 and not is_paused and is_first_half:

                ball_x = WIDTH / 2
                ball_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
                ball_x_change = 6
                ball_y_change = 6
                player1_x = WIDTH - 20 - PLAYER_RADIUS
                player1_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
                player2_x = 20 + PLAYER_RADIUS
                player2_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
                is_first_half = False
                is_half_time = True
                counter = 180
            elif counter == 0 and not is_paused and not is_first_half:
                is_full_time = True
            if not is_paused and not is_half_time and not is_full_time:
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
    if not is_paused and not is_half_time and not is_full_time:
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

        is_goal = check_goal(ball_x, ball_y)
        if is_goal[0]:
            ball_x = WIDTH / 2
            ball_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
            ball_x_change = 6 * is_goal[1]
            ball_y_change = 6
            player1_x = WIDTH - 20 - PLAYER_RADIUS
            player1_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2
            player2_x = 20 + PLAYER_RADIUS
            player2_y = (HEIGHT - GROUND_HEIGHT) + GROUND_HEIGHT / 2

        show_ball(ball_x, ball_y)
        show_player1(player1_x, player1_y)
        show_player2(player2_x, player2_y)
        show_score(score_text_x, score_text_y)
        show_half_name()
    elif is_paused:
        show_paused_screen(score_1, score_2, counter)
    elif is_half_time:
        show_half_end_screen(score_1, score_2)
    elif is_full_time:
        show_full_time_screen(score_1, score_2)

    pygame.display.update()
