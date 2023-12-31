import pygame

from . import _constants
from . import _base as _wuib
from ._bars import Slider, ProgressBar
from ._buttons import Button, Checkbox
from ._containers import VCont, HCont
from ._images import Image, Slideshow, GIF
from ._menus import DropMenu, SelectionList
from ._separators import Line, Separator
from ._texts import Label, Entryline
from ._windows import Window

from . import withuiext as ext

DefaultSettings = _wuib._Settings
EmptyElement = _wuib._Element


class UserSettings:
    settings: dict[str, dict[str, _wuib.typing.Any]] = {}

    @classmethod
    def add(cls, name: str, **kwargs: dict[str, _wuib.typing.Any]) -> dict[str, _wuib.typing.Any]:
        cls.settings[name] = kwargs
        return kwargs

    @classmethod
    def get(cls, name: str) -> dict[str, _wuib.typing.Any]:
        return cls.settings[name]


class Themes:
    PURPLE = {
        'background_color': (65, 0, 117),
        'hover_color': (101, 0, 171),
        "dark_bg_color": (31, 0, 61),
        "click_color": (45, 0, 75),
        "outline_color": (67, 0, 137),
        "inner_color": "purple",
        "text_color": "white",
        "navigation_color": "white",
    }
    GREEN = {
        "background_color": (0, 78, 18),
        "dark_bg_color": (0, 35, 8),
        "hover_color": (0, 115, 35),
        "click_color": (0, 58, 14),
        "outline_color": (0, 95, 20),
        "inner_color": (0, 255, 155),
        "text_color": "white",
        "navigation_color": "yellow",
    }
    BLUE = {
        "dark_bg_color": (0, 10, 60),
        "background_color": (0, 30, 125),
        "hover_color": (0, 48, 170),
        "click_color": (0, 20, 105),
        "outline_color": (0, 50, 145),
        "inner_color": (0, 100, 255),
        "text_color": "white",
        "navigation_color": "green",
    }
    RED = {
        "dark_bg_color": (55, 0, 0),
        "background_color": (115, 0, 0),
        "hover_color": (155, 0, 0),
        "click_color": (100, 0, 0),
        "outline_color": (135, 0, 0),
        "inner_color": (255, 0, 0),
        "text_color": "white",
        "navigation_color": "yellow",
    }
    DARK = {
        "dark_bg_color": (17, 17, 17),
        "background_color": (30, 30, 30),
        "hover_color": (40, 40, 40),
        "click_color": (22, 22, 22),
        "outline_color": (50, 50, 50),
        "inner_color": (0, 100, 200),
        "text_color": "white",
        "navigation_color": "red",
    }

    LIGHT = {
        "dark_bg_color": (245, 245, 245),
        "background_color": (255, 255, 255),
        "hover_color": (242, 242, 242),
        "click_color": (230, 230, 230),
        "outline_color": (230, 230, 230),
        "inner_color": (0, 150, 255),
        "text_color": "black",
        "navigation_color": "yellow",
    }

    @classmethod
    def set_default(cls, builtin_color_theme_or_name):
        theme = None
        if isinstance(builtin_color_theme_or_name, str):
            themes = {"red": cls.RED, "blue": cls.BLUE, "green": cls.GREEN, "purple": cls.PURPLE, "dark": cls.DARK,
                      "light": cls.LIGHT, "black": cls.DARK, "white": cls.LIGHT}
            if builtin_color_theme_or_name.lower() not in themes:
                raise _wuib._WithUIException(
                    f"There isn't any builtin theme with name '{builtin_color_theme_or_name}'. Available are red, blue, green, purple, dark, light")
            theme = themes[builtin_color_theme_or_name.lower()]
        else:
            theme = builtin_color_theme_or_name
            for col in ["dark_bg_col", "background_color", "hover_color",
                        "click_color", "outline_color", "inner_color", "text_color", "navigation_color"]:
                if col not in theme:
                    raise _wuib._WithUIException(
                        f"The theme dict provided must contain the '{col}' key")
        _wuib._Settings.dark_bg_color = theme["dark_bg_color"]
        _wuib._Settings.background_color = theme["background_color"]
        _wuib._Settings.hover_color = theme["hover_color"]
        _wuib._Settings.click_color = theme["click_color"]
        _wuib._Settings.outline_color = theme["outline_color"]
        _wuib._Settings.inner_color = theme["inner_color"]
        _wuib._Settings.text_color = theme["text_color"]
        _wuib._Settings.navigation_color = theme["navigation_color"]


