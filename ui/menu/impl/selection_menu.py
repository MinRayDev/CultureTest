from typing import Optional

import pygame
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.menu.impl.question_menu import QuestionMenu
from ui.menu.impl.settings_menu import SettingsMenu
from ui.menu.menu import Menu
from ui.menu.menu_template import MenuTemplate


class SelectionMenu(MenuTemplate):
    def __init__(self):
        from references import game
        super().__init__(None, None, "ECRAN DE SELECTION")
        for name, action in (
                ("1. Start", lambda: self.change_menu(None)),
                ("2. Questions", lambda: self.change_menu(QuestionMenu(self))),
                ("3. Settings", lambda: self.change_menu(SettingsMenu(self))),
                ("4. Quit", lambda: game.quit())
        ):
            self.choices.append(Choice(name, self.default_x, self.default_y, int(15*self.ratio), action))
            self.default_y += int(33*self.ratio)
        self.setup_fairy()

    def activity(self, events: dict[int, list[Event]]) -> None:
        super().activity(events)
        if pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_SPACE in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
            Sound.turn.play()
            self.choices[self.fairy.position].activity(events)

    @classmethod
    def change_menu(cls, menu: Optional[Menu]) -> None:
        from references import game
        game.menu = menu
