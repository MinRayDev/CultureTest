from typing import Optional, TYPE_CHECKING, Literal

import pygame
from pygame.mixer import Channel, Sound

from core.question import QuestionManager
from entities.entity import Entity
from ui.menu.game_menu import GameMenu
from ui.menu.impl.over_transition import GameOverTransition
from utils.event_transformer import convert
from utils.files import get_map
from ui.menu.menu import Menu

if TYPE_CHECKING:
    from entities.player_entity import PlayerEntity
    from entities.screen import Screen
    from ui.hud import HUD


class Game(QuestionManager):
    __player: Optional['PlayerEntity']
    screens: list['Screen']
    screen: 'Screen'
    entities: list[Entity]
    scroll: list[int]
    good_answers: int
    hud: 'HUD'
    menu: Optional['Menu']
    run: bool
    general_volume: float
    music_volume: float
    collision_sound: bool
    music_channel: Channel
    can_play: bool

    def __init__(self):
        super().__init__()
        from entities.screen import Screen
        from ui.hud import HUD
        self.__player = None
        self.screens = [Screen(get_map(i)) for i in range(4)]
        self.screen = self.screens[0]
        self.entities = []
        self.scroll = [0, 0]
        self.good_answers = 0
        self.hud = HUD()
        self.menu = None
        self.run = True
        self.general_volume = 1
        self.music_volume = 0.3
        self.collision_sound = True
        self.music_channel = pygame.mixer.find_channel()
        self.music_channel.set_volume(self.music_volume)
        self.can_play = True

    def next_screen(self) -> None:
        if self.screen.index + 1 < 2:
            self.screen = self.screens[self.screen.index + 1]
        elif self.screen.index + 1 == 2 or self.screen.index + 1 == 3:
            self.question = self.get_question()
            if self.question is None:
                self.screen = self.screens[3]
                self.hud.forest_shadow = pygame.mask.from_surface(self.screen.background).overlap_mask(
                    pygame.mask.from_threshold(self.hud.forest_shadow, (30, 30, 30, 120), (1, 1, 1, 255)),
                    (
                        - self.hud.forest_shadow.get_width() // 4,
                        - self.hud.forest_shadow.get_height() // 4

                    )
                ).to_surface()
                i: int = 30
                pygame.transform.threshold(self.hud.forest_shadow, self.hud.forest_shadow, (0, 0, 0, 255), (1, 1, 1, 255), (i, i, i, 120))
                pygame.transform.threshold(self.hud.forest_shadow, self.hud.forest_shadow, (i, i, i, 120), (1, 1, 1, 255), (0, 0, 0, 0))
                return
            self.screen = self.screens[2]
            self.screen.reset()
            self.screen.add(f"addon{self.question.correct}", "collisions")

    def previous_screen(self) -> None:
        if self.screen.index > 0:
            self.screen = self.screens[self.screen.index - 1]

    def game_over(self) -> None:
        self.player.stop()
        self.can_play = False
        self.music_channel.stop()
        self.menu = GameOverTransition()

    def loop(self) -> None:
        from core.control import check_events
        import references
        music_name: str = ""
        while self.run:
            if self.can_play:
                if self.menu is None or isinstance(self.menu, GameMenu):
                    if (not self.music_channel.get_busy()) or (music_name != self.screen.current_sound):
                        self.music_channel.stop()
                        music: Sound = self.screen.sounds.get(self.screen.current_sound, None)
                        if music is not None:
                            self.music_channel.play(music, -1)
                            music_name = self.screen.current_sound
                elif isinstance(self.menu, Menu):
                    if (not self.music_channel.get_busy()) or (music_name != self.menu.music):
                        music: Sound = self.menu.sounds.get(self.menu.music, None)
                        if music is not None:
                            self.menu.play(self.music_channel)
                            music_name = self.menu.music
            if self.player.life <= 0 and self.menu is None:
                self.game_over()
            check_events(convert(events=pygame.event.get()))
            self.draw()
            pygame.display.update()
            references.client.clock.tick(60)

    def draw(self) -> None:
        import references
        from ui.menu.game_menu import GameMenu
        from utils.sprites import draw_with_scroll
        references.client.surface.fill((0, 0, 0))
        if isinstance(self.menu, Menu) and not isinstance(self.menu, GameMenu):
            self.menu.draw(references.client.surface)
            return
        draw_with_scroll(references.client.surface, self.screen.background, self.screen.x, self.screen.y)
        for entity in self.entities:
            entity.draw(references.client.surface)
        if self.screen.foreground is not None:
            draw_with_scroll(references.client.surface, self.screen.foreground, self.screen.x, self.screen.y)
        if 3 > self.screen.index > 0:
            draw_with_scroll(references.client.surface, self.hud.forest_shadow,
                             self.screen.x - self.hud.forest_shadow.get_width() // 4,
                             self.screen.y - self.hud.forest_shadow.get_height() // 4, 0.7)
        elif self.screen.index == 3:
            draw_with_scroll(references.client.surface, self.hud.forest_shadow,
                             self.screen.x,
                             self.screen.y, 1)
        self.hud.draw(references.client.surface)
        if self.menu is not None:
            self.menu.draw(references.client.surface)

    @property
    def player(self) -> 'PlayerEntity':
        if self.__player is None:
            raise ValueError("Player is not set")
        return self.__player

    @player.setter
    def player(self, value: 'PlayerEntity') -> None:
        self.__player = value
        self.scroll = [-self.__player.x, -self.__player.y]
        if self.__player not in self.entities:
            self.entities.append(self.__player)
        self.player.compute_scroll(0, 0)

    def change_volume(self, volume_type: Literal["general", "music"], volume: float) -> None:
        if volume_type == "general":
            from core.sound import Sound as cSound
            self.general_volume = volume
            for sound in cSound:
                sound.value.set_volume(self.general_volume)

        elif volume_type == "music":
            self.music_volume = volume
            self.music_channel.set_volume(self.music_volume)

    def set_collision_sound(self, val: bool) -> None:
        self.collision_sound = val

    def quit(self) -> None:
        self.run = False
