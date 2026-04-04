import pygame
from pygame import Surface, display, font, transform, mouse

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class BasePaddle:
    moving_up = 0
    paddle_box = None

    def __init__(
        self,
        name,
        left: float,
        top: float,
        width: float = 5.0,
        height: float = 50.0,
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

    def set_movement(self, up: int = 0) -> int:
        """-1 is moving up, 1 is moving down, 0 for not moving"""
        self.moving_up = up
        return self.moving_up

    def update_position(self, speed: float):
        self.top = self.top + speed * self.moving_up
        self.bottom = self.top + self.height
        self.centery = self.top + self.height / 2

    def draw_paddle(self, screen: Surface):
        self.paddle_box = pygame.Rect(
            self.left,
            self.top,
            self.width,
            self.height,
        )
        pygame.draw.rect(
            screen,
            COLOUR_WHITE,
            self.paddle_box,
        )
