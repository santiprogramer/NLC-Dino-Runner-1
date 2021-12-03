import random
import pygame

from dino_runner.components.power_ups.hammer import Hammer
from dino_runner.components.power_ups.shield import Shield
from dino_runner.utils.constants import DEFAULT_TYPE, SHIELD_TYPE, HAMMER_TYPE


class PowerUpManager:

    def __init__(self):
        self.power_ups = []
        self.when_appears = 0
        self.points = 0
        self.option_numbers = list(range(1, 10))
        self.throwing_hammer = False
        self.hammer = Hammer()

    def reset_power_ups(self, points, player):
        self.hammer.hammers_left = 0
        self.power_ups = []
        self.points = points
        self.when_appears = random.randint(200, 300) + self.points
        player.hammer = False
        player.type = DEFAULT_TYPE

    def generate_power_ups(self, points, player):
        self.points = points
        if len(self.power_ups) == 0:
            if self.when_appears == self.points:
                print("generating powerup")
                self.when_appears = random.randint(self.when_appears + 200, 500 + self.when_appears)
                if player.type == DEFAULT_TYPE:
                    self.power_ups.append(random.choice([Shield(), Hammer()]))

    def update(self, points, game_speed, player):
        self.generate_power_ups(points, player)
        for power_up in self.power_ups:
            power_up.update(game_speed, self.power_ups)
            if player.dino_rect.colliderect(power_up.rect):
                player.type = power_up.type
                power_up.start_time = pygame.time.get_ticks ()
                time_random = random.randrange(5, 8)
                self.power_ups.remove(power_up)
                if player.type == SHIELD_TYPE:
                    player.shield = True
                    player.show_text = True
                    player.shield_time_up = power_up.start_time + (time_random * 1000)

                if player.type == HAMMER_TYPE:
                    self.hammer.count_hammers = True
                    player.hammer = True
                    player.hammer_time_up = power_up.start_time + (time_random*1000)
                    self.hammer.hammers_left = 3

        user_input = pygame.key.get_pressed()
        if user_input[pygame.K_SPACE] and player.hammer and not self.throwing_hammer and self.hammer.hammers_left > 0:
            self.throwing_hammer = True
            self.hammer.set_pos_hammer(player.dino_rect)
            self.hammer.hammers_left -= 1
            if self.hammer.hammers_left == 0:
                player.type = DEFAULT_TYPE

        if self.throwing_hammer:
            self.hammer.update_hammer(game_speed, self)

    def draw(self, screen):
        for power_up in self.power_ups:
            power_up.draw(screen)

        if self.throwing_hammer:
            self.hammer.draw_hammer(screen)

        if self.hammer.hammers_left > 0:
            self.hammer.draw_left_hammers(screen)