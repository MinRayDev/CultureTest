import enum


class Facing(enum.IntEnum):
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __str__(self):
        match self:
            case Facing.NORTH:
                return "top"
            case Facing.EAST:
                return "right"
            case Facing.SOUTH:
                return "bottom"
            case Facing.WEST:
                return "left"

    def next(self) -> 'Facing':
        if self.value == 3:
            return Facing(0)
        else:
            return Facing((self.value + 1))
