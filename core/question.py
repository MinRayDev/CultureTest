import functools
import json
import os
import random
from typing import Optional

from utils.files import get_question


class QuestionEncoder(json.JSONEncoder):
    def default(self, o: 'Question') -> dict[str, str | dict[str, bool]]:
        return o.to_json()


class Question:
    text: str
    answers: dict[str, bool]
    correct: int
    past: bool
    good_answer: str
    bad_answers: list[str]

    def __init__(self, text: str, answers: dict[str, bool]):
        self.text = text
        self.answers = answers
        self.correct = random.randint(1, len(answers))
        self.past = False

    def to_json(self) -> dict[str, str | dict[str, bool]]:
        return {"text": self.text, "answers": self.answers}

    @property
    def good_answer(self):
        return [key for key, value in self.answers.items() if value][0]

    @property
    def bad_answers(self):
        return [key for key, value in self.answers.items() if not value]


class QuestionManager:
    questions: list[Question]
    question: Optional[Question]

    def __init__(self):
        self.questions = self.load_questions()
        self.question = None

    def add_question(self, text: str, answers: dict[str, bool]) -> 'Question':
        question: Question = Question(text, answers)
        self.questions.append(question)
        json.dump(self.questions, open(get_question(), "w"), cls=QuestionEncoder)
        return question

    @classmethod
    def load_questions(cls) -> list['Question']:
        questions: list['Question'] = []
        for question in json.load(open(get_question(), "r")):
            questions.append(Question(**question))
        return questions

    def save_questions(self) -> None:
        json.dump(self.questions, open(get_question(), "w"), cls=QuestionEncoder)

    def get_question(self) -> Optional['Question']:
        if len(self.questions) == 0:
            raise Exception("No questions loaded")
        if all(question.past for question in self.questions):
            return None
        while True:
            question: 'Question' = random.choice(self.questions)
            if not question.past:
                return question
