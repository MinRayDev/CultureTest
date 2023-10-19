from typing import Optional

from core.client import Client
from core.game import Game
from entities.player import Player

player: Optional[Player] = None
client: Client = Client()
game: Game = Game()
