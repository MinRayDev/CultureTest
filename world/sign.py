from typing import Literal

from core.question import Question
from references import game, client
from ui.menu.impl.text_box import TextBox


def read(read_type: Literal[0, 1, 2, 3, 4]) -> None:
    question: Question = game.question
    content: str
    match read_type:
        case 0:
            content = "Exemple: Prenez le premier tronc d'arbre a gauche." if question is None else question.text
        case 4:
            content = f"Bravo, vous avez fini le jeu avec un score de {game.good_answers} sur {len(game.questions)}."
            game.menu = TextBox(content, client.surface, True)
            return
        case _:
            answers: list[str] = question.bad_answers
            if read_type == question.correct:
                content = question.good_answer
            else:
                answer_index: int = 0
                match question.correct:
                    case 1:
                        answer_index = read_type - 2
                    case 2:
                        if read_type == 1:
                            answer_index = 0
                        else:
                            answer_index = 1
                    case 3:
                        answer_index = 1 if read_type > 1 else 0
                content = answers[answer_index]
    game.menu = TextBox(content, client.surface, False)
