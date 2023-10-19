import os


def get_map_directory():
    return os.path.join(os.path.dirname(os.path.dirname(__file__)), "resources", "map")

def get_map(index: int):
    return os.path.join(get_map_directory(), str(index))