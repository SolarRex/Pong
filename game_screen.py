import pygame
from pygame import Surface, display, font, transform, mouse
import argparse
import keyboard  # pip install keyboard
import sys
import random

from base_screen import BaseScreen
from button import Button
from base_paddle import BasePaddle
from base_ball import BaseBall

COLOUR_BLACK = (0, 0, 0)
COLOUR_WHITE = (255, 255, 255)
COLOUR_GREEN = (0, 255, 0)
COLOUR_RED = (255, 0, 0)


class GameScreen(BaseScreen):
    showing = False
    paused = False
    player_paddle: BasePaddle = None
    cpu_paddle: BasePaddle = None

    # display location, width, and height
    left: int = None
    top: int = None
    width: int = None
    height: int = None
    bottom: int = None
    right: int = None
    player_score = 0
    cpu_score = 0
    cpu_hold_dir = 0
    ball_speed_max = 0.1
    bot_difficulty = 1

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

        self.player_paddle = BasePaddle(
            "player_paddle", self.left + 20, self.height / 2
        )

        self.cpu_paddle = BasePaddle(
            "cpu_paddle", self.left + self.width - 20, self.height / 2
        )

        self.ball = BaseBall(
            "ball", self.left + self.width / 2, self.top + self.width / 2
        )

    # def __del__(self):
    #     try:
    #         self.on_end()
    #     except:
    #         pass

    def on_start(self) -> bool:
        self.showing = True
        self.paused = False

        self.player_paddle.top = (
            self.top + (self.height - self.player_paddle.height) / 2
        )

        self.cpu_paddle.top = self.top + (self.height - self.cpu_paddle.height) / 2
        self.cpu_paddle.set_movement(random.choice([-1, 1]))

        self.ball.top = self.top + (self.height - self.ball.height) / 2
        self.ball.left = self.left + (self.width - self.ball.width) / 2

        up = random.choice([-1, 1])
        left = random.choice([-1, 1])
        self.ball.set_movement(up, left)

        self.ball_speedx = random.uniform(0.05, self.ball_speed_max)
        self.ball_speedy = random.uniform(0.01, self.ball_speed_max)

        self.player_score = 0
        self.cpu_score = 0

        return True

    def reset_ball(self):
        self.ball.top = self.top + (self.height - self.ball.height) / 2
        self.ball.left = self.left + (self.width - self.ball.width) / 2

        up = random.choice([-1, 1])
        left = random.choice([-1, 1])
        self.ball.set_movement(up, left)

        self.ball_speedx = random.uniform(0.05, self.ball_speed_max)
        self.ball_speedy = random.uniform(0.01, self.ball_speed_max)
        print("ball reset")

    def on_end(self) -> bool:
        self.showing = False
        print("Exiting Game")
        return False

    def toggle_pause(self) -> bool:
        self.paused = not self.paused
        if self.paused:
            self.cpu_hold_dir = self.cpu_paddle.moving_up
            self.cpu_paddle.set_movement(0)
        else:
            self.cpu_paddle.set_movement(self.cpu_hold_dir)

        return self.paused

    def render(self, screen: Surface):
        if self.showing:
            pygame.draw.lines(
                screen,
                COLOUR_WHITE,
                False,
                [
                    (self.left, self.top),
                    (self.right, self.top),
                ],
            )
            pygame.draw.lines(
                screen,
                COLOUR_WHITE,
                False,
                [
                    (self.left, self.bottom - 1),
                    (self.right, self.bottom - 1),
                ],
            )
            self.player_paddle.draw_paddle(screen)
            self.cpu_paddle.draw_paddle(screen)
            self.ball.draw_ball(screen)
            if not self.paused:
                if self.ball.centery < self.cpu_paddle.centery:
                    if self.cpu_paddle.top >= self.top:
                        self.cpu_paddle.set_movement(-1)
                    else:
                        self.cpu_paddle.set_movement(0)

                if self.ball.centery > self.cpu_paddle.centery:
                    if self.cpu_paddle.bottom <= self.bottom:
                        self.cpu_paddle.set_movement(1)
                    else:
                        self.cpu_paddle.set_movement(0)

                self.cpu_paddle.update_position(0.01 * self.bot_difficulty)

                self.player_paddle.update_position(0.1)

                if self.ball.top <= self.top or self.ball.bottom >= self.bottom:
                    self.ball.set_movement(
                        self.ball.moving_up * -1, self.ball.moving_left
                    )
                if (
                    self.player_paddle.paddle_box.collidepoint(
                        self.ball.left, self.ball.top
                    )
                    and self.ball.moving_left == -1
                ) or (
                    self.cpu_paddle.paddle_box.collidepoint(
                        self.ball.right, self.ball.top
                    )
                    and self.ball.moving_left == 1
                ):
                    self.ball.set_movement(
                        self.ball.moving_up, self.ball.moving_left * -1
                    )
                    self.ball_speedx = self.ball_speedx + 0.01

                self.ball.update_position(self.ball_speedx, self.ball_speedy)
            if self.ball.left <= self.left:
                self.cpu_score = self.cpu_score + 1
                self.reset_ball()
                print(self.cpu_score)

            if self.ball.right >= self.right:
                self.player_score = self.player_score + 1
                self.reset_ball()
                print(self.player_score)

        if self.paused:
            paused_text = self.font.render(
                f"PAUSED",
                True,
                COLOUR_WHITE,
            )
            paused_text_rect = paused_text.get_rect(
                center=(self.left + self.width / 2, self.top + self.height / 2 - 50)
            )
            screen.blit(paused_text, paused_text_rect)

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
            self.pause_button.draw_button(screen, 8)

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
                    return "exit"
            except:
                return "didn't press"
