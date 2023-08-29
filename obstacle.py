import pygame.sprite


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, x, y, position):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('img/pipe.png')
        # self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], y))
        self.rect = self.image.get_rect()
        self.gap = 250
        # position 1 is from the top, -1 is from the bottom
        if position == 1:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect.bottomleft = [x, y - int(self.gap / 2)]
        if position == -1:
            self.rect.topleft = [x, y + int(self.gap / 2)]

    def update(self, scroll_speed):
        self.rect.x -= scroll_speed
        if self.rect.right < 0:
            self.kill()