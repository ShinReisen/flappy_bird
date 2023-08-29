import pygame
from pygame.locals import *
import random
from button import Button
from crow import Crow
from obstacle import Obstacle
from settings import screen_width, screen_height, fps, obstacle_frequency

pygame.init()

clock = pygame.time.Clock()

screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Owl')

# define game variables
bg_scroll = 0
scroll_speed = 2
game_over = False
last_obstacle = pygame.time.get_ticks() - obstacle_frequency
score = 0
pass_obstacle = False

font = pygame.font.SysFont('Bauhaus 93', 60)
white = (255, 255, 255)

# load images
bg_img = pygame.image.load('img/bg.png')
bg_img = pygame.transform.scale(bg_img, (screen_width, screen_height))
button_img = pygame.image.load('img/restart.png')

pygame.mixer.init()
pygame.mixer.music.load('sound/bg.ogg')
# pygame.mixer.music.play()
game_over_sound = pygame.mixer.Sound("sound/gameover.wav")
game_over_sound_played = False

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def reset_game():
    obstacle_group.empty()
    flappy.rect.x = 100
    flappy.rect.y = int(screen_height / 2)
    flappy.dead = False
    flappy.flying = False
    score = 0
    return score


bird_group = pygame.sprite.Group()
obstacle_group = pygame.sprite.Group()

flappy = Crow(100, int(screen_height / 2))
bird_group.add(flappy)

# create restart button instance
button = Button(screen_width // 2 - 50, screen_height // 2 - 100, button_img, screen)

run = True
while run:


    obstacle_frequency = int(6000 / scroll_speed)

    clock.tick(fps)

    screen.fill((0, 0, 0))
    screen.blit(bg_img, (bg_scroll, 0))
    screen.blit(bg_img, (screen_width + bg_scroll, 0))

    # check the score
    if len(obstacle_group) > 0:
        if bird_group.sprites()[0].rect.left > obstacle_group.sprites()[0].rect.left \
                and bird_group.sprites()[0].rect.right < obstacle_group.sprites()[0].rect.right \
                and not pass_obstacle:
            pass_obstacle = True
        if pass_obstacle:
            if bird_group.sprites()[0].rect.right > obstacle_group.sprites()[0].rect.right:
                score += 1
                pass_obstacle = False



    if not game_over and flappy.flying:

        # generate new obstacles
        time_now = pygame.time.get_ticks()
        if time_now - last_obstacle > obstacle_frequency:
            obstacle_height = random.randint(-100, 100)
            btm_obstacle = Obstacle(screen_width, int(screen_height / 2) + obstacle_height, -1)
            top_obstacle = Obstacle(screen_width, int(screen_height / 2) + obstacle_height, 1)
            obstacle_group.add(btm_obstacle)
            obstacle_group.add(top_obstacle)
            last_obstacle = time_now

        # background scrolling
        if abs(bg_scroll) >= screen_width:
            screen.blit(bg_img, (screen_width + bg_scroll, 0))
            bg_scroll = 0
            if scroll_speed < 6:
                scroll_speed += 1
        bg_scroll -= scroll_speed
        obstacle_group.update(scroll_speed)

    obstacle_group.draw(screen)
    draw_text(str(score), font, white, int(screen_width / 2), 20)
    bird_group.draw(screen)
    bird_group.update()

    # look for collision
    if pygame.sprite.groupcollide(bird_group, obstacle_group, False, False) or flappy.rect.top < 0:
        game_over = True

    # check if bird hit the ground
    if flappy.rect.bottom >= screen_height:
        game_over = True
        flappy.flying = False
        flappy.dead = True

    # check for game over and reset
    if game_over == True:
        if not game_over_sound_played:
            pygame.mixer.Sound.play(game_over_sound)
            pygame.mixer.music.stop()
        game_over_sound_played = True
        if button.draw():
            game_over = False
            game_over_sound_played = False
            scroll_speed = 2
            score = reset_game()


    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and not (flappy.flying or game_over):
            flappy.flying = True
            pygame.mixer.music.play()
        # if event.type == pygame.KEYDOWN:
        #     if event.key == pygame.K_DOWN and action > 0:
        #         action -= 1
        #         frame = 0
        #     if event.key == pygame.K_UP and action < len(animation_list) - 1:
        #         action += 1
        #         frame = 0

    pygame.display.update()

pygame.quit()
