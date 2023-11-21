from typing import Optional, Literal

import pygame
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.element.impl.settings_menu.choice_bar import ChoiceBar
from ui.element.impl.settings_menu.choice_box import ChoiceBox
from ui.menu.menu import Menu
from ui.menu.menu_template import MenuTemplate


class SettingsMenu(MenuTemplate):
    def __init__(self, parent: Optional['Menu']):
        from references import game
        super().__init__(parent, None, "ECRAN DES PARAMETRES")
        height: int = int(15*self.ratio)
        y_increment: int = int(33*self.ratio)
        self.choices.append(ChoiceBar("1. General Volume", self.default_x, self.default_y, height, self.ratio, lambda value: self.edit_volume("general", value), int(game.general_volume*100)))
        self.default_y += y_increment

        self.choices.append(ChoiceBar("2. Music Volume", self.default_x, self.default_y, height, self.ratio, lambda value: self.edit_volume("music", value), int(game.music_volume*100)))
        self.default_y += y_increment

        self.choices.append(ChoiceBox("3. Collisons Sound", self.default_x, self.default_y, height, lambda value: game.set_collision_sound(value), game.collision_sound))
        self.default_y += y_increment

        self.choices.append(Choice("4. Back", self.default_x, self.default_y, height, self.back))
        self.setup_fairy()

    def activity(self, events: dict[int, list[Event]]) -> None:
        super().activity(events)
        if pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_SPACE in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
            if self.choices[self.fairy.position].action is not None or isinstance(self.choices[self.fairy.position], ChoiceBox):
                if isinstance(self.choices[self.fairy.position], ChoiceBox):
                    Sound.turn.play()
                self.choices[self.fairy.position].activity(events)

        elif pygame.K_ESCAPE in events[pygame.KEYDOWN]:
            self.back()
            return

        if pygame.key.get_pressed()[pygame.K_RIGHT]:
            current_choice: Choice = self.choices[self.fairy.position]
            if isinstance(current_choice, ChoiceBar):
                current_choice.value += 1

        elif pygame.key.get_pressed()[pygame.K_LEFT]:
            current_choice: Choice = self.choices[self.fairy.position]
            if isinstance(current_choice, ChoiceBar):
                current_choice.value -= 1

    @classmethod
    def edit_volume(cls, volume_type: Literal["general", "music"], value: int):
        from references import game
        game.change_volume(volume_type, value / 100)
