import sys
from pathlib import Path
from time import time
from typing import TYPE_CHECKING

import pygame
from pygame import Surface
from pygame.event import Event

from ui.element.impl.fairy import Fairy
from ui.element.impl.game_over.letter import Letter
from ui.element.impl.outlined_text import OutlinedText
from ui.menu.menu import Menu
from utils.files import get_menus
from utils.time_util import has_elapsed

if TYPE_CHECKING:
    from pygame.mixer import Channel
    from entities.player_entity import PlayerEntity


class GameOver(Menu):
    player: 'PlayerEntity'
    frame: int
    played: bool
    start_time: float
    fell: bool
    background_color: list[int, int, int]
    letters: list[Letter]
    regrouped_frame: int
    fairy: Fairy
    quit_text: OutlinedText
    already_played: bool
    music_channel: 'Channel'

    def __init__(self):
        super().__init__(None, Path(get_menus(), "default"))
        from references import game, client
        self.player = game.player
        self.frame = 0
        self.played = False
        self.start_time = time()
        self.fell = False
        self.background_color = [255, 0, 0]
        self.letters = []
        self.regrouped_frame = 0
        self.already_played = False
        self.music_channel = game.music_channel
        self.sounds[self.music].set_volume(game.music_volume / 1.25)
        title: str = "GAME OVER"
        sw, sh = client.surface.get_size()
        swc: int = sw // 2
        shc: int = sh // 2
        i: int = -4
        space: int = sw // 20
        y: int = int(sh / 2.75)
        for char in title:
            if char != " ":
                letter: Letter = Letter(char, sw, y)
                if i < 0:
                    x = swc - space*abs(i) - letter.width
                else:
                    x = swc + space*i
                letter.limit_x = x
                self.letters.append(letter)
            else:
                i = 0
            i += 1
        final_x: int = swc - sum([letter.width for letter in self.letters[:4]]) - space // 2 - 4*10
        for i, letter in enumerate(self.letters):
            if i == 4:
                final_x = swc + space // 2
            letter.final_x = final_x
            final_x += letter.width + 10
        self.fairy = Fairy(int(sw / 2.5), shc + sh // 10)
        self.fairy.y -= self.fairy.height // 2
        self.quit_text = OutlinedText("Quit Game", 0, 0, (255, 255, 255), (0, 0, 200), 60)
        self.quit_text.rectangle.x = swc - self.quit_text.width // 2 + self.quit_text.width // 15
        self.quit_text.rectangle.y = shc + sh // 10 - self.quit_text.height // 2

    def draw(self, surface: Surface) -> None:
        surface.fill(self.background_color)
        self.player.draw(surface)
        if self.frame > 75:
            for letter in self.letters:
                letter.draw(surface)
        if self.letters[-1].color[2] == 0:
            self.fairy.draw(surface)
            self.quit_text.draw(surface)

    def activity(self, events: dict[int, list[Event]]) -> None:
        if not self.fell:
            if not self.played:
                from core.sound import Sound
                self.played = True
                Sound.dies.play()
            if self.frame > 7:
                self.frame = 0
                self.player.facing = self.player.facing.next()
                self.player.stop()
                if has_elapsed(self.start_time, 0.9):
                    self.fell = True
                    self.player.current_key = "fall_0"
                    self.player.current_sprite = self.player.sprites[self.player.current_key]
                    return
        else:
            if self.frame > 10 and self.player.current_key == "fall_0":
                self.player.current_key = f"fall_1"
                self.player.current_sprite = self.player.sprites[self.player.current_key]
            if self.frame > 40 and self.background_color[0] > 0:
                if self.background_color[0] - 10 <= 0:
                    self.background_color[0] = 0
                else:
                    self.background_color[0] -= 10
            if self.frame > 80:
                for letter in self.letters:
                    if not letter.reached_limit:
                        if letter.x - 65 > letter.limit_x:
                            letter.x -= 65
                        else:
                            letter.x = letter.limit_x
                        break
            if not self.regrouped_frame and self.letters[-1].reached_limit:
                if all([letter.regrouped for letter in self.letters]):
                    self.regrouped_frame = self.frame
                else:
                    self.letters[-1].regrouping = True
                    for letter in self.letters:
                        if self.letters[-1].x <= letter.x:
                            letter.regrouping = True
                        if letter.regrouping:
                            if letter == self.letters[-1]:
                                if letter.x - 30 > self.letters[0].limit_x:
                                    letter.x -= 30
                                else:
                                    letter.x = self.letters[0].limit_x
                                    letter.regrouped = True
                            else:
                                letter.x = self.letters[-1].x
                                if letter.x == self.letters[0].x:
                                    letter.regrouped = True
            if self.frame > self.regrouped_frame + 15 and self.regrouped_frame:
                if not self.already_played:
                    from core.sound import Sound
                    Sound.menu_slide.play()
                    self.already_played = True
                for letter in self.letters:
                    if not letter.is_finished:
                        if letter.x + 30 < letter.final_x:
                            letter.x += 30
                        else:
                            letter.x = letter.final_x
                    elif letter.color[2] > 0:
                        if letter.color[2] - 20 > 0:
                            letter.color = (255, letter.color[1]-20, letter.color[2]-20)
                        else:
                            letter.color = (255, 0, 0)
            if self.letters[-1].color[2] == 0:
                if not self.music_channel.get_busy():
                    self.play(self.music_channel)
                self.fairy.activity(events)
                if pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_SPACE in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
                    from references import game
                    game.run = False
                    sys.exit()
        self.frame += 1

    def play(self, channel: 'Channel', loops: int = -1):
        super().play(channel, loops=loops)
