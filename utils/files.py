from pathlib import Path


def get_resources() -> Path:
    """Returns the resources directory path.

        :return: The resources directory path.
        :rtype: Path.

    """
    return Path(Path.cwd(), "resources")


def get_map_directory() -> Path:
    """Returns the map directory path.

        :return: The map directory path.
        :rtype: Path.

    """
    return Path(get_resources(), "map")


def get_map(index: int) -> Path:
    """Returns the map file path.

        :param index: The index of the map.
        :type index: int.

    """
    return Path(get_map_directory(), str(index))


def get_question() -> Path:
    """Returns the question file path.

        :return: The question file path.
        :rtype: Path.

    """
    return Path(get_resources(), "questions.json")


def get_sounds() -> Path:
    """Returns the sounds directory path.

        :return: The sounds directory path.
        :rtype: Path.

    """
    return Path(get_resources(), "sounds")


def get_sound(name: str, ext: str = "wav") -> Path:
    """Returns the sound file path.

        :param name: The name of the sound.
        :type name: str.
        :param ext: The extension of the sound.
        :type ext: str.

    """
    return Path(get_sounds(), name + "." + ext)


def get_menus() -> Path:
    """Returns the menus directory path.

        :return: The menus directory path.
        :rtype: Path.

    """
    return Path(get_resources(), "menus")


def get_fonts() -> Path:
    """Returns the fonts directory path.

        :return: The fonts directory path.
        :rtype: Path.

    """
    return Path(get_resources(), "fonts")
