from pathlib import Path
from typing import Optional, TYPE_CHECKING

from pygame import Surface
from pygame.event import Event
from utils.sprites import load, resize

if TYPE_CHECKING:
    from core.sound import Sound
    from pygame.mixer import Channel


class Menu:
    parent: Optional['Menu']
    sprites: dict[str, Surface]
    music: Optional[str]
    sounds: dict[str, 'Sound']

    def __init__(self, parent: Optional['Menu'], resources_path: Optional[Path], ratio: float = 4):
        from core.sound import Sound
        self.parent = parent
        self.sprites = {}
        self.sounds = {}
        self.music = None
        if resources_path:
            self.sounds = Sound.load_sounds(resources_path)
            if len(self.sounds):
                self.music = list(self.sounds.keys())[0]

            sprites: dict[str, Surface] = load(resources_path)
            for key, value in sprites.items():
                self.sprites[key] = resize(value, ratio)

    def draw(self, surface: Surface) -> None:
        ...

    def activity(self, events: dict[int, list[Event]]) -> None:
        ...

    def play(self, channel: 'Channel', loops: int = 0):
        channel.stop()
        channel.play(self.sounds[self.music], loops=loops)

    def reload(self):
        ...
