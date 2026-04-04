import pygame
from pygame import Surface, display, font, transform, mouse

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class BaseBall:
    moving_up = 0
    moving_left = 0

    def __init__(
        self,
        name,
        left: float,
        top: float,
        width: float = 5.0,
        height: float = 5.0,
    ):
        pygame.init()

        self.name = name
        self.left = left
        self.top = top
        self.right = left + width
        self.bottom = top + height
        self.width = width
        self.height = height
        self.centerx = left - width / 2
        self.centery = top + height / 2

    def set_movement(self, up: int = 0, left: int = 0) -> tuple:
        """-1 is moving up or left, 1 is moving down or right, 0 for not moving"""
        self.moving_up = up
        self.moving_left = left
        return (self.moving_up, self.moving_left)

    def update_position(self, speedx: float, speedy: float):
        self.top = self.top + (speedx * self.moving_up)
        self.bottom = self.top + self.height
        self.centery = self.top + self.height / 2

        self.left = self.left + (speedy * self.moving_left)
        self.right = self.left + self.width
        self.centerx = self.left + self.width / 2

    def draw_ball(self, screen: Surface):
        ball_box = pygame.Rect(
            self.left,
            self.top,
            self.width,
            self.height,
        )
        pygame.draw.rect(
            screen,
            COLOUR_WHITE,
            ball_box,
        )
