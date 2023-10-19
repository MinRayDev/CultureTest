from entities.entity import Entity
from entities.screen import Screen
from utils.files import get_map_directory, get_map


class Game:
    def __init__(self):
        from entities.screen import Screen
        self.screen = Screen(get_map(1))
        self.entities: list[Entity] = []
        self.scroll: list[int] = [0, 0]

    def set_screen(self, screen: 'Screen'):
        self.screen = screen

    def next_screen(self):
        self.screen = Screen(get_map(self.screen.index + 1))
