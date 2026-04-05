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
    ball_speedx_max = 0.1
    ball_speedx_min = 0.05
    ball_speedy_max = 0.3
    ball_speedy_min = 0.005
    bot_difficulty = 1
    number_of_balls = 1

    def __init__(
        self,
        name,
        left=0,
        top=0,
        width=320,
        height=320,
        buttons: list = None,
        number_of_balls: int = 1,
        player_score: int = 0,
    ):
        super().__init__(name)

        self.name = name
        self.left = left
        self.top = top
        self.width = width
        self.height = height
        self.bottom = top + height
        self.right = left + width
        self.number_of_balls = number_of_balls
        self.player_score = player_score

        self.font = font.SysFont("arial", 50)
        self.small_font = font.SysFont("arial", 25)

        self.player_paddle = BasePaddle(
            "player_paddle", self.left + 20, self.height / 2
        )

        self.cpu_paddle = BasePaddle(
            "cpu_paddle", self.left + self.width - 20, self.height / 2
        )
        self.list_of_balls: list[BaseBall] = []
        # self.ball_dict: dict[str, BaseBall] = []
        for num in range(self.number_of_balls):
            self.list_of_balls.append(
                BaseBall(
                    f"ball_{num}", self.left + self.width / 2, self.top + self.width / 2
                )
            )

        self.paused_text = self.font.render(
            f"PAUSED",
            True,
            COLOUR_WHITE,
        )
        self.paused_text_rect = self.paused_text.get_rect(
            center=(self.left + self.width / 2, self.top + self.height / 2 - 50)
        )

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

    # def __del__(self):
    #     try:
    #         self.on_end()
    #     except:
    #         pass

    def on_start(self) -> bool:
        self.showing = True
        self.paused = False

        self.player_paddle.set_position(
            self.top + (self.height - self.player_paddle.height) / 2
        )

        self.cpu_paddle.set_position(
            self.top + (self.height - self.cpu_paddle.height) / 2
        )
        # self.cpu_paddle.set_movement(random.choice([-1, 1]))

        self.reset_balls()

        self.player_score = 0
        self.cpu_score = 0

        return True

    def reset_balls(self):
        for ball in self.list_of_balls:
            ball.set_position(
                self.top + (self.height - ball.height) / 2,
                self.left + (self.width - ball.width) / 2,
            )

            up = random.choice([-1, 1])
            left = random.choice([-1, 1])
            ball.set_movement(up, left)

            ball.speedx = random.uniform(self.ball_speedx_min, self.ball_speedx_max)
            ball.speedy = random.uniform(self.ball_speedy_min, self.ball_speedy_max)
        print("balls reset")

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

    def render(self, screen: Surface, mouse_pos=None):
        if self.showing:
            self.player_paddle.draw_paddle(screen)
            self.cpu_paddle.draw_paddle(screen)
            for ball in self.list_of_balls:
                ball.draw_ball(screen)

            if not self.paused:
                self.cpu_paddle.update_position(0.01 * self.bot_difficulty)

                self.player_paddle.update_position(0.1)

                if self.cpu_paddle.centery > self.list_of_balls[0].centery:
                    if self.cpu_paddle.top >= self.top:
                        self.cpu_paddle.set_movement(-1)
                    else:
                        self.cpu_paddle.set_movement(0)

                elif self.cpu_paddle.centery < self.list_of_balls[0].centery:
                    if self.cpu_paddle.bottom <= self.bottom:
                        self.cpu_paddle.set_movement(1)
                    else:
                        self.cpu_paddle.set_movement(0)

                for ball in self.list_of_balls:

                    if ball.top <= self.top or ball.bottom >= self.bottom:
                        ball.set_movement(ball.moving_up * -1, ball.moving_left)

                    elif (
                        self.player_paddle.paddle_box.colliderect(ball.ball_box)
                        and ball.moving_left == -1
                    ) or (
                        self.cpu_paddle.paddle_box.colliderect(ball.ball_box)
                        and ball.moving_left == 1
                    ):
                        ball.set_movement(ball.moving_up, ball.moving_left * -1)
                        ball.speedx = ball.speedx + 0.01

                    elif ball.left <= self.left:
                        self.cpu_score = self.cpu_score + 1
                        self.reset_balls()
                        print(self.cpu_score)

                    elif ball.right >= self.right:
                        self.player_score = self.player_score + 1
                        self.reset_balls()
                        print(self.player_score)

                    ball.update_position()

            else:
                screen.blit(self.paused_text, self.paused_text_rect)

                # button

                self.pause_button.is_hovering(mouse_pos)
                self.pause_button.draw_button(screen, 8)

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
