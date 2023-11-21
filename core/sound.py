import enum
import os
from pathlib import Path

import pygame

from utils.files import get_sound


class Sound(enum.Enum):
    message = pygame.mixer.Sound(get_sound("message"))
    message_finish = pygame.mixer.Sound(get_sound("message_finish"))
    dies = pygame.mixer.Sound(get_sound("dies"))
    hurt = pygame.mixer.Sound(get_sound("hurt"))
    bounce = pygame.mixer.Sound(get_sound("bounce"))
    screen_switch = pygame.mixer.Sound(get_sound("screen_switch"))
    secret = pygame.mixer.Sound(get_sound("secret"))
    item_get = pygame.mixer.Sound(get_sound("item_get"))
    turn = pygame.mixer.Sound(get_sound("turn"))
    delete = pygame.mixer.Sound(get_sound("delete"))
    back = pygame.mixer.Sound(get_sound("back"))
    error = pygame.mixer.Sound(get_sound("error"))
    menu_slide = pygame.mixer.Sound(get_sound("menu_slide", ext="mp3"))

    def get(self):
        return self.value

    def play(self):
        pygame.mixer.Sound.play(self.value)

    @staticmethod
    def stop():
        pygame.mixer.stop()

    def get_volume(self) -> float:
        return self.value.get_volume()

    def set_volume(self, volume: float):
        self.value.set_volume(volume)

    @staticmethod
    def load_sounds(path: Path) -> dict[str, pygame.mixer.Sound]:
        sounds: dict[str, pygame.mixer.Sound] = {}
        for file in os.listdir(path):
            if file.endswith(".wav") or file.endswith(".mp3"):
                sounds[file[:-4]] = pygame.mixer.Sound(Path(path, file))
        return sounds
