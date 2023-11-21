from pathlib import Path


def get_resources() -> Path:
    return Path(Path.cwd(), "resources")


def get_map_directory() -> Path:
    return Path(get_resources(), "map")


def get_map(index: int) -> Path:
    return Path(get_map_directory(), str(index))


def get_question() -> Path:
    return Path(get_resources(), "questions.json")


def get_sounds() -> Path:
    return Path(get_resources(), "sounds")


def get_sound(name: str, ext: str = "wav") -> Path:
    return Path(get_sounds(), name + "." + ext)


def get_menus() -> Path:
    return Path(get_resources(), "menus")


def get_fonts() -> Path:
    return Path(get_resources(), "fonts")
