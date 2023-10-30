from pygame import Surface

import references
from ui.element.impl.text import Text
from utils.sprites import load, resize, draw_with_scroll


class HUD:
    """Class 'HUD' is the HUD of the game."""

    def __init__(self):
        """Constructor of the class 'HUD'."""
        self.x = 0
        self.y = 0
        client_surface: Surface = references.client.surface
        self.width = client_surface.get_width()
        self.height = client_surface.get_height()
        self.elems = []
        self.sprites = {}
        sprites = load("resources/hud")
        self.forest_mask = sprites["forest_mask"]
        for px in range(self.forest_mask.get_width()):
            for py in range(self.forest_mask.get_height()):
                if self.forest_mask.get_at((px, py)) == (0, 0, 0, 255):
                    i: int = 30
                    self.forest_mask.set_at((px, py), (i, i, i, 120))
                else:
                    self.forest_mask.set_at((px, py), (0, 0, 0, 0))
        for key, value in sprites.items():
            self.sprites[key] = resize(value, 4)

    def draw(self, surface: Surface) -> None:
        """Draws the HUD on the screen.

            :param surface: The surface on which the HUD is drawn.
            :type surface: Surface.
        """
        hearts = []
        match references.player.life:
            case 3:
                hearts.append(self.sprites["heart"])
                hearts.append(self.sprites["heart"])
                hearts.append(self.sprites["heart"])
            case 2:
                hearts.append(self.sprites["heart"])
                hearts.append(self.sprites["heart"])
                hearts.append(self.sprites["heart_slot"])
            case 1:
                hearts.append(self.sprites["heart"])
                hearts.append(self.sprites["heart_slot"])
                hearts.append(self.sprites["heart_slot"])

        for i, heart in enumerate(hearts):
            surface.blit(heart, (self.width - self.width//30 - (i * self.width//30), self.height//20))
        Text("Correct: " + str(references.game.good_answers), self.width-self.width//15, self.height//10, (0, 255, 0)).draw(surface)
        Text("Fps: " + str(references.client.clock.get_fps()), self.width-self.width//15, self.height//80, (0, 255, 0)).draw(surface)
        if references.player.ghost:
            Text("Ghost Mod", self.width - self.width // 8, self.height // 7, (0, 255, 255)).draw(surface)