INVISIBLE: dict[str, bool] = {
    "has_background": False,
    "has_outline": False
}

SCROLLABLE: dict[str, bool] = {
    "can_scroll_h": True,
    "can_scroll_v": True
}

STATIC: dict[str, bool] = {
    "can_press": False,
    "can_hover": False,
    "can_select": False,
}

NORESIZE: dict[str, bool] = {
    "auto_resize_h": False,
    "auto_resize_v": False
}

MODERN_DOWN_ARROW = " ▼ "
MODERN_UP_ARROW = " ▲ "


def settings_help(element: str | type[_wuib._Element] | _wuib._Element = "Element", setting: str = None) -> str | dict[str, str]:
    element_name = element
    if isinstance(element_name, type):
        element_name = element.__name__
    elif isinstance(element_name, _wuib._Element):
        element_name = element.__class__.__name__
    if element_name in _constants._SETTINGS_HELP:
        settings = _constants._SETTINGS_HELP[element_name].copy()
        if element_name != "Element":
            settings.update(_wuib._SETTINGS_HELP["Element"])
        if setting is not None:
            if setting in settings:
                return settings[setting]
            else:
                raise _wuib._WithUIException(
                    f"Element '{element_name}' has no setting '{setting}'")
        else:
            return settings
    else:
        raise _wuib._WithUIException(
            f"No element exist with name '{element_name}'. Available are: '{_wuib._SETTINGS_HELP.keys()}'")


def pretty_print(json_like_object: _wuib.typing.Any):
    if isinstance(json_like_object, str):
        print(json_like_object)
        return
    formatted = _wuib.json.dumps(json_like_object, indent=2)
    print(formatted)


def pretty_format(json_like_object: _wuib.typing.Any) -> str:
    if isinstance(json_like_object, str):
        return json_like_object
    formatted = _wuib.json.dumps(json_like_object, indent=2)
    return formatted


def refresh_default_font():
    func = pygame.font.SysFont if _wuib._Settings.sysfont_name else pygame.font.Font
    font_name = _wuib._Settings.sysfont_name if _wuib._Settings.sysfont_name else _wuib._Settings.font_name
    _wuib._Settings.font = func(font_name, _wuib._Settings.font_size)


def raycast(position: _wuib._Coordinate) -> _wuib._Element | None:
    for element in sorted(_wuib._UIManager.root_elements, key=lambda tel: -tel._root_index):
        for el in _wuib._UIManager.top_elements:
            if el._root_element._root_index == element._root_index:
                result = el._raycast(position, True)
                if result:
                    return result
        result = element._raycast(position)
        if result:
            return result
    return None


def get_all_elements() -> list[_wuib._Element]:
    return _wuib._UIManager.all_elements.copy()


def apply_settings_to_all_elements(**kwargs):
    for element in _wuib._UIManager.all_elements:
        element.set(**kwargs)


def set_hover_sound(sound: pygame.mixer.Sound):
    _wuib._UIManager.hover_sound = sound


def set_click_sound(sound: pygame.mixer.Sound):
    _wuib._UIManager.click_sound = sound


def disable_keyboard_navigation():
    _wuib._UIManager.navigating = False
    _wuib._UIManager.tabbed_element = None
    _wuib._UIManager.navigation_enabled = False


def enable_keyboard_navigation():
    _wuib._UIManager.navigation_enabled = True


def register_event(event: pygame.event.Event):
    if _wuib._UIManager.frame_ended:
        _wuib._UIManager.frame_ended = False
        _wuib._UIManager.frame_events = []
    _wuib._UIManager.frame_events.append(event)


def update_ui():
    if _wuib._UIManager.frame_ended:
        _wuib._UIManager.frame_ended = False
        _wuib._UIManager.frame_events = []
    _wuib._UIManager.update()
    for element in _wuib._UIManager.root_elements:
        element._update()
    _wuib._UIManager.frame_ended = True


def draw_ui(surface: pygame.Surface):
    for element in sorted(_wuib._UIManager.root_elements, key=lambda tel: tel._root_index):
        element._draw(surface)
        for el in _wuib._UIManager.top_elements:
            if el._root_element._root_index == element._root_index and element.settings.visible:
                el._draw(surface)
