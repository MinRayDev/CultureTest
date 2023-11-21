from pathlib import Path
from typing import Optional

import pygame
from pygame import Surface
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.menu.menu import Menu
from ui.menu.menu_template import MenuTemplate
from utils.files import get_menus
from utils.sprites import get_center


class QuestionMenu(MenuTemplate):
    choices_draw: list[Choice]

    def __init__(self, parent: Optional['Menu']):
        super().__init__(parent, Path(get_menus(), "question_list"), "ECRAN DES QUESTIONS")
        self.choices = [Choice("Ajouter", self.default_x, self.default_y, int(15*self.ratio), action=lambda: self.add())]
        self.choices[0].outline_color = (0, 150, 0)
        y: int = self.default_y
        y += int(33*self.ratio)
        from references import game
        for question in game.questions:
            self.choices.append(Choice(question.text, self.default_x, y, int(15*self.ratio)))
            y += int(33*self.ratio)
        self.choices_draw = self.choices[:4]
        self.setup_fairy()
        self.reload_sprites()

    def draw(self, surface: Surface) -> None:
        self.title.draw(surface)
        for choice in self.choices_draw:
            choice.draw(surface)
        self.fairy.draw(surface)
        surface.blit(self.sprites["foreground"], get_center(self.sprites["foreground"]))

    def activity(self, events: dict[int, list[Event]]) -> None:
        if pygame.K_DOWN in events[pygame.KEYDOWN] and self.fairy.position < self.fairy.limit:
            self.fairy.position += 1
            if self.fairy.relative_position < 3:
                self.fairy.relative_position += 1
            else:
                self.choices_draw = self.choices[self.fairy.position - 3:self.fairy.position+1]
                y = self.default_y
                for choice in self.choices_draw:
                    choice.y = y
                    y += int(33*self.ratio)
            self.fairy.move(self.fairy.relative_position * int(33*self.ratio) + self.default_y)

        elif pygame.K_UP in events[pygame.KEYDOWN] and self.fairy.position > 0:
            self.fairy.position -= 1
            if self.fairy.relative_position > 0:
                self.fairy.relative_position -= 1
            else:
                self.choices_draw = self.choices[self.fairy.position:self.fairy.position + 4]
                y = self.default_y
                for choice in self.choices_draw:
                    choice.y = y
                    y += int(33*self.ratio)
            self.fairy.move(self.choices[self.fairy.position].rectangle.y)

        elif pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_SPACE in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
            Sound.turn.play()
            if self.choices[self.fairy.position].outline_color == (220, 0, 0):
                from references import game
                game.questions.pop(self.fairy.position - 1)
                self.reload()
                return
            if self.choices[self.fairy.position].action is not None:
                self.choices[self.fairy.position].activity(events)
            else:
                self.edit(self.fairy.position-1)
        elif pygame.K_DELETE in events[pygame.KEYDOWN] or pygame.K_BACKSPACE in events[pygame.KEYDOWN]:
            Sound.delete.play()
            for i, choice in enumerate(self.choices):
                if choice.outline_color == (220, 0, 0):
                    choice.outline_color = (0, 0, 220)
            self.choices[self.fairy.position].outline_color = (220, 0, 0)
        elif pygame.K_ESCAPE in events[pygame.KEYDOWN]:
            self.back()
        self.fairy.activity(events)

    @classmethod
    def change_menu(cls, menu: Optional['Menu']) -> None:
        from references import game
        game.menu = menu

    def back(self):
        Sound.back.play()
        self.change_menu(self.parent)

    def add(self):
        from ui.menu.impl.add_menu import AddMenu
        self.change_menu(AddMenu(self))

    def edit(self, question_index: int):
        from ui.menu.impl.edit_menu import EditMenu
        self.change_menu(EditMenu(self, question_index))

    def reload(self) -> None:
        self.fairy.position = 0
        self.fairy.relative_position = 0
        temp = self.choices[0]
        self.choices = [temp]
        y: int = self.default_y + int(33*self.ratio)
        from references import game
        for question in game.questions:
            self.choices.append(Choice(question.text, int(130*self.ratio), y, int(15*self.ratio)))
            y += int(33*self.ratio)
        self.choices_draw = self.choices[:4]
        self.setup_fairy()
