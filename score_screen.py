import pygame
from pygame import Surface, transform, font
import argparse
import keyboard  # pip install keyboard
import sys

from base_screen import BaseScreen

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class ScoreScreen(BaseScreen):
    showing = False
    paused = False

    # display location, width, and height
    left: int = None
    top: int = None
    width: int = None
    height: int = None
    bottom: int = None
    right: int = None
    player_score = 0
    cpu_score = 0

    fps = 0

    def __init__(
        self,
        name,
        left=0,
        top=0,
        width=320,
        height=320,
        buttons: list = None,
    ):
        super().__init__(name)

        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.bottom = top + height
        self.right = left + width

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

    def render(self, screen: Surface):
        if self.showing:
            fps_text = self.small_font.render(
                f"FPS: {self.fps:.0f}", True, COLOUR_WHITE
            )
            screen.blit(fps_text, (self.left + 10, self.top + 10))

            pygame.draw.lines(
                screen,
                COLOUR_WHITE,
                True,
                [
                    (self.left, self.bottom - 1),
                    (self.left, self.top),
                    (self.right - 1, self.top),
                    (self.right - 1, self.bottom - 1),
                ],
            )
            scores = self.font.render(
                f"{self.player_score} | {self.cpu_score}",
                True,
                COLOUR_WHITE,
            )
            scores_text_rect = scores.get_rect(
                center=(self.left + self.width / 2, self.top + self.height / 2)
            )
            screen.blit(scores, scores_text_rect)

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
