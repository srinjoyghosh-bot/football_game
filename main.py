import math

import pygame
import pygame_widgets
from pygame_widgets.button import ButtonArray

# Constants
HEIGHT = 600
GROUND_HEIGHT = 500
WIDTH = 800
PLAYER_RADIUS = 32
BALL_RADIUS = 20
BLACK = (0, 0, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
WHITE = (255, 255, 255)
GAME_NAME = "AirBall"
COLORS = [RED, BLUE, YELLOW, GREEN]

pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
# title and icon
pygame.display.set_caption(GAME_NAME)
icon = pygame.image.load('icon_football.png')
pygame.display.set_icon(icon)

background = pygame.image.load("ground.png")
small_text_font = pygame.font.Font('freesansbold.ttf', 16)

# Teams
team_name_a = "Team A"
team_color_a = 0
team_name_b = "Team B"
team_color_b = 1

# Score board
score_1 = 0
score_2 = 0
score_font = pygame.font.Font('freesansbold.ttf', 32)
score_text_x = WIDTH / 2 - 30
score_text_y = HEIGHT - GROUND_HEIGHT - 80

# countdown clock
clock = pygame.time.Clock()
counter = 60
half_length = 60
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

# Enter names screen
is_name_screen = False
enter_team_a_name = True
color_inactive = pygame.Color('lightskyblue3')
color_active = pygame.Color('dodgerblue2')
color = color_inactive
active = False
text = ''
input_box = pygame.Rect(WIDTH / 2 - 80, HEIGHT / 2, 180, 40)

# Select team color screen
is_color_screen = False
selecting_team_a_color = True
team_color_button_x = [WIDTH / 2 - 100, WIDTH / 2 - 20, WIDTH / 2 + 60, WIDTH / 2 + 140]

# Select half-length screen
is_half_length_screen = False

game_over = False
is_paused = False
is_first_half = True
is_half_time = False
is_full_time = False
is_start_screen = True


def set_half_length(time):
    global counter, is_half_length_screen, half_length
    counter = time
    half_length = time
    is_half_length_screen = False
    print(counter)


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
    counter = 60


def show_ball(x, y):
    pygame.draw.circle(screen, (0, 0, 0), (x, y), BALL_RADIUS)


def show_player1(x, y):
    pygame.draw.circle(screen, COLORS[team_color_a], (x, y), PLAYER_RADIUS)


def show_player2(x, y):
    pygame.draw.circle(screen, COLORS[team_color_b], (x, y), PLAYER_RADIUS)


def is_ball_collision(x1, y1, x2, y2, mx2, my2):
    global ball_x_change, ball_y_change
    v1 = pygame.math.Vector2(x1, y1)
    v2 = pygame.math.Vector2(x2, y2)
    nv = v2 - v1
    m1 = pygame.math.Vector2(ball_x_change, ball_y_change).reflect(nv)
    m2 = pygame.math.Vector2(mx2, my2).reflect(nv)
    if v1.distance_to(v2) <= BALL_RADIUS + PLAYER_RADIUS:
        ball_x_change, ball_y_change = m1.x, m1.y
        return True, m2.x, m2.y
    else:
        return False, -1, -1


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


def show_team_names():
    global team_name_a, team_name_b
    team_1 = score_font.render(team_name_a, True, WHITE)
    pygame.draw.rect(screen, BLACK, (WIDTH - 140, HEIGHT - GROUND_HEIGHT - 40, 200, 30))
    screen.blit(team_1, (WIDTH - 140, HEIGHT - GROUND_HEIGHT - 40))
    team_2 = score_font.render(team_name_b, True, WHITE)
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - GROUND_HEIGHT - 40, 200, 30))
    screen.blit(team_2, (20, HEIGHT - GROUND_HEIGHT - 40))


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
    screen.blit(background, (0, 100))
    time_text_string = get_time_text(time_left + 1)
    pause_text_string = "GAME PAUSED !!"
    score_text_string = f"{score_b} - {score_a}"
    resume_text_string = "Press SPACE to resume game"
    quit_text_string = "Press Q to quit game"

    pause_text = pause_text_font.render(pause_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    time_text = pause_text_font.render(time_text_string, True, BLACK)
    resume_text = score_font.render(resume_text_string, True, BLACK)
    quit_text = score_font.render(quit_text_string, True, BLACK)

    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name
    pygame.draw.rect(screen, BLACK, (WIDTH - 140, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name

    screen.blit(pause_text, (WIDTH / 2 - 250, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(time_text, (WIDTH / 2 - 110, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    screen.blit(resume_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 80))
    screen.blit(quit_text, (WIDTH / 2 - 160, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 120))


def show_half_end_screen(score_a, score_b):
    screen.blit(background, (0, 100))
    pause_text_string = "HALF TIME !!"
    score_text_string = f"{score_b} - {score_a}"
    resume_text_string = "Press SPACE to start 2nd Half"
    quit_text_string = "Press Q to quit game"

    pause_text = pause_text_font.render(pause_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    resume_text = score_font.render(resume_text_string, True, BLACK)
    quit_text = score_font.render(quit_text_string, True, BLACK)

    screen.blit(pause_text, (WIDTH / 2 - 180, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(resume_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    screen.blit(quit_text, (WIDTH / 2 - 160, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 30))

    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name
    pygame.draw.rect(screen, BLACK, (WIDTH - 140, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name


def show_start_screen():
    screen.fill(BLACK)
    game_name = pause_text_font.render(GAME_NAME, True, BLUE)
    start_game_text = score_font.render("Press P to play game", True, WHITE)
    screen.blit(game_name, (WIDTH / 2 - 100, HEIGHT / 2 - 60))
    screen.blit(start_game_text, (WIDTH / 2 - 160, HEIGHT / 2 + 40))


def show_enter_names_screen():
    global team_name_a, team_name_b
    screen.fill(BLACK)
    title = pause_text_font.render('Enter team names', True, BLUE)
    start_game_text = score_font.render("Press ENTER to continue", True, WHITE)
    team_a_name = score_font.render('Team A :', True, WHITE)
    team_b_name = score_font.render('Team B :', True, WHITE)
    limit = small_text_font.render('Use maximum 6 characters', True, BLUE)
    screen.blit(title, (WIDTH / 2 - 280, 60))
    screen.blit(start_game_text, (WIDTH / 2 - 180, HEIGHT - 40))

    screen.blit(limit, (WIDTH / 2 - 90, HEIGHT - 80))

    txt_surface = score_font.render(text, True, color)
    width = max(180, txt_surface.get_width() + 10)
    input_box.w = width
    # Blit the text.
    screen.blit(txt_surface, (input_box.x + 5, input_box.y + 5))
    # Blit the input_box rect.
    pygame.draw.rect(screen, color, input_box, 2)
    if enter_team_a_name:
        screen.blit(team_a_name, (WIDTH / 2 - 60, HEIGHT / 2 - 60))
    else:
        screen.blit(team_b_name, (WIDTH / 2 - 60, HEIGHT / 2 - 60))


def show_select_color_screen():
    screen.fill(BLACK)
    title = pause_text_font.render('Select team color', True, BLUE)
    team_a_name = score_font.render(f'{team_name_a} :', True, WHITE)
    team_b_name = score_font.render(f'{team_name_b} :', True, WHITE)
    screen.blit(title, (WIDTH / 2 - 280, 60))

    if selecting_team_a_color:
        screen.blit(team_a_name, (WIDTH / 2 - 60, HEIGHT / 2 - 60))
    else:
        screen.blit(team_b_name, (WIDTH / 2 - 60, HEIGHT / 2 - 60))
    for i in range(len(COLORS)):
        pygame.draw.circle(screen, COLORS[i], (team_color_button_x[i], HEIGHT / 2 + 60), PLAYER_RADIUS)


def show_select_half_length_screen():
    buttonArray = ButtonArray(
        # Mandatory Parameters
        screen,  # Surface to place button array on
        int(WIDTH / 2 - 150),  # X-coordinate
        int(HEIGHT / 2 - 100),  # Y-coordinate
        300,  # Width
        300,  # Height
        (1, 3),  # Shape: 2 buttons wide, 2 buttons tall
        border=1,  # Distance between buttons and edge of array
        texts=('1 Minute', '2 Minute', '3 Minute'),
        hoverColours=(BLUE, BLUE, BLUE),
        inactiveColours=(BLACK, BLACK, BLACK),
        textColours=(WHITE, WHITE, WHITE),
        onClicks=(lambda: set_half_length(60), lambda: set_half_length(120), lambda: set_half_length(180))
    )
    screen.fill(BLACK)
    title = pause_text_font.render('Select Half Length', True, BLUE)
    screen.blit(title, (WIDTH / 2 - 280, 60))
    buttonArray.draw()


def check_winner(score_a, score_b):
    if score_a > score_b:
        return f"{team_name_a} WON !!"
    elif score_b > score_a:
        return f"{team_name_b} WON !!"
    else:
        return "MATCH TIED !!"


def show_full_time_screen(score_a, score_b):
    screen.blit(background, (0, 100))
    winner_text_string = check_winner(score_a, score_b)
    score_text_string = f"{score_b} - {score_a}"
    restart_text_string = "Press R to restart match"
    quit_text_string = "Press Q to quit game"

    winner_text = pause_text_font.render(winner_text_string, True, BLACK)
    score_text = pause_text_font.render(score_text_string, True, BLACK)
    restart_text = score_font.render(restart_text_string, True, BLACK)
    quit_text = score_font.render(quit_text_string, True, BLACK)

    screen.blit(winner_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 150))
    screen.blit(score_text, (WIDTH / 2 - 65, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 80))
    screen.blit(restart_text, (WIDTH / 2 - 200, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 - 10))
    screen.blit(quit_text, (WIDTH / 2 - 160, HEIGHT - GROUND_HEIGHT + GROUND_HEIGHT / 2 + 30))

    pygame.draw.rect(screen, BLACK, (score_text_x - 20, score_text_y + 40, 110, 30))  # to hide time
    pygame.draw.rect(screen, BLACK, (score_text_x, score_text_y, 100, 30))  # to hide score
    pygame.draw.rect(screen, BLACK, (0, 0, 200, 30))  # to hide half name
    pygame.draw.rect(screen, BLACK, (WIDTH - 140, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name
    pygame.draw.rect(screen, BLACK, (20, HEIGHT - GROUND_HEIGHT - 40, 200, 40))  # hide team name


while not game_over:
    events = pygame.event.get()

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
                    if not is_half_time and not is_full_time and not is_start_screen and not is_name_screen and not is_color_screen and not is_half_length_screen:
                        is_paused = True
                    elif is_half_time:
                        is_half_time = False
                else:
                    is_paused = False
            if event.key == pygame.K_r and is_full_time:
                reset_game_conditions()
                reset_ball_conditions()
                reset_player_conditions()
            if event.key == pygame.K_p and is_start_screen:
                is_start_screen = False
                is_name_screen = True
            if event.key == pygame.K_RETURN or event.key == pygame.K_KP_ENTER:
                if is_name_screen:
                    if enter_team_a_name:
                        enter_team_a_name = False
                        team_name_a = text if len(text) != 0 else 'Team A'
                        text = ''
                        print('A: ' + team_name_a)
                    else:
                        enter_team_a_name = True
                        team_name_b = text if len(text) != 0 else 'Team B'
                        text = ''
                        print('B: ' + team_name_b)
                        is_name_screen = False
                        is_color_screen = True
            if is_name_screen:
                if active:
                    if event.key == pygame.K_BACKSPACE:
                        text = text[:-1]
                    elif event.key != pygame.K_RETURN and event.key != pygame.K_KP_ENTER:
                        if len(text) < 6:
                            text += event.unicode

            if event.key == pygame.K_q and not is_start_screen and not is_name_screen and not is_color_screen and not is_half_length_screen and (
                    is_paused or is_half_time or is_full_time):
                is_start_screen = True
                reset_game_conditions()
                reset_player_conditions()
                reset_ball_conditions()
                if is_paused:
                    is_paused = False
                if is_half_time:
                    is_half_time = False
                if is_full_time:
                    is_full_time = False
        if event.type == timer_event:
            if counter > 0 and not is_paused:
                screen.fill(BLACK)
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
                counter = half_length
            elif counter == 0 and not is_paused and not is_first_half:
                is_full_time = True
            if not is_paused and not is_half_time and not is_full_time and not is_start_screen and not is_name_screen and not is_color_screen and not is_half_length_screen:
                counter -= 1
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            if is_color_screen:
                for i in range(len(team_color_button_x)):
                    dist = math.hypot(team_color_button_x[i] - pos[0], HEIGHT / 2 + 60 - pos[1])
                    if dist <= PLAYER_RADIUS:
                        if selecting_team_a_color:
                            team_color_a = i
                            selecting_team_a_color = False
                            print('A: ' + str(COLORS[i]))
                        else:
                            team_color_b = i
                            selecting_team_a_color = True
                            is_color_screen = False
                            is_half_length_screen = True
                            print('B: ' + str(COLORS[i]))
        if event.type == pygame.MOUSEBUTTONDOWN:
            if input_box.collidepoint(event.pos):
                active = not active
            else:
                active = False
            color = color_active if active else color_inactive

    collision1 = is_ball_collision(player1_x, player1_y, ball_x, ball_y, player1_x_change, player1_y_change)
    if collision1[0]:
        player1_x += collision1[1]
        player1_y += collision1[2]
    collision2 = is_ball_collision(player2_x, player2_y, ball_x, ball_y, player2_x_change, player2_y_change)
    if collision2[0]:
        player2_x += collision2[1]
        player2_y += collision2[2]
    if not is_paused and not is_half_time and not is_full_time and not is_start_screen and not is_name_screen and not is_color_screen and not is_half_length_screen:
        screen.blit(background, (0, 100))
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
        show_team_names()
    elif is_paused:
        show_paused_screen(score_1, score_2, counter)
    elif is_half_time:
        show_half_end_screen(score_1, score_2)
    elif is_full_time:
        show_full_time_screen(score_1, score_2)
    elif is_start_screen:
        show_start_screen()
    elif is_name_screen:
        show_enter_names_screen()
    elif is_color_screen:
        show_select_color_screen()
    elif is_half_length_screen:
        show_select_half_length_screen()
        pygame_widgets.update(events)

    pygame.display.update()
