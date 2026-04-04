import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import keyboard  # pip install keyboard
import sys

from base_screen import BaseScreen
from button import Button

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class GameScreen(BaseScreen):
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
        super().__init__(name)

        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height

        self.display = display.set_mode((self.width, self.height))
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
        self.paused = not self.paused
        return self.paused

    def render(self):
        if self.showing:
            self.display.fill(COLOUR_BLACK)

        if self.paused:
            paused_text = self.font.render(
                f"PAUSED",
                True,
                COLOUR_WHITE,
            )
            paused_text_rect = paused_text.get_rect(
                center=(self.left + self.width / 2, self.top + self.height / 2 - 50)
            )
            self.display.blit(paused_text, paused_text_rect)

            # button

            mouse_pos = pygame.mouse.get_pos()

            self.pause_button = Button(
                "pause_button",
                "Unpause",
                COLOUR_BLACK,
                25,
                (self.width / 2 - 50, self.height / 2 + 50),
                COLOUR_GREEN,
                COLOUR_RED,
                self.left,
                self.top,
            )

            self.pause_button.is_hovering(mouse_pos)
            self.pause_button.draw_button(self.display, 8)

            self.exit_button = Button(
                "exit_button",
                "Exit",
                COLOUR_BLACK,
                25,
                (self.width / 2 + 50, self.height / 2 + 50),
                COLOUR_GREEN,
                COLOUR_RED,
                self.left,
                self.top,
            )

            self.exit_button.is_hovering(mouse_pos)
            self.exit_button.draw_button(self.display, 8)

    def on_button_click(self) -> str:
        # print("Button was clicked!")
        if self.paused:
            try:
                self.pause_button
                if self.pause_button.hovered_over:
                    return "pause"
            except:
                return "didn't press"
            try:
                self.exit_button
                if self.exit_button.hovered_over:
                    print("Exiting Game")
                    self.on_end()
                    return "exit"
            except:
                return "didn't press"
