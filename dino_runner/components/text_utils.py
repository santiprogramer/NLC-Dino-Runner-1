import pygame.font

from dino_runner.utils.constants import SCREEN_WIDTH, SCREEN_HEIGHT, NORMAL_MODE, DARK_MODE

FONT_STYLE = "freesansbold.ttf"


def get_score_element(points, dark):
    font = pygame.font.Font(FONT_STYLE, 30)
    if dark:
        text = font.render("Points: {}" .format(points), True, NORMAL_MODE)
    else:
        text = font.render("Points: {}".format(points), True, DARK_MODE)
    text_rect = text.get_rect()
    text_rect.center = (100, 40)
    return text, text_rect


def get_centered_message(message, width=SCREEN_WIDTH//2, height=SCREEN_HEIGHT//2, dark=False):
    font = pygame.font.Font(FONT_STYLE, 30)
    if dark:
        text = font.render(message, True, NORMAL_MODE)
    else:
        text = font.render(message, True, DARK_MODE)
    text_rect = text.get_rect()
    text_rect.center = (width, height)
    return text, text_rect

