from dino_runner.components.power_ups.powerup import PowerUp
from dino_runner.utils.constants import HAMMER, HAMMER_TYPE, SCREEN_WIDTH
import pygame.key


class Hammer(PowerUp):

    def __init__(self):
        self.image = HAMMER
        self.type = HAMMER_TYPE
        self.throw = False
        self.hammers_left = 0
        self.count_hammers = False
        self.hammers_pos = [(25, 85), (65, 85), (105, 85)]
        super().__init__(self.image, self.type)

    def set_pos_hammer(self, dino_rect):
        self.rect.x = dino_rect.x
        self.rect.y = dino_rect.y

    def update_hammer(self, game_speed, powerup):
        self.rect.x += game_speed + 10
        if self.rect.x >= SCREEN_WIDTH:
            self.rect.x = -200
            powerup.throwing_hammer = False

    def draw_hammer(self, screen):
        screen.blit(self.image, self.rect)

    def draw_left_hammers(self, screen):
        counter = 0
        for pos_hammer in self.hammers_pos:
            if counter < self.hammers_left:
                screen.blit(self.image, pos_hammer)
            counter += 1
