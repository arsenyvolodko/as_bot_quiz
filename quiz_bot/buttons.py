from abc import ABC

from aiogram.types import InlineKeyboardButton


class Button:

    def __init__(self) -> None:
        self.name = None
        self.txt = None
        self.callback_suffix: str = "_callback"

    def __str__(self):
        return self.callback

    @property
    def text(self):
        return self.txt

    @property
    def callback(self):
        return self.name.lower() + self.callback_suffix

    def get_button(self, **kwargs) -> InlineKeyboardButton:
        text = kwargs.get("text", self.txt)
        url = kwargs.get("url", None)
        if url:
            return InlineKeyboardButton(text=text, url=url)
        return InlineKeyboardButton(text=text, callback_data=self.callback)


class AutoNameButtonMeta(type):
    def __new__(cls, name, bases, namespace):
        for attr_name, value in namespace.items():
            if isinstance(value, Button):
                if not value.name:
                    value.name = attr_name
                if not value.txt:
                    value.txt = getattr(ButtonsTextStorage, value.name)
        return type.__new__(cls, name, bases, namespace)


class ButtonsTextStorage(ABC):
    CONTINUE_FROM_START = "Продолжить"
    CONTINUE_FROM_SUBSCRIBE = "Я подписался"
    CONTINUE_FROM_AFTER_SUBSCRIBE = "Продолжить"
    START_AGAIN = "Пройти тест ещё раз"


class ButtonsStorage(metaclass=AutoNameButtonMeta):
    CONTINUE_FROM_START = Button()
    CONTINUE_FROM_SUBSCRIBE = Button()
    CONTINUE_FROM_AFTER_SUBSCRIBE = Button()
    START_AGAIN = Button()
