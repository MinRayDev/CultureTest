import enum


class Facing(enum.IntEnum):
    """Class that represents the direction the player is facing."""
    NORTH = 0
    EAST = 1
    SOUTH = 2
    WEST = 3

    def __str__(self):
        """Returns the string representation of the direction.

            This representation is used for the player's sprite.

        """
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
        """Returns the next direction in clockwise order.

            :return: The next direction in clockwise order.
            :rtype: Facing

        """
        if self.value == 3:
            return Facing(0)
        else:
            return Facing((self.value + 1))
