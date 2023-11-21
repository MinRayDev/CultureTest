import json
import random
from typing import Optional

from utils.files import get_question


class QuestionEncoder(json.JSONEncoder):
    """Encoder for Question class to json."""
    def default(self, o: 'Question') -> dict[str, str | dict[str, bool]]:
        """Encode Question class to json.

            :param o: question to encode.
            :type o: Question

            :return: encoded question.
            :rtype: dict[str, str | dict[str, bool]]

        """
        return o.to_json()


class Question:
    """Question class.

        :ivar text: question text.
        :type text: str
        :ivar answers: question answers.
        :type answers: dict[str, bool]
        :ivar correct: correct answer.
        :type correct: int
        :ivar past: if the question has already been asked.
        :type past: bool
        :ivar good_answer: good answer.
        :type good_answer: str
        :ivar bad_answers: bad answers.
        :type bad_answers: list[str]

    """
    text: str
    answers: dict[str, bool]
    correct: int
    past: bool
    good_answer: str
    bad_answers: list[str]

    def __init__(self, text: str, answers: dict[str, bool]):
        """Constructor of Question class.

            :param text: question text.
            :type text: str
            :param answers: question answers.
            :type answers: dict[str, bool]

        """
        self.text = text
        self.answers = answers
        self.correct = random.randint(1, len(answers))
        self.past = False

    def to_json(self) -> dict[str, str | dict[str, bool]]:
        """Encode Question class to json.

            :return: encoded question.
            :rtype: dict[str, str | dict[str, bool]]

        """
        return {"text": self.text, "answers": self.answers}

    @property
    def good_answer(self) -> str:
        """Get good answer."""
        return [key for key, value in self.answers.items() if value][0]

    @property
    def bad_answers(self) -> list[str]:
        """Get bad answers."""
        return [key for key, value in self.answers.items() if not value]


class QuestionManager:
    """Question manager class.

        :ivar questions: list of questions.
        :type questions: list[Question]
        :ivar question: current question.
        :type question: Optional[Question]

    """
    questions: list[Question]
    question: Optional[Question]

    def __init__(self):
        """Constructor of QuestionManager class."""
        self.questions = self.load_questions()
        self.question = None

    def add_question(self, text: str, answers: dict[str, bool]) -> 'Question':
        """Add question to the list.

            :param text: question text.
            :type text: str
            :param answers: question answers.
            :type answers: dict[str, bool]

        """
        question: Question = Question(text, answers)
        self.questions.append(question)
        json.dump(self.questions, open(get_question(), "w"), cls=QuestionEncoder)
        return question

    @classmethod
    def load_questions(cls) -> list['Question']:
        """Load questions from json file.

            :return: list of questions.
            :rtype: list[Question]

        """
        questions: list['Question'] = []
        for question in json.load(open(get_question(), "r")):
            questions.append(Question(**question))
        return questions

    def save_questions(self) -> None:
        """Save questions to json file."""
        json.dump(self.questions, open(get_question(), "w"), cls=QuestionEncoder)

    def get_question(self) -> Optional['Question']:
        """Get a random question.

            :return: a question.
            :rtype: Optional[Question]

        """
        if len(self.questions) == 0:
            raise Exception("No questions loaded")
        if all(question.past for question in self.questions):
            return None
        while True:
            question: 'Question' = random.choice(self.questions)
            if not question.past:
                return question
