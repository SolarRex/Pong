import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import keyboard  # pip install keyboard
import sys

from base_screen import BaseScreen
from button import Button
from title_screen import TitleScreen

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class Pong:
    def __init__(self):
        self.title_screen: BaseScreen = TitleScreen("screen", width=500, height=500)
        self.running = True

    def on_start(self):
        self.running = True
        self.title_screen.on_start()

    def on_end(self):
        print("exiting")
        print("------------------------------")
        self.running = False
        self.title_screen.on_end()
        pygame.quit()

    def toggle_pause(self) -> bool:
        self.pause = not self.pause
        return self.pause


def main():
    pong_game = Pong()
    pong_game.on_start()

    try:
        while pong_game.running:

            pong_game.title_screen.render()
            display.flip()
            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong_game.on_end()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pong_game.on_end()

                    if keyboard.is_pressed("p"):
                        pong_game.toggle_pause()
                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    if pong_game.title_screen.on_button_click():
                        pass
                    else:
                        pong_game.on_end()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        if pong_game.running:
            pong_game.on_end()
            print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()
