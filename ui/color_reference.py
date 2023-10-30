import enum


class ColorReference(enum.Enum):
    collision = (255, 0, 0, 255)
    forward = (0, 255, 255, 255)
    backward = (0, 255, 0, 255)
    yforward = (255, 255, 0, 255)
    question = (125, 125, 125, 255)
    answer1 = (125, 0, 0, 255)
    answer2 = (0, 125, 0, 255)
    answer3 = (0, 0, 125, 255)

    collisions = (
        collision,
        question,
        answer1,
        answer2,
        answer3
    )

    interactions = (
        question,
        answer1,
        answer2,
        answer3
    )

    def get_value(self):
        return self.value
