import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import keyboard  # pip install keyboard
import sys

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class Button:
    """Creates button, position is based on the left and top of the screen."""

    button_text: str = None
    text_colour: tuple = None
    text_size: int = 10
    button_pos: tuple = (0, 0)
    button_base_colour: tuple = None
    button_hover_colour: tuple = None
    button_colour: tuple = None
    left = 0
    top = 0
    button_box = None
    hovered_over = False
    text = None

    def __init__(
        self,
        name,
        button_text: str = None,
        text_colour: tuple = None,
        text_size: int = None,
        button_pos: tuple = None,
        button_base_colour: tuple = None,
        button_hover_colour: tuple = None,
        left: int = 0,
        top: int = 0,
    ):
        self.button_text = button_text
        self.text_colour = text_colour
        self.text_size = text_size
        self.button_pos = button_pos
        self.button_base_colour = button_base_colour
        self.button_hover_colour = button_hover_colour
        self.button_colour = button_base_colour
        self.left = left
        self.top = top

        font_size = font.SysFont("arial", self.text_size)
        self.text = font_size.render(
            self.button_text,
            True,
            self.text_colour,
        )
        self.text_rect = self.text.get_rect(
            center=(self.left + self.button_pos[0], self.top + self.button_pos[1])
        )

        button_padding = 20
        self.button_box = pygame.Rect(
            self.text_rect.left - button_padding,
            self.text_rect.top - button_padding,
            self.text_rect.width + button_padding * 2,
            self.text_rect.height + button_padding * 2,
        )

    def is_hovering(self, mouse_pos):
        self.hovered_over = self.button_box.collidepoint(mouse_pos)

        if self.hovered_over:
            self.button_colour = self.button_hover_colour
        else:
            self.button_colour = self.button_base_colour

    def draw_button(self, screen: Surface, border_radius: int):
        pygame.draw.rect(
            screen,
            self.button_colour,
            self.button_box,
            border_radius=border_radius,
        )

        screen.blit(self.text, self.text_rect)
