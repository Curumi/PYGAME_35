import sys
import pygame as pg
from pygame.constants import *

pg.init()

SCREEN_WIDTH = 1200
SCREEN_HEIGHT = 720
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pg.display.set_caption("Pong Game")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

PADDLE_WIDTH = 25
PADDLE_HEIGHT = 100
PADDLE_SPEED = 10

BALL_SIZE = 10
INITIAL_BALL_SPEED_X = 5
INITIAL_BALL_SPEED_Y = 5
MAX_BALL_SPEED = 30

paddle1_rect = pg.Rect(0, SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                       PADDLE_WIDTH, PADDLE_HEIGHT)
paddle2_rect = pg.Rect(SCREEN_WIDTH - PADDLE_WIDTH,
                       SCREEN_HEIGHT // 2 - PADDLE_HEIGHT // 2,
                       PADDLE_WIDTH, PADDLE_HEIGHT)
ball_rect = pg.Rect(SCREEN_WIDTH // 2 - BALL_SIZE // 2,
                    SCREEN_HEIGHT // 2 - BALL_SIZE // 2,
                    BALL_SIZE, BALL_SIZE)

score1 = 0
score2 = 0

ball_speed_x = INITIAL_BALL_SPEED_X
ball_speed_y = INITIAL_BALL_SPEED_Y
speed_increase = 1.1

font = pg.font.Font(None, 32)

try:
    hit_sound = pg.mixer.Sound("hit.wav")
    score_sound = pg.mixer.Sound("score.wav")
except:
    hit_sound = pg.mixer.Sound(buffer=bytearray(0))
    score_sound = pg.mixer.Sound(buffer=bytearray(0))

FPS = 60
clock = pg.time.Clock()
running = True

ai_mode = True
if len(sys.argv) > 1 and sys.argv[1] == '--human':
    ai_mode = False

def reset_ball(direction):
    global ball_speed_x, ball_speed_y
    ball_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    ball_speed_x = INITIAL_BALL_SPEED_X * direction
    ball_speed_y = INITIAL_BALL_SPEED_Y * (1 if pg.time.get_ticks() % 2 == 0 else -1)

def update_ai():
    if ball_rect.x > SCREEN_WIDTH // 2:
        if ball_rect.centery < paddle2_rect.centery:
            paddle2_rect.y -= PADDLE_SPEED
        elif ball_rect.centery > paddle2_rect.centery:
            paddle2_rect.y += PADDLE_SPEED
        if paddle2_rect.top < 0:
            paddle2_rect.top = 0
        if paddle2_rect.bottom > SCREEN_HEIGHT:
            paddle2_rect.bottom = SCREEN_HEIGHT
    else:
        paddle2_rect.centery += (SCREEN_HEIGHT // 2 - paddle2_rect.centery) / PADDLE_SPEED

def increase_ball_speed():
    global ball_speed_x, ball_speed_y
    ball_speed_x *= speed_increase
    ball_speed_y *= speed_increase
    if abs(ball_speed_x) > MAX_BALL_SPEED:
        ball_speed_x = MAX_BALL_SPEED if ball_speed_x > 0 else -MAX_BALL_SPEED
    if abs(ball_speed_y) > MAX_BALL_SPEED:
        ball_speed_y = MAX_BALL_SPEED if ball_speed_y > 0 else -MAX_BALL_SPEED

reset_ball(1)

while running:
    for event in pg.event.get():
        if event.type == pg.QUIT:
            running = False

    keys = pg.key.get_pressed()
    if keys[K_w]:
        paddle1_rect.y -= PADDLE_SPEED
        if paddle1_rect.top <= 0:
            paddle1_rect.top = 0
    if keys[K_s]:
        paddle1_rect.y += PADDLE_SPEED
        if paddle1_rect.bottom >= SCREEN_HEIGHT:
            paddle1_rect.bottom = SCREEN_HEIGHT

    if not ai_mode:
        if keys[K_UP]:
            paddle2_rect.y -= PADDLE_SPEED
            if paddle2_rect.top <= 0:
                paddle2_rect.top = 0
        if keys[K_DOWN]:
            paddle2_rect.y += PADDLE_SPEED
            if paddle2_rect.bottom >= SCREEN_HEIGHT:
                paddle2_rect.bottom = SCREEN_HEIGHT
    else:
        update_ai()

    ball_rect.x += ball_speed_x
    ball_rect.y += ball_speed_y

    if ball_rect.top <= 0 or ball_rect.bottom >= SCREEN_HEIGHT:
        ball_speed_y *= -1
        hit_sound.play()

    if ball_rect.colliderect(paddle1_rect) or ball_rect.colliderect(paddle2_rect):
        ball_speed_x *= -1
        increase_ball_speed()
        hit_sound.play()

    if ball_rect.left <= 0:
        score2 += 1
        score_sound.play()
        reset_ball(1)

    if ball_rect.right >= SCREEN_WIDTH:
        score1 += 1
        score_sound.play()
        reset_ball(-1)

    screen.fill(BLACK)

    pg.draw.rect(screen, WHITE, paddle1_rect)
    pg.draw.rect(screen, WHITE, paddle2_rect)
    pg.draw.ellipse(screen, WHITE, ball_rect)
    pg.draw.aaline(screen, WHITE, (SCREEN_WIDTH // 2, 0), (SCREEN_WIDTH // 2, SCREEN_HEIGHT))

    score_text = font.render(f'{score1} : {score2}', True, WHITE)
    screen.blit(score_text, (SCREEN_WIDTH // 2 - score_text.get_width() // 2, 10))

    speed_text = font.render(f'Speed: {int(abs(ball_speed_x))}', True, WHITE)
    screen.blit(speed_text, (SCREEN_WIDTH // 2 - speed_text.get_width() // 2, 50))

    pg.display.flip()
    clock.tick(FPS)

pg.quit()
