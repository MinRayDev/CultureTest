from pathlib import Path
from time import time
from typing import Optional, TYPE_CHECKING

from pygame import Surface

import references
from world.collision_type import CollisionType
from world.facing import Facing
from core.sound import Sound
from entities.entity import Entity
from references import game, client
from utils.files import get_resources
from utils.sprites import get_coordinates_with_scroll
from utils.time_util import times, has_elapsed
from world.sign import read

if TYPE_CHECKING:
    from entities.screen import Screen


class PlayerEntity(Entity):
    current_key: str
    motion_ratio: int
    motions: dict[Facing, int]
    __life: int
    velocity: int
    facing: Facing

    def __init__(self, x: int, y: int):
        super().__init__("Player", Path(get_resources(), "player"), x, y)
        self.current_sprite = self.sprites["bottom_idle"]
        self.current_key = "bottom_idle"
        self.motion_ratio = 4
        self.motions = {Facing.NORTH: 0, Facing.EAST: 0, Facing.SOUTH: 0, Facing.WEST: 0}
        self.__life = 3
        self.velocity = 4
        self.facing = Facing.SOUTH

    def draw(self, surface: Surface) -> None:
        from utils.sprites import draw_with_scroll
        draw_with_scroll(surface, self.sprites["shadow"], self.x + self.width // 2 - self.sprites["shadow"].get_width() // 2, self.y + self.height - 20)
        super().draw(surface)

    @property
    def life(self) -> int:
        return self.__life

    @life.setter
    def life(self, value: int) -> None:
        if value < self.__life:
            Sound.hurt.play()
        self.__life = value
        game.hud.set_life(value)

    def stop(self) -> None:
        self.motions = {Facing.NORTH: 0, Facing.EAST: 0, Facing.SOUTH: 0, Facing.WEST: 0}
        self.current_key = f"{str(self.facing)}_idle"
        self.current_sprite = self.sprites[self.current_key]

    def move(self, facing: Facing) -> None:
        motion_x: int = 0
        motion_y: int = 0
        self.facing = facing
        match facing:
            case Facing.EAST:
                motion_x = self.velocity
            case Facing.WEST:
                motion_x = -self.velocity
            case Facing.SOUTH:
                motion_y = self.velocity
            case Facing.NORTH:
                motion_y = -self.velocity

        screen_movement: CollisionType = self.collide(motion_x, motion_y, facing)
        if screen_movement == CollisionType.collision:
            if has_elapsed(times.get("collision", 0), 1):
                times["collision"] = time()
                if references.game.collision_sound:
                    Sound.bounce.play()
                self.stop()

            return
        if self.motions[facing] > 8 * self.motion_ratio:
            self.motions[facing] = 1
        self.motions[facing] += 1
        index_ = round(self.motions[facing] // self.motion_ratio)
        if index_ == 0:
            index_ = 1
        self.current_key = f"{str(self.facing)}_{index_}"
        self.current_sprite = self.sprites[self.current_key]

        self.x += motion_x
        self.y += motion_y

        self.compute_scroll(motion_x, motion_y)
        if screen_movement is not None:
            self.change_screen(screen_movement)

    def interact(self) -> None:
        from entities.screen import ColorManager
        current_screen: Screen = game.screen
        mask, mask_offset = self.get_interaction_area(self.facing, current_screen.get_offsets())
        for i, mask_name in enumerate(ColorManager.get_signs()):
            if current_screen.masks[mask_name.get_name()].overlap(mask, mask_offset):
                read(i)
                return

    def compute_scroll(self, x: int, y: int) -> None:
        if not game.screen.border:
            game.scroll[0] -= x
            game.scroll[1] -= y
            return
        gsw, gsh = client.surface.get_size()
        x__, y__ = get_coordinates_with_scroll(self.current_sprite, self.x - x, self.y - y)
        x_mid: int = self.x + self.width // 2
        y_mid: int = self.y + self.height // 2
        screen_borders: tuple[int, int, int, int] = (
            y_mid - gsh // 2,
            x_mid + gsw // 2,
            y_mid + gsh // 2,
            x_mid - gsw // 2
        )
        surface_borders: tuple[int, int, int, int] = game.screen.get_borders()
        if x == 0 and y == 0:
            if x__ == 0:
                if screen_borders[Facing.EAST] >= surface_borders[Facing.EAST]:
                    game.scroll[0] += screen_borders[Facing.EAST] - surface_borders[Facing.EAST]

                if screen_borders[Facing.WEST] <= surface_borders[Facing.WEST]:
                    game.scroll[0] += screen_borders[Facing.WEST] - surface_borders[Facing.WEST]

            if y__ == 0:
                if screen_borders[Facing.NORTH] <= surface_borders[Facing.NORTH]:
                    game.scroll[1] += screen_borders[Facing.NORTH] - surface_borders[Facing.NORTH]

                if screen_borders[Facing.SOUTH] >= surface_borders[Facing.SOUTH]:
                    game.scroll[1] += screen_borders[Facing.SOUTH] - surface_borders[Facing.SOUTH]
            return

        error_margin: tuple[int, ...] = tuple(range(-self.velocity//2, self.velocity//2))
        screen_border: int = screen_borders[self.facing]
        if x__ in error_margin:
            if self.facing == Facing.EAST:
                if screen_border > surface_borders[Facing.EAST]:
                    screen_border = surface_borders[Facing.EAST]
                if screen_border < surface_borders[Facing.EAST]:
                    game.scroll[0] -= x

            if self.facing == Facing.WEST:
                if screen_border < surface_borders[Facing.WEST]:
                    screen_border = surface_borders[Facing.WEST]
                if screen_border > surface_borders[Facing.WEST]:
                    game.scroll[0] -= x

        if y__ in error_margin:
            if self.facing == Facing.NORTH:
                if screen_border < surface_borders[Facing.NORTH]:
                    screen_border = surface_borders[Facing.NORTH]
                if screen_border > surface_borders[Facing.NORTH]:
                    game.scroll[1] -= y

            if self.facing == Facing.SOUTH:
                if screen_border > surface_borders[Facing.SOUTH]:
                    screen_border = surface_borders[Facing.SOUTH]
                if screen_border < surface_borders[Facing.SOUTH]:
                    game.scroll[1] -= y

    def change_screen(self, screen_movement: CollisionType) -> None:
        if screen_movement != CollisionType.backward:
            if game.question is not None:
                game.question.past = True
                game.question = None
                if screen_movement == CollisionType.bad_forward:
                    self.life -= 1
                else:
                    Sound.secret.play()
                    game.good_answers += 1
            custom: Optional[list[list[int]]] = game.screen.custom
            game.next_screen()
            self.x, self.y = game.screen.px, game.screen.py
            if custom:
                if len(custom) and self.x == 0 and self.y == 0:
                    addon_index: int = 0
                    addons: tuple[str, ...] = tuple(game.screen.addons)
                    if len(addons):
                        addon_index = int(addons[-1].strip("addon")) - 1
                    if len(custom) == 1:
                        addon_index = 0

                    self.x = custom[addon_index][0]
                    self.y = custom[addon_index][1]
            game.scroll = [-self.x, -self.y]
            self.compute_scroll(0, 0)
        else:
            game.previous_screen()
            self.x = game.screen.px
            self.y = game.screen.py
            game.scroll = [-game.screen.px, -game.screen.py]
            self.compute_scroll(0, 0)
        Sound.screen_switch.play()
