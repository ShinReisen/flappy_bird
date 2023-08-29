from typing import Any

import pygame

import sprite_sheet
from settings import screen_height


class Crow(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        crow_sprite = pygame.image.load('img/crow.png')
        crow_sprite_sheet = sprite_sheet.SpriteSheet(crow_sprite)
        BLACK = (0, 0, 0)
        self.animation_list = []
        self.animation_steps = [4, 4, 4]
        self.action = 0
        self.last_update = pygame.time.get_ticks()
        self.animation_cooldown = 100
        self.frame = 0
        self.flying = False
        step_counter = 0
        row_counter = 0

        for animation in self.animation_steps:
            temp_img_list = []
            for _ in range(animation):
                temp_img_list.append(crow_sprite_sheet.get_image(step_counter, 697, 800, 0.1, BLACK, row_counter))
                step_counter += 1
            row_counter += 1
            step_counter = 0
            self.animation_list.append(temp_img_list)

        self.image = self.animation_list[self.action][self.frame]
        self.rect = self.image.get_rect()
        self.rect.center = [x, y]
        self.vel = 0
        self.jumped = False
        self.dead = False


    def update(self, *args: Any, **kwargs: Any) -> None:

        # PHYSICS
        if self.flying:
            # gravity
            self.vel += 0.5
            if self.vel > 8:
                self.vel = 8
            if self.rect.bottom < screen_height:
                self.rect.y += int(self.vel)

        if not self.dead:
            # jump
            self.mid_air = True
            key = pygame.key.get_pressed()
            if (pygame.mouse.get_pressed()[0] or key[pygame.K_SPACE]) and self.jumped == False and self.mid_air == True:
                self.vel = -10
                self.jumped = True
            if not (pygame.mouse.get_pressed()[0] or key[pygame.K_SPACE]):
                self.jumped = False

            # ANIMATION
            current_time = pygame.time.get_ticks()
            if current_time - self.last_update >= self.animation_cooldown:
                self.frame += 1
                self.last_update = current_time
            if self.frame >= len(self.animation_list[self.action]):
                self.frame = 0
            self.image = self.animation_list[self.action][self.frame]

            # rotate the bird
            self.image = pygame.transform.rotate(self.animation_list[self.action][self.frame], self.vel * -2)
        else:
            self.image = pygame.transform.rotate(self.animation_list[self.action][self.frame], -90)
