from aiogram.types import InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

from quiz_bot.buttons import ButtonsStorage
from quiz_bot.utils.consts import QUESTION_OPTIONS, GO_BACK
from quiz_bot.utils.factories import QuestionSubmissionFactory


def get_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ButtonsStorage.CONTINUE_FROM_START.text,
        callback_data=ButtonsStorage.CONTINUE_FROM_START.callback
    )
    return builder.as_markup()


def get_continue_after_start_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text="Подписаться",
        url="https://t.me/juniorrosatom"
    )
    builder.button(
        text=ButtonsStorage.CONTINUE_FROM_SUBSCRIBE.text,
        callback_data=ButtonsStorage.CONTINUE_FROM_SUBSCRIBE.callback
    )
    builder.adjust(1)
    return builder.as_markup()


def get_continue_from_subscribe_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ButtonsStorage.CONTINUE_FROM_AFTER_SUBSCRIBE.text,
        callback_data=ButtonsStorage.CONTINUE_FROM_AFTER_SUBSCRIBE.callback,
    )
    builder.adjust(1)
    return builder.as_markup()


def get_question_options_keyboard(question_num: int) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    options_list = QUESTION_OPTIONS[question_num]
    for i in range(5):
        option_text = options_list[i]
        builder.button(
            text=option_text,
            callback_data=QuestionSubmissionFactory(
                question_num=question_num,
                option_num=i
            )
        )
    if question_num == 1:
        pass
    else:
        builder.button(
            text=GO_BACK,
            callback_data=QuestionSubmissionFactory(
                question_num=question_num - 1,
                get_back=True,
            )
        )
    if question_num == 10:
        builder.adjust(5, 1)
    else:
        builder.adjust(1)
    return builder.as_markup()


def get_start_again_keyboard() -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    builder.button(
        text=ButtonsStorage.START_AGAIN.text,
        callback_data=ButtonsStorage.START_AGAIN.callback
    )
    return builder.as_markup()
