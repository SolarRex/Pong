import pygame
from pygame import Surface, transform, font
import argparse
import keyboard  # pip install keyboard
import sys

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class BaseScreen:
    showing = False
    paused = False

    # display location, width, and height
    left: int = None
    top: int = None
    width: int = None
    height: int = None

    def __init__(
        self,
        name,
        left=0,
        top=0,
        width=320,
        height=320,
        buttons: list = None,
    ):
        pygame.init()

        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.font = font.SysFont("arial", 50)
        self.small_font = font.SysFont("arial", 25)

    # def __del__(self):
    #     try:
    #         self.on_end()
    #     except:
    #         pass

    def on_start(self) -> bool:
        self.showing = True
        return True

    def on_end(self) -> bool:
        self.showing = False
        return False

    def toggle_pause(self) -> bool:
        self.pause = not self.pause
        return self.pause

    def render(self, screen: Surface, mouse_pos=None):
        raise NotImplementedError()

    def draw_button(
        self,
        button_box,
        button_text,
        button_rect,
        screen: Surface,
        hover=False,
    ):
        raise NotImplementedError()

    def on_button_click():
        raise NotImplementedError()
