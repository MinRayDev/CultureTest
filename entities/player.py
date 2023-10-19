from pygame import Surface

import references
from entities.entity import Entity


class Player(Entity):
    def __init__(self, x: int, y: int, surface: Surface):
        super().__init__("Player", r"C:\Users\Gekota\Documents\Dev\Python\CultureTest\resources\player", x, y)
        self.current_sprite = self.sprites["bottom_idle"]
        self.current_key = "bottom_idle"
        self.bouding_box = {}
        for key, value in self.sprites.items():
            value = value.copy()
            for _x in range(value.get_width()):
                for _y in range(value.get_height()):
                    if value.get_at((_x, _y))[3] != 0:
                        value.set_at((_x, _y), (255, 0, 0, 255))
            self.bouding_box[key] = value
        self.default_x, self.default_y = x + surface.get_width() // 2 + references.game.scroll[0] - self.width // 2, y + surface.get_height() // 2 + references.game.scroll[1] - self.height // 2
        self.motion_ratio = 10
        self.motions = {"left": 1, "right": 2, "top": 3, "bottom": 4}

    def move(self, x: int, y: int):
        screen = references.client.client_surface
        x_offset = 1500
        y_offset = 732
        if x > 0:
            for x_ in range(self.x + x_offset + self.width + x, self.x + x_offset, -1):
                for y_ in range(self.y+y_offset, self.y+y_offset+self.height):
                    x_point = x_-(self.x+x_offset+x+1)
                    y_point = y_-(self.y+y_offset+y)
                    if references.game.screen.collisions.get_at((x_, y_)) == (255, 0, 0, 255) and self.bouding_box[self.current_key].get_at((x_point, y_point)) == (255, 0, 0, 255):
                        self.current_sprite.set_at((x_-(self.x+x_offset), y_-(self.y+y_offset)), (0, 0, 0, 0))
                        return
        elif x < 0:
            for x_ in range(self.x+x_offset+x, self.x+x_offset, -1):
                for y_ in range(self.y+y_offset, self.y+y_offset+self.height):
                    x_point = x_ - (self.x + x_offset + x)
                    y_point = y_ - (self.y + y_offset + y)
                    if references.game.screen.collisions.get_at((x_, y_)) == (255, 0, 0, 255) and self.bouding_box[self.current_key].get_at((x_point, y_point)) == (255, 0, 0, 255):
                        self.current_sprite.set_at((x_ - (self.x + x_offset), y_ - (self.y + y_offset)), (0, 0, 0, 0))
                        return
        if y > 0:
            for y_ in range(self.y + y_offset + self.height + y, self.y + y_offset + self.height, -1):
                for x_ in range(self.x+x_offset, self.x+x_offset+self.width):
                    x_point = x_ - (self.x + x_offset + x)
                    y_point = y_ - (self.y + y_offset + y + 1)
                    print(x_point, y_point, self.bouding_box[self.current_key].get_width(), self.bouding_box[self.current_key].get_height())
                    print(references.game.screen.collisions.get_at((x_, y_)) == (255, 0, 0, 255))
                    print("b", self.bouding_box[self.current_key].get_at((x_point, y_point)))
                    if references.game.screen.collisions.get_at((x_, y_)) == (255, 0, 0, 255) and self.bouding_box[self.current_key].get_at((x_point, y_point)) == (255, 0, 0, 255):
                        self.current_sprite.set_at((x_ - (self.x + x_offset), y_ - (self.y + y_offset)), (0, 0, 0, 0))
                        return
            if self.motions["bottom"] > 8*self.motion_ratio:
                self.motions["bottom"] = 0
            self.motions["bottom"] += 1
            index_ = round(self.motions["bottom"]//self.motion_ratio)
            if index_ == 0:
                index_ = 1
            self.current_sprite = self.bouding_box[f"bottom_{index_}"]
            self.current_key = f"bottom_{index_}"
        elif y < 0:
            for x_ in range(self.x+x_offset, self.x+x_offset+self.width):
                for y_ in range(self.y+y_offset+y, self.y+y_offset+y+self.height):
                    if references.game.screen.collisions.get_at((x_, y_)) == (255, 0, 0, 255):
                        return
        self.x += x
        self.y += y
        sw = screen.get_width()-1
        # top, right, bottom, left
        sh = screen.get_height()-1
        points: list[tuple[tuple[int, int], ...]] = [
            ((0, 0), (sw//2, 0), (sw, 0)),
            ((sw, 0), (sw, sh//2), (sw, sh)),
            ((sw, sh), (sw//2, sh), (0, sh)),
            ((0, sh), (0, sh//2), (0, 0))
        ]

        if x > 0:
            # Go right
            # and references.entities[0].width + sx - self.width + x < sw
            a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[1])
            a = False
            if a:
                pass
            else:
                references.game.scroll[0] -= x
        elif x < 0:
            # Go left
            # < sx - x + self.width
            a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[3])
            a = False

            if a:
                pass
            else:
                references.game.scroll[0] -= x
        if y > 0:
            # Go down
            # and references.entities[0].height + sy - self.height + y < sh
            a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[2])
            a = False

            if a:
                pass
            else:
                references.game.scroll[1] -= y
        elif y < 0:
            # Go up
            #  < sy - y
            a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[0])
            a = False

            if a:
                pass
            else:
                references.game.scroll[1] -= y
        tp_ = False
        for x_ in range(self.width):
            if (x_, 0) in references.game.screen.forward_tp:
                tp_ = True
                break
            if (x_, self.height-1) in references.game.screen.forward_tp:
                tp_ = True
                break
        for y_ in range(self.height):
            if (0, y_) in references.game.screen.forward_tp:
                tp_ = True
                break
            if (self.width-1, y_) in references.game.screen.forward_tp:
                tp_ = True
                break
        print(tp_)
        if tp_:
            references.game.next_screen()
            self.x = self.default_x
            self.y = self.default_y
            references.game.scroll = [0, 0]


