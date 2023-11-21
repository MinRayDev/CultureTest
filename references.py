from core.client import Client
from core.game import Game
from ui.menu.impl.over_transition import load_rads

client: Client = Client()
game: Game = Game()
load_rads(client.surface.get_width(), client.surface.get_height())