import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import sys

# from pynput.keyboard import Key, Listener
from pynput import keyboard, mouse
import time
import threading
import tkinter as tk

from base_screen import BaseScreen
from button import Button
from title_screen import TitleScreen
from game_screen import GameScreen
from score_screen import ScoreScreen
from winner_screen import WinnerScreen
from IO import Listener


COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)
DEFAULT_WIDTH = "500"
DEFAULT_HEIGHT = "500"
TRUE_SET = {"true", "t", "y", "yes", "1"}
FALSE_SET = {"false", "f", "n", "no", "0"}


class Pong:
    paused = False
    winning_score = 10
    player_score = 0
    cpu_score = 0
    # difficulty ranges from 1 to 10
    bot_difficulty = 1
    number_of_balls = 1

    top_fps = 0
    bottom_fps = 10000
    ave = 0.0
    count = 0

    def __init__(self, width, height, fullscreen, xfullscreen, number_of_balls):
        if fullscreen in TRUE_SET:
            self.width, self.height = self.get_screen_resolution()
        else:
            self.width = width
            self.height = height

        self.number_of_balls = number_of_balls
        self.title_screen: BaseScreen = TitleScreen(
            "title_screen", width=self.width, height=self.height
        )
        self.game_screen: BaseScreen = GameScreen(
            "game_screen",
            top=self.height / 5,
            width=self.width,
            height=self.height * 4 / 5,
            number_of_balls=self.number_of_balls,
        )
        self.score_screen: BaseScreen = ScoreScreen(
            "score_screen", width=self.width, height=self.height / 5
        )
        self.winner_screen: BaseScreen = WinnerScreen(
            "winner_screen", width=self.width, height=self.height
        )
        if xfullscreen in TRUE_SET:
            self.display = pygame.display.set_mode(
                (self.width, self.height), pygame.FULLSCREEN
            )
        else:
            self.display = pygame.display.set_mode((self.width, self.height))
        self.running = True
        self.bot_difficulty = 5

        self.clock = pygame.time.Clock()
        self.previous_time_tick = time.time()

    def on_callback(self, callable):
        threading.Thread(target=callable, daemon=True).start()

    def on_start(self):

        self.running = True
        self.title_screen.on_start()
        # self.listeners = Listener(
        #     keyboard.Listener(
        #         on_press=self.on_key_press, on_release=self.on_key_release
        #     ),
        #     mouse.Listener(on_click=self.on_click),
        # )
        # self.on_callback(self.listeners.on_start)
        self.player_score = 0
        self.cpu_score = 0
        self.game_screen.player_score = self.player_score
        self.game_screen.cpu_score = self.cpu_score
        self.game_screen.bot_difficulty = self.bot_difficulty
        self.game_screen.number_of_balls = self.number_of_balls
        if self.bot_difficulty < 1:
            print("setting bot difficulty to 1")
            self.bot_difficulty = 1
        elif self.bot_difficulty > 10:
            print("setting bot difficulty to 10")
            self.bot_difficulty = 10

    def on_restart(self):
        self.running = False
        self.title_screen.on_end()
        self.game_screen.on_end()
        self.score_screen.on_end()
        self.winner_screen.on_end()
        # self.on_callback(self.listeners.on_end)
        print("Restarting")
        time.sleep(2)
        self.on_start()

    def on_end(self):
        self.running = False
        self.title_screen.on_end()
        self.game_screen.on_end()
        self.score_screen.on_end()
        self.winner_screen.on_end()
        # self.on_callback(self.listeners.on_end)
        print("exiting")
        print("------------------------------")
        print(f"Top FPS was {self.top_fps}")
        print(f"Bottom FPS was {self.bottom_fps}")
        print(f"The average FPS was {self.ave/self.count}")
        pygame.quit()

    def toggle_pause(self, *kwargs) -> bool:
        self.paused = not self.paused
        self.game_screen.toggle_pause()
        if self.paused:
            print("paused")
        else:
            print("unpaused")

        return self.paused

    # --- Keyboard event handlers ---
    def on_key_press(self, key):
        # print(f"Key pressed: {key}")  # Printable keys
        if key == keyboard.Key.up:
            if self.game_screen.player_paddle.top > self.game_screen.top:
                self.game_screen.player_paddle.set_movement(-1)
            else:
                self.game_screen.player_paddle.set_movement(0)
                # self.game_screen.player_paddle.top = self.game_screen.top #brute force method
        elif key == keyboard.Key.down:
            if self.game_screen.player_paddle.bottom < self.game_screen.bottom:
                self.game_screen.player_paddle.set_movement(1)
            else:
                self.game_screen.player_paddle.set_movement(0)

    def on_key_release(self, key):
        print(f"Key released: {key}")
        if key == keyboard.Key.esc:  # Stop listener on ESC
            print("Stopping listeners...")
            self.on_end()
            return False  # Returning False stops the listener
        elif key == keyboard.Key.up or key == keyboard.Key.down:
            self.game_screen.player_paddle.set_movement(0)

    # --- Mouse event handlers ---
    def on_click(self, x, y, button, pressed):
        if pressed:
            print(f"Mouse button {button} pressed at ({x}, {y})")
        else:
            print(f"Mouse button {button} released at ({x}, {y})")

    def get_screen_resolution(self):
        try:
            root = tk.Tk()
            root.withdraw()  # Hide the main window
            width = root.winfo_screenwidth()
            height = root.winfo_screenheight()
            root.destroy()
            return width, height
        except Exception as e:
            print(
                f"Error retrieving resolution: {e}. Setting to default resolution ({DEFAULT_WIDTH}, {DEFAULT_HEIGHT})"
            )
            return None, None


