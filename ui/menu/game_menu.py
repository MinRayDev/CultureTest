from pathlib import Path
from typing import Optional

from ui.menu.menu import Menu


class GameMenu(Menu):
    def __init__(self, resources_path: Optional[Path] = None):
        super().__init__(None, resources_path)
