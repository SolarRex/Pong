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


class TitleScreen(BaseScreen):
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

        self.font = font.SysFont("arial", 50)
        self.small_font = font.SysFont("arial", 25)

    # def __del__(self):
    #     try:
    #         self.on_end()
    #     except:
    #         pass

    def on_start(self) -> bool:
        self.showing = True
        print("starting")
        print("------------------------------")
        return True

    def on_end(self) -> bool:
        self.showing = False
        return False

    def toggle_pause(self) -> bool:
        self.pause = not self.pause
        return self.pause

    def render(self, screen: Surface):
        if self.showing:
            screen.fill(COLOUR_BLACK)
            title = self.font.render(
                f"PONG",
                True,
                COLOUR_WHITE,
            )
            title_text_rect = title.get_rect(
                center=(self.left + self.width / 2, self.top + self.height / 2 - 50)
            )
            screen.blit(title, title_text_rect)

            # button

            mouse_pos = pygame.mouse.get_pos()

            self.start_button = Button(
                "start_button",
                "Start",
                COLOUR_BLACK,
                25,
                (self.width / 2 - 50, self.height / 2 + 50),
                COLOUR_GREEN,
                COLOUR_RED,
                self.left,
                self.top,
            )

            self.start_button.is_hovering(mouse_pos)
            self.start_button.draw_button(screen, 8)

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
            self.exit_button.draw_button(screen, 8)

    def on_button_click(self) -> str:
        # print("Button was clicked!")
        if self.showing:
            try:
                self.start_button
                if self.start_button.hovered_over:
                    print("Starting Game")
                    return "start"
            except:
                return "didn't press"
            try:
                self.exit_button
                if self.exit_button.hovered_over:
                    return "exit"
            except:
                return "didn't press"


def main():

    screen = TitleScreen("screen", width=500, height=500)

    screen.on_start()

    try:
        while screen.showing:
            screen.render()

            display.flip()

            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    screen.on_end()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        screen.on_end()

                    if keyboard.is_pressed("p"):
                        screen.toggle_pause()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    screen.on_button_click()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        if screen.showing:
            screen.on_end()
            print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()
