from pathlib import Path
from typing import TYPE_CHECKING, Optional

import pygame
from pygame import Surface
from pygame.event import Event

from core.sound import Sound
from ui.element.impl.choice import Choice
from ui.element.impl.choice_text import ChoiceText
from ui.element.impl.fairy import Fairy
from ui.element.impl.outlined_text import OutlinedText
from ui.menu.menu import Menu
from utils.files import get_menus
from utils.sprites import get_center

if TYPE_CHECKING:
    from pygame.mixer import Channel


class AddMenu(Menu):
    ratio: float
    menu_title: OutlinedText
    choices: list[Choice]
    results: list[Choice]
    choices_draw: list[Choice]
    fairy: Fairy
    default_y: int
    question: ChoiceText
    question_done: bool
    answers: tuple[ChoiceText, ChoiceText, ChoiceText]
    good: int

    def __init__(self, parent: Optional['Menu']):
        from references import client
        self.ratio = client.surface.get_height()/224
        super().__init__(parent, Path(get_menus(), "question_manage"), ratio=self.ratio)
        self.menu_title = OutlinedText("ECRAN D'AJOUTS DE QUESTIONS", int(112*self.ratio), int(38*self.ratio), (255, 255, 255), (0, 0, 200), int(15*self.ratio))
        y: int = int(122*self.ratio)
        self.default_y = y
        self.choices = []
        x: int = int(130*self.ratio)
        height: int = int(15*self.ratio)
        self.question = ChoiceText("Question", int(104*self.ratio), int(90*self.ratio), height)
        self.question.outline_color = (0, 220, 0)
        self.choices.append(self.question)
        self.answers = (
            ChoiceText("Reponse 1", x, y, height),
            ChoiceText("Reponse 2", x, y + int(19*self.ratio), height),
            ChoiceText("Reponse 3", x, y + int(37*self.ratio), height)
        )
        self.choices += self.answers
        self.results = list(self.answers)
        self.results.append(Choice("Ajouter", x, y + int(56*self.ratio), height, action=lambda: self.add()))
        self.choices.append(self.results[-1])
        self.fairy = Fairy(int(100*self.ratio), self.answers[0].rectangle.y, limit=len(self.answers))
        self.good = -1
        self.question_done = False

    def draw(self, surface: Surface) -> None:
        self.menu_title.draw(surface)
        if self.question_done:
            self.fairy.draw(surface)
        for choice in self.choices:
            choice.draw(surface)
        surface.blit(self.sprites["foreground"], get_center(self.sprites["foreground"]))

    def activity(self, events: dict[int, list[Event]]) -> None:
        if self.question_done:
            if pygame.K_DOWN in events[pygame.KEYDOWN] and self.fairy.position < self.fairy.limit:
                self.fairy.position += 1
                self.fairy.move(self.results[self.fairy.position].rectangle.y)

            elif pygame.K_UP in events[pygame.KEYDOWN] and self.fairy.position > 0:
                self.fairy.position -= 1
                self.fairy.move(self.results[self.fairy.position].rectangle.y)

            elif pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
                Sound.turn.play()
                if self.fairy.position < 3:
                    self.good = self.fairy.position
                    answer: ChoiceText
                    for i, answer in enumerate(self.answers):
                        if i == self.good:
                            answer.outline_color = (0, 220, 0)
                        else:
                            answer.outline_color = (0, 0, 220)
            elif pygame.K_ESCAPE in events[pygame.KEYDOWN]:
                Sound.turn.play()
                self.question_done = False
                self.question.outline_color = (0, 220, 0)
        elif pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
            Sound.turn.play()
            self.question_done = True
            self.question.outline_color = (0, 0, 220)
        elif pygame.K_ESCAPE in events[pygame.KEYDOWN]:
            self.back()
        if self.question_done:
            if isinstance(self.results[self.fairy.position], ChoiceText):
                self.results[self.fairy.position].activity(events)
            else:
                if pygame.K_RETURN in events[pygame.KEYDOWN] or pygame.K_KP_ENTER in events[pygame.KEYDOWN]:
                    Sound.turn.play()
                    self.results[self.fairy.position].activity(events)
        else:
            self.choices[0].activity(events)
        self.fairy.activity(events)

    def play(self, channel: 'Channel', loops: int = -1):
        super().play(channel, loops=loops)

    def back(self):
        from references import game
        Sound.back.play()
        self.parent.reload()
        game.menu = self.parent

    def add(self):
        from references import game
        if self.question.content and self.answers[0].content and self.answers[1].content and self.answers[2].content and self.good != -1 and self.answers[0].content != self.answers[1].content and self.answers[0].content != self.answers[2].content and self.answers[1].content != self.answers[2].content:
            answers: dict[str, bool] = {}
            for i, answer in enumerate(self.answers):
                if i == self.good:
                    answers[answer.content] = True
                else:
                    answers[answer.content] = False
            game.add_question(self.question.content, answers)
            self.back()
        else:
            Sound.error.play()