def main():
    parser = argparse.ArgumentParser(description="Start the game with bot difficulty")
    parser.add_argument(
        "--bot_difficulty",
        type=str,
        default="5",
        help="The bot difficulty which ranges from 1 to 10, out of this range will set to either 1 or 10.",
    )
    parser.add_argument(
        "--width",
        type=str,
        default=DEFAULT_WIDTH,
        help="Sets the width of the screen.",
    )
    parser.add_argument(
        "--height",
        type=str,
        default=DEFAULT_HEIGHT,
        help="Sets the height of the screen.",
    )
    parser.add_argument(
        "--fullscreen",
        type=str,
        default="False",
        help="Sets to the monitors resolution.",
    )
    parser.add_argument(
        "--exclusive_fullscreen",
        type=str,
        default="False",
        help="Sets to exclusive fullscreen.",
    )
    parser.add_argument(
        "--number_of_balls",
        type=str,
        default=1,
        help="Sets the number of balls.",
    )

    args = parser.parse_args()
    args_info = {
        "width": int(args.width),
        "height": int(args.height),
        "fullscreen": args.fullscreen.lower(),
        "xfullscreen": args.exclusive_fullscreen.lower(),
        "number_of_balls": int(args.number_of_balls),
    }

    pong_game = Pong(
        width=args_info["width"],
        height=args_info["height"],
        fullscreen=args_info["fullscreen"],
        xfullscreen=args_info["xfullscreen"],
        number_of_balls=args_info["number_of_balls"],
    )
    pong_game.on_start()

    pong_game.count = 0
    pong_game.ave = 0

    try:
        while pong_game.running:
            pong_game.clock.tick(0)
            fps = pong_game.clock.get_fps()

            if time.time() - pong_game.previous_time_tick >= 1.0:
                pong_game.previous_time_tick = time.time()
                pong_game.score_screen.fps = fps
                print(fps)

            pong_game.top_fps = max(fps, pong_game.top_fps)
            pong_game.bottom_fps = min(fps, pong_game.bottom_fps)
            pong_game.ave = pong_game.ave + fps
            pong_game.count = pong_game.count + 1

            pong_game.display.fill(COLOUR_BLACK)

            if not pong_game.winner_screen.showing and (
                pong_game.player_score >= pong_game.winning_score
                or pong_game.cpu_score >= pong_game.winning_score
            ):
                pong_game.title_screen.on_end()
                pong_game.game_screen.on_end()
                pong_game.score_screen.on_end()
                pong_game.winner_screen.set_winner(
                    pong_game.player_score >= pong_game.winning_score
                )
                pong_game.winner_screen.on_start()

            else:
                mouse_pos = pygame.mouse.get_pos()
                pong_game.title_screen.render(pong_game.display, mouse_pos)
                pong_game.game_screen.render(pong_game.display, mouse_pos)

                pong_game.player_score = pong_game.game_screen.player_score
                pong_game.cpu_score = pong_game.game_screen.cpu_score
                pong_game.score_screen.player_score = pong_game.player_score
                pong_game.score_screen.cpu_score = pong_game.cpu_score

                pong_game.score_screen.render(pong_game.display)

            pong_game.winner_screen.render(pong_game.display)

            # pygame.QUIT event means the user clicked X to close your window
            keys = pygame.key.get_pressed()

            if keys[pygame.K_UP]:
                if pong_game.game_screen.player_paddle.top > pong_game.game_screen.top:
                    pong_game.game_screen.player_paddle.set_movement(-1)
                else:
                    pong_game.game_screen.player_paddle.set_movement(0)
            elif keys[pygame.K_DOWN]:
                if (
                    pong_game.game_screen.player_paddle.bottom
                    < pong_game.game_screen.bottom
                ):
                    pong_game.game_screen.player_paddle.set_movement(1)
                else:
                    pong_game.game_screen.player_paddle.set_movement(0)
            else:
                pong_game.game_screen.player_paddle.set_movement(0)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pong_game.on_end()
                    return
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE:
                        pong_game.on_end()
                        return
                    if event.key == pygame.K_p:
                        if pong_game.game_screen.showing:
                            pong_game.toggle_pause()
                    if event.key == pygame.K_r and not pong_game.title_screen.showing:
                        pong_game.on_restart()

                elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                    try:
                        pong_game.title_screen
                        if pong_game.title_screen.on_button_click() == "start":
                            pong_game.title_screen.on_end()
                            pong_game.game_screen.on_start()
                            pong_game.score_screen.on_start()
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
            display.flip()

    except KeyboardInterrupt:
        # Handle Ctrl+C gracefully
        if pong_game.running:
            pong_game.on_end()
            print("\nProgram interrupted by user.")


if __name__ == "__main__":
    main()
