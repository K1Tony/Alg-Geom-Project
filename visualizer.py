import pygame as pg
from Assets.Scene import Scene
from Assets.shapesCollections import Point, PointsCollection, LinesCollection, Rectangle, RectsCollection, Line
from Assets.Color import Color
from Assets.Button import Button
from random import uniform

pg.init()


class Time:
    MILLISECOND = 1
    SECOND = 1000
    MINUTE = 60 * SECOND
    HOUR = 60 * MINUTE
    DAY = 24 * HOUR
    WEEK = 7 * DAY
    YEAR = 365 * DAY


class Toggle:
    MANUAL = 1
    AUTOMATIC = 0


class Visualizer:

    __SCENE_DELAY = Time.SECOND
    __TOGGLE = Toggle.MANUAL
    __NEXT_SCENE = 0
    __WAIT = -1

    __BUTTON_COUNT = 7

    def __init__(self, size: pg.Vector2 = None,
                 color: tuple[int, int, int] = Color.WHITE,
                 flags: int = 0):
        if size is None:
            screen_width, screen_height = pg.display.get_desktop_sizes()[0]
            screen_height -= 100
            size = screen_width, screen_height
        self.__size = size
        self.__color = color
        self.__flags = flags

        self.__points = PointsCollection()
        self.__lines = LinesCollection()
        self.__rects = RectsCollection()

        self.__scenes = []
        self.__scene_played = -1

        self.__window = pg.display.set_mode(self.__size, flags=flags)
        self.__point_radius = self.__size[1] // 300

        self.__onclick = None

        self.__new_rect_onclick = []

        self.__search_region = Rectangle()

        self.__buttons = {
            "Add Point": Button(0, 0, width=self.control_panel_width, height=self.height // self.__BUTTON_COUNT,
                   border_color=Color.BLACK, text="Add Point",
                   font=self.font, callback=lambda: self.__set_onclick(self.__add_point_onclick)),
            "Random Points": Button(self.height // self.__BUTTON_COUNT, 0, self.control_panel_width,
                                    self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                                    text="Random Points", font=self.font, callback=lambda: self.add_points(
                    self.generate_random_points())),
            "Add Region": Button(top=2 * self.height // self.__BUTTON_COUNT, left=0,
                                 width=self.control_panel_width,
                   height=self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                   text="Add Region", font=self.font, callback=lambda: self.__set_onclick(self.__add_region_onclick)),
            "Clear area": Button(top=3 * self.height // self.__BUTTON_COUNT, left=0,
                                 width=self.control_panel_width,
                                 height=self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                                 text="Clear area", font=self.font, callback=self.clear),
            "Toggle": Button(top=4 * self.height // self.__BUTTON_COUNT, left=0,
                             width=self.control_panel_width,
                   height=self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                   text=self.toggle, font=self.font, callback=lambda: self.__set_opposite_toggle()),
            "Replay": Button(top=5 * self.height // self.__BUTTON_COUNT, left=0,
                             width=self.control_panel_width,
                   height=self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                   text="Replay", font=self.font, callback=self.__replay),
            "Clear Scenes": Button(top=6 * self.height // self.__BUTTON_COUNT, left=0,
                                   width=self.control_panel_width,
                                   height=self.height // self.__BUTTON_COUNT, border_color=Color.BLACK,
                                   text="Clear Scenes", font=self.font, callback=self.clear_scenes_and_return)
        }

        self.__key_bindings = []

        self.__repeats = set()

        self.__BOUNDING_RECT = Rectangle(0, self.control_panel_width, self.width - self.control_panel_width, self.height)

    @property
    def SCENE_DELAY(self): return self.__SCENE_DELAY

    @property
    def points(self):
        return self.__points

    @property
    def lines(self):
        return self.__lines

    @property
    def rects(self):
        return self.__rects

    @property
    def size(self):
        return self.__size

    @property
    def color(self):
        return self.__color

    @property
    def window(self):
        return self.__window

    @property
    def width(self):
        return self.__size[0]

    @property
    def height(self):
        return self.__size[1]

    @property
    def point_radius(self):
        return self.__point_radius

    def set_point_radius(self, fraction: int = None, raw_pixels: int | float = None):
        if fraction is not None:
            self.__point_radius = self.__size[1] // fraction
        elif raw_pixels is not None:
            self.__point_radius = raw_pixels

    @color.setter
    def color(self, new_color: tuple[int, int, int]):
        self.__color = new_color

    @property
    def scenes(self):
        return self.__scenes

    @property
    def last_scene(self):
        if not self.__scenes: return
        return self.__scenes[-1]

    @property
    def first_scene(self):
        if not self.__scenes: return
        return self.__scenes[0]

    @property
    def scene_played(self):
        return self.__scene_played

    def set_scene_played(self, scene_index: int = -1):
        if len(self.scenes) == 0: return
        if scene_index < 0:
            self.set_scene_played(scene_index + len(self.scenes))
        if 0 <= scene_index < len(self.scenes):
            self.__scene_played = scene_index

    @property
    def control_panel_width(self):
        return self.width // 10

    @property
    def BOUNDING_RECT(self):
        return self.__BOUNDING_RECT

    @property
    def font(self):
        return pg.font.SysFont("Arial", self.height // 20)

    @property
    def toggle(self):
        return f"{'Manual' if self.__TOGGLE == Toggle.MANUAL else 'Auto'}"

    @property
    def search_region(self):
        return self.__search_region

    @search_region.setter
    def search_region(self, rect: Rectangle):
        if rect.left < self.control_panel_width:
            rect.left = self.control_panel_width
        if rect.top < 0:
            rect.top = 0
        if rect.right > self.width:
            rect.right = self.width
        if rect.bottom > self.height:
            rect.bottom = self.height
        self.__search_region = rect

    @property
    def BUTTON_COUNT(self):
        return self.__BUTTON_COUNT

    def draw_rectangle(self, rectangle: Rectangle):
        if self.__window is None: return
        border_rect = pg.Rect(rectangle.left - rectangle.border_width, rectangle.top - rectangle.border_width,
                              rectangle.width + rectangle.border_width + rectangle.border_width,
                              rectangle.height + rectangle.border_width + rectangle.border_width)
        if rectangle.color == Color.VOID:
            pg.draw.line(self.__window, rectangle.border_color, rectangle.topleft, rectangle.topright,
                         width=rectangle.border_width)
            pg.draw.line(self.__window, rectangle.border_color, rectangle.topright, rectangle.bottomright,
                         width=rectangle.border_width)
            pg.draw.line(self.__window, rectangle.border_color, rectangle.bottomright, rectangle.bottomleft,
                         width=rectangle.border_width)
            pg.draw.line(self.__window, rectangle.border_color, rectangle.bottomleft, rectangle.topleft,
                         width=rectangle.border_width)
        elif rectangle.alpha < 255:
            surface = pg.Surface(rectangle.size)
            surface.fill(rectangle.color)
            surface.set_alpha(rectangle.alpha)
            self.__window.blit(surface, rectangle.topleft)
        else:
            pg.draw.rect(self.__window, rectangle.border_color, border_rect, width=rectangle.border_width)
            pg.draw.rect(self.__window, rectangle.color, pg.Rect(rectangle.left, rectangle.top,
                                                                 rectangle.width, rectangle.height))

    def set_scene_delay(self, delay: int):
        if delay < 0: delay = 0
        self.__SCENE_DELAY = delay

    def __set_opposite_toggle(self):
        if self.__TOGGLE == Toggle.MANUAL:
            self.set_automatic()
        else:
            self.set_manual()
        self.__buttons["Toggle"].update_text(self.toggle)

    def set_manual(self):
        self.__TOGGLE = Toggle.MANUAL

    def set_automatic(self):
        self.__TOGGLE = Toggle.AUTOMATIC

    def clear_scenes_and_return(self):
        self.__scene_played = 0
        self.__NEXT_SCENE = True
        self.__set_scene()
        self.clear_scenes()

    def __set_background(self):
        if self.__window is None: return
        if self.__TOGGLE == Toggle.AUTOMATIC and self.__scene_played < len(self.__scenes):
            self.__WAIT += 1
            if self.__WAIT >= self.__SCENE_DELAY:
                self.__WAIT = -1
                self.__auto_set_scene()
        else:
            self.__set_scene()
        for point in self.__points.items:
            pg.draw.circle(self.__window, point.color, point.pos, self.__point_radius)
        for line in self.__lines.items:
            pg.draw.line(self.__window, line.color, line.start.pos, line.end.pos, width=line.width)
        for rect in self.__rects.items:
            self.draw_rectangle(rect)

        for text, button in self.__buttons.items():
            self.draw_rectangle(button)
            for txt, pos in zip(button.text_to_draw, button.text_positions):
                self.__window.blit(txt, pos)
        self.draw_rectangle(self.__search_region)
        pg.draw.line(self.__window, Color.BLACK, (self.control_panel_width, 0), (self.control_panel_width, self.height),
                     width=6)

    def __set_scene(self):
        if len(self.__scenes) > 0:
            if not self.__NEXT_SCENE:
                return
            self.__scene_played += self.__NEXT_SCENE
            self.__scene_played %= len(self.__scenes)
            scene = self.__scenes[self.__scene_played]
            self.__points = scene.points
            self.__lines = scene.lines
            self.__rects = scene.rects
            self.__NEXT_SCENE = False

    def __auto_set_scene(self):
        if len(self.__scenes) > 0:
            if self.__scene_played == len(self.__scenes) - 1:
                return
            if self.__scene_played in self.__scene_pauses:
                return
            self.__scene_played += 1
            scene = self.__scenes[self.__scene_played]
            self.__points = scene.points
            self.__lines = scene.lines
            self.__rects = scene.rects

    def __replay(self):
        self.__scene_played = -1

    def clear(self):
        self.__points = PointsCollection()
        self.__lines = LinesCollection()
        self.__rects = RectsCollection()
        self.__search_region = Rectangle()
        self.scenes.clear()
        self.__scene_played = -1

    def __set_onclick(self, function_callback):
        self.__onclick = function_callback

    def __add_point_onclick(self, pos: Point):
        if pos in self.BOUNDING_RECT:
            self.add_points(PointsCollection([pos]))

    def __add_region_onclick(self, pos: Point):
        if pos.tuple() not in self.BOUNDING_RECT: return
        if len(self.__new_rect_onclick) == 0:
            self.__new_rect_onclick.append(pos)
            self.add_points(PointsCollection([pos], color=Color.GREEN))
        elif len(self.__new_rect_onclick) == 1:
            self.__new_rect_onclick.append(pos)
            self.__search_region = Rectangle.form(*self.__new_rect_onclick, fill_color=Color.GREEN, alpha=50)
            self.__rects = RectsCollection()
            self.remove_points(PointsCollection(self.__new_rect_onclick))
        else:
            self.__search_region = Rectangle()
            self.__new_rect_onclick.clear()
            self.__add_region_onclick(pos)

    def add_points(self, points: PointsCollection):
        if points is None: return
        self.__points += points.__copy__()

    def add_lines(self, lines: LinesCollection):
        if lines is None: return
        self.__lines += lines.__copy__()

    def add_rects(self, rects: RectsCollection):
        if rects is None: return
        self.__rects += rects.__copy__()

    def remove_points(self, points: PointsCollection):
        self.__points -= points

    def remove_lines(self, lines: LinesCollection):
        self.__lines -= lines

    def add_scene(self, points: PointsCollection | None = None, lines: LinesCollection | None = None,
                  rects: RectsCollection | None = None):
        self.__scenes.append(Scene(points, lines, rects))

    def add_updated_scene(self, points: PointsCollection | None = None, lines: LinesCollection | None = None,
                          rects: RectsCollection | None = None):
        if len(self.__scenes) == 0: self.add_scene(points, lines, rects)
        updated_points = self.__scenes[-1].points + points
        updated_lines = self.__scenes[-1].lines + lines
        updated_rects = self.__scenes[-1].rects + rects
        self.add_scene(updated_points, updated_lines, updated_rects)

    def update_last_scene(self, points: PointsCollection | None = None, lines: LinesCollection | None = None,
                          rects: RectsCollection | None = None):
        self.__scenes[-1] = Scene(
            points if points is not None else self.__scenes[-1].points,
            lines if lines is not None else self.__scenes[-1].lines,
            rects if rects is not None else self.__scenes[-1].rects
        )

    def pop_scene(self):
        self.__scenes.pop()

    def remove_scene(self, scene: Scene):
        self.__scenes.remove(scene)

    def clear_scenes(self):
        self.__scenes.clear()
        self.__scene_played = -1
        self.__scene_pauses = {}

    def generate_random_points(self, bound_x: tuple[float, float] = None, bound_y: tuple[float, float] = None,
                               color: tuple[int, int, int] = Color.RED, point_count: int = 100):
        if bound_x is None: bound_x = self.control_panel_width, self.width
        bound_x = max(0, bound_x[0]), min(self.width, bound_x[1])

        if bound_y is None: bound_y = 0, self.height
        bound_y = max(0, bound_y[0]), min(self.height, bound_y[1])
        points = [
            Point(uniform(*bound_x),
                  uniform(*bound_y), self.__point_radius,
                  color) for _ in range(point_count)
        ]
        return PointsCollection(points)

    def add_key_binding(self, key: int, callback):
        self.__key_bindings.append((key, callback))

    def add_button(self, text: str, key: str, function_callback):
        self.__BUTTON_COUNT += 1
        for i, button in self.__buttons.items():
            self.__buttons[i] = button.resized_copy(button.top * (self.__BUTTON_COUNT - 1) / self.__BUTTON_COUNT,
                                                    button.left, button.width,
                                                    button.height * (self.__BUTTON_COUNT - 1) / self.__BUTTON_COUNT)
        self.__buttons[key] = \
            Button(self.height - self.height // self.__BUTTON_COUNT, 0, self.control_panel_width,
                   self.height // self.__BUTTON_COUNT,
                   border_color=Color.BLACK, text=text, font=self.font, callback=function_callback)

    def remove_button(self, text: str):
        self.__buttons.pop(text)

    def add_repeatable(self, function_callback):
        self.__repeats.add(function_callback)

    def remove_repeatable(self, function_callback):
        if function_callback in self.__repeats:
            self.__repeats.remove(function_callback)

    def clear_repeatable(self):
        self.__repeats.clear()

    def update_button(self, key: str, text: str = '', function_callback=None):
        self.__buttons[key].update_text(text)
        self.__buttons[key].callback = function_callback

    def run(self):
        run = True
        clock = pg.time.Clock()

        while run:
            clock.tick(Time.SECOND)
            for event in pg.event.get():
                if event.type == pg.QUIT:
                    run = False

                if event.type == pg.KEYDOWN:
                    if event.key == pg.K_LEFT:
                        self.__NEXT_SCENE = -1
                    if event.key == pg.K_RIGHT:
                        self.__NEXT_SCENE = 1
                    for key, callback in self.__key_bindings:
                        if event.key == key:
                            callback()
                if event.type == pg.MOUSEBUTTONDOWN and event.button == pg.BUTTON_LEFT:
                    pos = Point(*pg.mouse.get_pos(), self.point_radius)
                    if self.__onclick is not None:
                        self.__onclick(pos)
                    for text, button in self.__buttons.items():
                        if pos.tuple() in button:
                            button.click()
                            break

            for text, button in self.__buttons.items():
                button.highlight_on_hover(pg.mouse.get_pos())

            for repeat in self.__repeats:
                repeat()

            self.__window.fill(self.color)
            self.__set_background()
            pg.display.update()
