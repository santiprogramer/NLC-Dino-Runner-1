import random

import pygame

from dino_runner.components.dinosaur import Dinosaur
from dino_runner.components.life.lives_manager import LivesManager
from dino_runner.components.obstacles.obstacle_manager import ObstacleManager
from dino_runner.components.power_ups.power_up_manager import PowerUpManager
from dino_runner.components.text_utils import get_score_element, get_centered_message
from dino_runner.utils.constants import BG, ICON, SCREEN_HEIGHT, SCREEN_WIDTH, TITLE, FPS, DARK_MODE, NORMAL_MODE, CLOUD
from dino_runner.components import text_utils


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption(TITLE)
        pygame.display.set_icon(ICON)
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.clock = pygame.time.Clock()
        self.playing = False
        self.game_speed = 20
        self.x_pos_bg = 0
        self.y_pos_bg = 380
        self.player = Dinosaur()
        self.obstacle_manage = ObstacleManager()
        self.points = 0
        self.running = True
        self.death_count = 0
        self.dark = False
        self.powerup_manager = PowerUpManager()
        self.lives_manager = LivesManager()

        self.separation = random.randint(350, 450)
        self.x_pos_cloud1 = 0 + self.separation
        self.x_pos_cloud2 = 0 + self.separation*2
        self.x_pos_cloud3 = 0 + self.separation*3
        self.x_pos_cloud4 = 0 + self.separation*4
        self.y_pos_cloud1 = random.randint(100, 250)
        self.y_pos_cloud2 = random.randint(100, 250)
        self.y_pos_cloud3 = random.randint(100, 250)
        self.y_pos_cloud4 = random.randint(100, 250)
        self.separation = 250

    def run(self):
        self.lives_manager.refill_lives()
        self.game_speed = 20
        self.points = 0
        self.create_components()
        # Game loop: events - update - draw
        self.playing = True
        while self.playing:
            self.events()
            self.update()
            self.draw()

    def create_components(self):
        self.obstacle_manage.reset_obstacle()
        self.powerup_manager.reset_power_ups(self.points, self.player)

    def execute(self):
        while self.running:
            if not self.playing:
                self.show_menu()
        pygame.quit()

    def events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.playing = False

    def update(self):
        user_input = pygame.key.get_pressed()
        self.player.update(user_input)
        self.obstacle_manage.update(self)
        self.powerup_manager.update(self.points, self.game_speed, self.player)

    def draw(self):
        self.clock.tick(FPS)
        if self.points % 1000 == 0:
            if(self.points / 1000) % 2 == 0:
                self.dark = False
            else:
                self.dark = True
        if self.dark:
            self.screen.fill(DARK_MODE)
        else:
            self.screen.fill(NORMAL_MODE)
        self.draw_background()
        self.lives_manager.draw(self.screen)
        self.score()
        self.draw_clouds()
        self.player.draw(self.screen)
        self.obstacle_manage.draw(self.screen)
        self.powerup_manager.draw(self.screen)

        pygame.display.update()
        pygame.display.flip()

    def score(self):
        self.points += 1
        if self.points % 100 == 0:
            self.game_speed += 1

        score, score_rect = get_score_element(self.points, self.dark)
        self.screen.blit(score, score_rect)
        self.player.check_invincibility(self.screen, self.dark)

    def show_menu(self):
        self.running = True
        white_color = (255, 255, 255)
        self.screen.fill(white_color)

        self.print_menu_elements(self.death_count)
        #the view of the game is update
        pygame.display.update()

        self.handle_key_events_on_menu()

    def print_menu_elements(self, death_count=0):
        #they are optional
        half_screen_height = SCREEN_HEIGHT//2
        half_screen_width = SCREEN_WIDTH//2
        death_count, death_count_rect = text_utils.get_centered_message("Death count: {}".format(self.death_count), height =half_screen_height+50)
        text, text_rect = get_centered_message('Press any Key to start the game')
        self.screen.blit(text, text_rect)
        self.screen.blit(death_count, death_count_rect)

    def handle_key_events_on_menu(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
                self.playing = False
                pygame.display.quit()
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                self.run()

    def draw_background(self):
        image_width = BG.get_width()
        self.screen.blit(BG, (self.x_pos_bg, self.y_pos_bg))
        self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
        if self.x_pos_bg <= -image_width:
            self.screen.blit(BG, (image_width + self.x_pos_bg, self.y_pos_bg))
            self.x_pos_bg = 0
        self.x_pos_bg -= self.game_speed

    def draw_clouds(self):
        self.screen.blit(CLOUD, (self.x_pos_cloud1, self.y_pos_cloud1))
        self.screen.blit(CLOUD, (self.x_pos_cloud2, self.y_pos_cloud2))
        self.screen.blit(CLOUD, (self.x_pos_cloud3, self.y_pos_cloud3))
        self.screen.blit(CLOUD, (self.x_pos_cloud4, self.y_pos_cloud4))
        self.x_pos_cloud1 -= self.game_speed // 2
        self.x_pos_cloud2 -= self.game_speed // 2
        self.x_pos_cloud3 -= self.game_speed // 2
        self.x_pos_cloud4 -= self.game_speed // 2
        if self.x_pos_cloud1 <=- SCREEN_WIDTH//4:
            self.x_pos_cloud1 = SCREEN_WIDTH
            self.y_pos_cloud1 = random.randint(100, 250)
        if self.x_pos_cloud2 <=- SCREEN_WIDTH//4:
            self.x_pos_cloud2 = SCREEN_WIDTH
            self.y_pos_cloud2 = random.randint(100, 250)
        if self.x_pos_cloud3 <=- SCREEN_WIDTH//4:
            self.x_pos_cloud3 = SCREEN_WIDTH
            self.y_pos_cloud3 = random.randint(100, 250)
        if self.x_pos_cloud4 <=- SCREEN_WIDTH//4:
            self.x_pos_cloud4 = SCREEN_WIDTH
            self.y_pos_cloud4 = random.randint(100, 250)
