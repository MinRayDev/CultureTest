import json
import os
import random
from typing import Optional

questions: list['Question'] = []


class QuestionEncoder(json.JSONEncoder):
    def default(self, o: 'Question') -> dict[str, str | dict[str, bool]]:
        return o.to_json()


class Question:
    text: str
    answers: dict[str, bool]
    past: bool

    def __init__(self, text: str, answers: dict[str, bool]):
        self.text = text
        self.answers = answers
        self.past = False

    def to_json(self) -> dict[str, str | dict[str, bool]]:
        return {"text": self.text, "answers": self.answers}

    @staticmethod
    def create_question(text: str, answers: dict[str, bool]) -> 'Question':
        question: Question = Question(text, answers)
        questions.append(question)
        json.dump(questions, open(os.path.join(os.getcwd(), "resources", "questions.json"), "w"), cls=QuestionEncoder)
        return question

    @staticmethod
    def load_questions() -> list['Question']:
        _questions: list['Question'] = []
        for question in json.load(open(os.path.join(os.getcwd(), "resources", "questions.json"), "r")):
            _questions.append(Question(**question))
        return _questions

    @staticmethod
    def get_question() -> Optional['Question']:
        if len(questions) == 0:
            raise Exception("No questions loaded")
        if all(question.past for question in questions):
            return None
        while True:
            question: 'Question' = random.choice(questions)
            if not question.past:
                return question
