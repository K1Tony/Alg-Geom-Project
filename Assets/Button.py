from Shapes.Rectangle import Rectangle, Color
import pygame as pg

pg.font.init()


class Button(Rectangle):

    def __init__(self, top: float = 0, left: float = 0, width: float = 0, height: float = 0,
                 fill_color: tuple[int, int, int] = Color.VOID, border_width: int = 3,
                 border_color: tuple[int, int, int] = Color.RED, font_color: tuple[int, int, int] = Color.BLACK,
                 hover_font_color: tuple[int, int, int] = Color.BLUE, hover_fill_color: tuple[int, int, int] = Color.CYAN,
                 click_font_color: tuple[int, int, int] = Color.WHITE, click_fill_color: tuple[int, int, int] = Color.RED,
                 alpha: int = 255, text: str = '', font: pg.font.Font = None, callback=None):
        super(Button, self).__init__(top, left, width, height, fill_color, border_width, border_color, alpha)
        self.text = text
        self.text_to_draw = font.render(text, 1, font_color)
        self.font_color = font_color
        self.font = font
        self.callback = callback

        self.__base_font_color = font_color
        self.__base_fill_color = fill_color

        self.__hover_font_color = hover_font_color
        self.__hover_fill_color = hover_fill_color

        self.__click_font_color = click_font_color
        self.__click_fill_color = click_fill_color

        self.__active = True

    @property
    def active(self):
        return self.__active

    def click(self):
        if self.callback is None or not self.__active: return
        self.callback()

    def update_text(self, text):
        self.text = text
        self.text_to_draw = self.font.render(text, 1, self.font_color)

    def highlight_on_hover(self, pos):
        if not self.__active: return
        if pos not in self:
            self.font_color = self.__base_font_color
            self.color = self.__base_fill_color
        else:
            self.font_color = self.__hover_font_color
            self.color = self.__hover_fill_color

    def activate(self):
        self.__active = True
        self.alpha = 255
        self.text_to_draw.set_alpha(self.alpha)

    def deactivate(self):
        self.__active = False
        self.alpha = 100
        self.text_to_draw.set_alpha(self.alpha)
        self.color = self.__base_fill_color
        self.font_color = self.__base_font_color
