import os

from pygame import Surface

from entities.entity import Entity


class Screen(Entity):
    def __init__(self, background_location: str):
        super().__init__("Background", background_location, -1500, -732)
        self.index = int(os.path.basename(background_location))
        self.background = self.sprites["background"]
        self.foreground = self.sprites["foreground"]
        self.collisions = self.sprites["collisions"]
        self.background = self.sprites["collisions"]

        self.forward_tp = []
        for x in range(self.background.get_width()):
            for y in range(self.background.get_height()):
                if self.collisions.get_at((x, y)) == (0, 0, 255):
                    self.forward_tp.append((x, y))

    def draw(self, screen: Surface):
        pass