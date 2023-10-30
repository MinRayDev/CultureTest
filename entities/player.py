import pygame
from pygame import Surface

import references
from entities.entity import Entity
from ui.color_reference import ColorReference
from ui.text_box import TextBox


class Player(Entity):
    def __init__(self, x: int, y: int, surface: Surface):
        super().__init__("Player", r"C:\Users\Gekota\Documents\Dev\Python\CultureTest\resources\player", x, y)
        self.current_sprite = self.sprites["bottom_idle"]
        self.current_key = "bottom_idle"
        self.bouding_box = {}
        self.ghost = False
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
        self.life = 3
        self.orientation = 2

    def draw(self, surface: Surface):
        if not self.ghost:
            from utils.sprites import draw_with_scroll
            shadow: Surface = self.sprites["shadow"]
            draw_with_scroll(surface, shadow, self.x + self.width//2 - shadow.get_width()//2, self.y + self.height - 20)
        super().draw(surface)


    def move(self, x: int, y: int) -> None:
        forward = False
        yforward = False
        backward = False
        current_screen = references.game.screen
        x_offset = -current_screen.x
        y_offset = -current_screen.y
        if not self.ghost:
            if x > 0:
                self.orientation = 1
                # rect = pygame.Surface((self.width, self.height))
                # rect.fill((255, 255, 0, 255))
                # draw_with_scroll(surface, rect, self.x, self.y + y)
                for y_ in range(self.y + y_offset, self.y + y_offset + self.height):
                    for x_ in range(self.x + x_offset, self.x + x_offset + self.width + x):
                        tup = tuple(current_screen.collisions.get_at((x_, y_)))
                        if tup in ColorReference.collisions.get_value():
                            return
                        elif tup == ColorReference.forward.get_value():
                            forward = True
                            break
                        elif tup == ColorReference.backward.get_value():
                            backward = True
                            break
                        elif tup == ColorReference.yforward.get_value():
                            yforward = True
                            break
            elif x < 0:
                self.orientation = 3
                # rect = pygame.Surface((self.width, self.height))
                # rect.fill((255, 255, 0, 255))
                # draw_with_scroll(surface, rect, self.x, self.y + y)
                for y_ in range(self.y + y_offset, self.y + y_offset + self.height):
                    for x_ in range(self.x + x_offset + x, self.x + x_offset + self.width):
                        tup = tuple(current_screen.collisions.get_at((x_, y_)))
                        if tup in ColorReference.collisions.get_value():
                            return
                        elif tup == ColorReference.forward.get_value():
                            forward = True
                            break
                        elif tup == ColorReference.backward.get_value():
                            backward = True
                            break
                        elif tup == ColorReference.yforward.get_value():
                            yforward = True
                            break
            if y > 0:
                self.orientation = 2
                # rect = pygame.Surface((self.width, self.height))
                # rect.fill((255, 255, 0, 255))
                # draw_with_scroll(surface, rect, self.x, self.y + y)
                for x_ in range(self.x + x_offset, self.x + x_offset + self.width):
                    for y_ in range(self.y + y_offset + y, self.y + y_offset + self.height):
                        tup = tuple(current_screen.collisions.get_at((x_, y_)))
                        if tup in ColorReference.collisions.get_value():
                            return
                        elif tup == ColorReference.forward.get_value():
                            forward = True
                            break
                        elif tup == ColorReference.backward.get_value():
                            backward = True
                            break
                        elif tup == ColorReference.yforward.get_value():
                            yforward = True
                            break
                if self.motions["bottom"] > 8*self.motion_ratio:
                    self.motions["bottom"] = 0
                self.motions["bottom"] += 1
                index_ = round(self.motions["bottom"]//self.motion_ratio)
                if index_ == 0:
                    index_ = 1
                self.current_sprite = self.sprites[f"bottom_{index_}"]
                self.current_key = f"bottom_{index_}"
            elif y < 0:
                self.orientation = 0
                # rect = pygame.Surface((self.width, self.height))
                # rect.fill((255, 255, 0, 255))
                # draw_with_scroll(surface, rect, self.x, self.y + y)
                for x_ in range(self.x + x_offset, self.x + x_offset + self.width):
                    for y_ in range(self.y + y_offset + y, self.y + y_offset + self.height + y):
                        tup = tuple(current_screen.collisions.get_at((x_, y_)))
                        if tup in ColorReference.collisions.get_value():
                            return
                        elif tup == ColorReference.forward.get_value():
                            forward = True
                            break
                        elif tup == ColorReference.backward.get_value():
                            backward = True
                            break
                        elif tup == ColorReference.yforward.get_value():
                            yforward = True
                            break
        self.x += x
        self.y += y
        # sw = screen.get_width()-0
        # top, right, bottom, left
        # sh = screen.get_height()-0
        # points: list[tuple[tuple[int, int], ...]] = [
        #     ((0, 0), (sw//1, 0), (sw, 0)),
        #     ((sw, 0), (sw, sh//1), (sw, sh)),
        #     ((sw, sh), (sw//1, sh), (0, sh)),
        #     ((0, sh), (0, sh//1), (0, 0))
        # ]
        if x > 0:
            # Go right
            # and references.entities[0].width + sx - self.width + x < sw
            # a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[0])
            a = False
            if a:
                pass
            else:
                references.game.scroll[0] -= x
        elif x < 0:
            # Go left
            # < sx - x + self.width
            # a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[2])
            a = False

            if a:
                pass
            else:
                references.game.scroll[0] -= x
        if y > 0:
            # Go down
            # and references.entities[0].height + sy - self.height + y < sh
            # a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[1])
            a = False

            if a:
                pass
            else:
                references.game.scroll[1] -= y
        elif y < 0:
            # Go up
            #  < sy - y
            # a = all(screen.get_at((x_, y_)) == (0, 0, 0, 255) for x_, y_ in points[0])
            a = False

            if a:
                pass
            else:
                references.game.scroll[1] -= y

        if forward or yforward:
            if references.game.question is not None:
                references.game.question.past = True
                references.game.question = None
                if yforward:
                    self.life -= 1
                    if self.life == 0:
                        references.game.game_over()
                else:
                    references.game.good_answers += 1
            custom = references.game.screen.custom
            addons = references.game.screen.addons.copy()
            references.game.next_screen()
            px, py = references.game.screen.px, references.game.screen.py
            self.x = px
            self.y = py
            if custom is not None and px == 0 and py == 0:
                index_ = 0
                if len(addons) > 0:
                    index_ = int(addons[-1].strip("addon")) - 1
                coos = custom[index_]
                self.x = coos[0]
                self.y = coos[1]
            references.game.scroll = [-self.x, -self.y]
        elif backward:
            references.game.previous_screen()
            self.x = references.game.screen.px
            self.y = references.game.screen.py
            references.game.scroll = [-references.game.screen.px, -references.game.screen.py]

    def interact(self):
        current_screen = references.game.screen
        surface = references.client.surface
        x_offset = -current_screen.x
        y_offset = -current_screen.y
        rect = pygame.Surface((self.width, self.height))
        rect.fill((255, 255, 255, 255))
        from utils.sprites import draw_with_scroll
        draw_with_scroll(surface, rect, self.x, self.y)
        match self.orientation:
            case 0:
                rect = pygame.Surface((self.width, 2))
                rect.fill((0, 0, 255, 255))
                draw_with_scroll(surface, rect, self.x, self.y-2)
                for x in range(self.x-1 + x_offset, self.x + self.width + x_offset):
                    for y in range(self.y-2 + y_offset, self.y + y_offset):
                        tup = tuple(current_screen.collisions.get_at((x, y)))
                        if tup in ColorReference.interactions.get_value():
                            type_ = self.check_sign(tup)
                            self.read(type_)
                            break
                    else:
                        continue
                    break
            case 1:
                for y in range(self.y-1 + y_offset, self.y + self.height + y_offset):
                    for x in range(self.x + self.width + x_offset, self.x + self.width + x_offset + 2):
                        tup = tuple(current_screen.collisions.get_at((x, y)))
                        if tup in ColorReference.interactions.get_value():
                            type_ = self.check_sign(tup)
                            self.read(type_)
                            break
                    else:
                        continue
                    break
            case 2:
                for x in range(self.x-1 + x_offset, self.x + self.width + x_offset):
                    for y in range(self.y + self.height + y_offset, self.y + self.height + y_offset + 2):
                        tup = tuple(current_screen.collisions.get_at((x, y)))
                        if tup in ColorReference.interactions.get_value():
                            type_ = self.check_sign(tup)
                            self.read(type_)
                            break
                    else:
                        continue
                    break
            case 3:
                for y in range(self.y-1 + y_offset, self.y + self.height + y_offset):
                    for x in range(self.x-2 + x_offset, self.x + x_offset):
                        tup = tuple(current_screen.collisions.get_at((x, y)))
                        if tup in ColorReference.interactions.get_value():
                            type_ = self.check_sign(tup)
                            self.read(type_)
                            break
                    else:
                        continue
                    break

    @classmethod
    def read(cls, type_: int) -> None:
        surface = references.client.surface
        content: str
        if type_ == 0:
            if references.game.question is None:
                content = "Exemple: Prennez le premier tronc d'arbre a gauche."
            else:
                content = references.game.question.text
        else:
            correct_answer = [key for key, value in references.game.question.answers.items() if value][0]
            print(correct_answer, references.game.question.correct)
            answers = list(references.game.question.answers.keys())
            answers.remove(correct_answer)
            i: float = 0
            match references.game.question.correct:
                case 1:
                    i = 1
                case 2:
                    i = 0.5
                case 3:
                    i = 0
            if type_ == references.game.question.correct:
                content = correct_answer
            else:
                if i == 0.5:
                    if type_ == 1:
                        content = list(references.game.question.answers.keys())[type_]
                    else:
                        content = list(references.game.question.answers.keys())[type_-1]
                else:
                    content = list(references.game.question.answers.keys())[int(type_-i)]
        references.game.menu = TextBox(content, surface)

    @classmethod
    def check_sign(cls, tup: tuple[int, int, int, int]) -> int:
        if tup == ColorReference.question.get_value():
            return 0
        elif tup == ColorReference.answer1.get_value():
            return 1
        elif tup == ColorReference.answer2.get_value():
            return 2
        elif tup == ColorReference.answer3.get_value():
            return 3
