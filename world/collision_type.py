import enum


class CollisionType(enum.IntEnum):
    collision = 0
    forward = 1
    backward = 2
    bad_forward = 3
