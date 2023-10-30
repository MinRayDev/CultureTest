import json
import os
import random
from typing import Optional


class QuestionEncoder(json.JSONEncoder):
    def default(self, o: 'Question') -> dict[str, str | dict[str, bool]]:
        return o.to_json()


class Question:
    text: str
    answers: dict[str, bool]
    correct: int
    past: bool

    def __init__(self, text: str, answers: dict[str, bool]):
        self.text = text
        self.answers = answers
        self.correct = random.randint(1, len(answers))
        self.past = False

    def to_json(self) -> dict[str, str | dict[str, bool]]:
        return {"text": self.text, "answers": self.answers}
