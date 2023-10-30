import json
import os
import random
from typing import Optional

from core.question import Question, QuestionEncoder
from entities.entity import Entity
from utils.files import get_map


class Game:
    def __init__(self):
        from entities.screen import Screen
        from ui.hud import HUD
        self.screens = [Screen(get_map(i)) for i in range(4)]
        self.screen = self.screens[0]
        self.entities: list[Entity] = []
        self.scroll: list[int] = [0, 0]
        self.questions: list[Question] = self.load_questions()
        self.question: Optional[Question] = None
        self.good_answers: int = 0
        self.hud = HUD()
        self.menu = None
        self.run = True

    def next_screen(self) -> None:
        if self.screen.index + 1 < 2:
            self.screen = self.screens[self.screen.index + 1]
        elif self.screen.index + 1 == 2 or self.screen.index + 1 == 3:
            self.question = self.get_question()
            if self.question is None:
                self.screen = self.screens[3]
                return
            self.screen = self.screens[2]
            self.screen.reset()
            self.screen.add(f"addon{self.question.correct}", "collisions")

    def previous_screen(self) -> None:
        if self.screen.index > 0:
            self.screen = self.screens[self.screen.index - 1]

    def create_question(self, text: str, answers: dict[str, bool]) -> 'Question':
        question: Question = Question(text, answers)
        self.questions.append(question)
        json.dump(self.questions, open(os.path.join(os.getcwd(), "resources", "questions.json"), "w"),
                  cls=QuestionEncoder)
        return question

    @classmethod
    def load_questions(cls) -> list['Question']:
        questions: list['Question'] = []
        for question in json.load(open(os.path.join(os.getcwd(), "resources", "questions.json"), "r")):
            questions.append(Question(**question))
        return questions

    def get_question(self) -> Optional['Question']:
        if len(self.questions) == 0:
            raise Exception("No questions loaded")
        if all(question.past for question in self.questions):
            return None
        while True:
            question: 'Question' = random.choice(self.questions)
            if not question.past:
                return question

    def game_over(self):
        self.run = False
