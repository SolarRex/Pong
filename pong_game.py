import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import sys
from pynput.keyboard import Key, Listener

from base_screen import BaseScreen
from button import Button
from title_screen import TitleScreen
from game_screen import GameScreen


COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class Pong:
    paused = False

    def __init__(self):
        self.width = 500
        self.height = 500
        self.title_screen: BaseScreen = TitleScreen(
            "screen", width=self.width, height=self.height
        )
        self.game_screen: BaseScreen = GameScreen(
            "screen", width=self.width, height=self.height
        )
        self.running = True

    def on_start(self):
        self.running = True
        self.title_screen.on_start()

    def on_end(self):
        print("exiting")
        print("------------------------------")
        self.running = False
        self.title_screen.on_end()
        self.game_screen.on_end()
        pygame.quit()

    def toggle_pause(self, *kwargs) -> bool:
        self.paused = not self.paused
        self.game_screen.toggle_pause()
        if self.paused:
            print("paused")
        else:
            print("unpaused")

        return self.paused


def main():
    pong_game = Pong()
    pong_game.on_start()

    try:
        while pong_game.running:

            pong_game.title_screen.render()
            pong_game.game_screen.render()
            display.flip()

            # pygame.QUIT event means the user clicked X to close your window
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong_game.on_end()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pong_game.on_end()
                    keys = pygame.key.get_pressed()  # Get state of all keys
                    if keys[pygame.K_p]:
                        if pong_game.game_screen.showing:
                            pong_game.toggle_pause()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    try:
                        pong_game.title_screen
                        if pong_game.title_screen.on_button_click() == "start":
                            pong_game.title_screen.on_end()
                            pong_game.game_screen.on_start()
                        elif pong_game.title_screen.on_button_click() == "exit":
                            pong_game.on_end()
                    except:
                        pass

                    try:
                        pong_game.game_screen
                        if pong_game.game_screen.on_button_click() == "pause":
                            pong_game.toggle_pause()
                        if pong_game.game_screen.on_button_click() == "exit":
                            pong_game.on_end()
                    except:
                        pass

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        if pong_game.running:
            pong_game.on_end()
            print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()
