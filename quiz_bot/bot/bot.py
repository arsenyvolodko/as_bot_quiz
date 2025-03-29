from collections import defaultdict
from operator import or_

from aiogram import Dispatcher, Router, types
from aiogram.enums import ParseMode, ChatMemberStatus
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, FSInputFile
from aiogram import F

from quiz_bot.buttons import ButtonsStorage
from quiz_bot.utils import consts
from quiz_bot.utils.factories import QuestionSubmissionFactory
from quiz_bot.utils.keyboards import get_start_keyboard, get_continue_after_start_keyboard, \
    get_continue_from_subscribe_keyboard, get_question_options_keyboard, get_start_again_keyboard

dp = Dispatcher()
router = Router()
dp.include_router(router)


@dp.message(CommandStart())
async def welcome_message(message: types.Message, state: FSMContext) -> None:
    await state.clear()
    await message.answer(
        consts.START_TEXT,
        reply_markup=get_start_keyboard()
    )


@router.callback_query(F.data == ButtonsStorage.CONTINUE_FROM_START.callback)
async def handle_continue_from_start_state_query(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(
        consts.NEED_TO_SUBSCRIBE_TEXT, reply_markup=get_continue_after_start_keyboard()
    )


@router.callback_query(F.data == ButtonsStorage.CONTINUE_FROM_SUBSCRIBE.callback)
async def handle_continue_from_subscribe_state_query(call: CallbackQuery, state: FSMContext):
    await state.clear()
    try:
        member = await call.bot.get_chat_member(chat_id=consts.JUNIOR_TEAM_CHAT_ID, user_id=call.from_user.id)
        is_member = (
                member.status in
                {
                    ChatMemberStatus.MEMBER,
                    ChatMemberStatus.ADMINISTRATOR,
                    ChatMemberStatus.CREATOR
                }
        ) if member else False

        if not is_member:
            await call.answer(
                consts.NOT_SUBSCRIBED_TEXT,
                show_alert=True
            )
            return
    except Exception as e:
        pass
    await call.message.edit_text(
        consts.AFTER_SUBSCRIBE_TEXT, reply_markup=get_continue_from_subscribe_keyboard()
    )


@router.callback_query(
    or_(
        F.data == ButtonsStorage.CONTINUE_FROM_AFTER_SUBSCRIBE.callback,
        F.data == ButtonsStorage.START_AGAIN.callback
    )
)
async def handle_continue_after_subscribe_state_query(call: CallbackQuery, state: FSMContext):
    await state.clear()

    kwargs = {
        "text": consts.QUESTIONS_TEXT[1],
        "reply_markup": get_question_options_keyboard(question_num=1)
    }

    if call.data == ButtonsStorage.CONTINUE_FROM_AFTER_SUBSCRIBE.callback:
        await call.message.edit_text(**kwargs)
        return

    await call.message.edit_reply_markup(
        reply_markup=None
    )
    await call.message.answer(**kwargs)


@router.callback_query(
    QuestionSubmissionFactory.filter(
        F.get_back == True
    )
)
async def handle_get_back(call: CallbackQuery, callback_data: QuestionSubmissionFactory, state: FSMContext):
    questions_data = await state.get_data()
    if callback_data.question_num == 9 and 'media_msg' in questions_data:
        await delete_media(questions_data)

    question_num = callback_data.question_num
    await call.message.edit_text(
        consts.QUESTIONS_TEXT[question_num], reply_markup=get_question_options_keyboard(question_num)
    )


@router.callback_query(
    QuestionSubmissionFactory.filter()
)
async def handle_question_submission_query(call: CallbackQuery, callback_data: QuestionSubmissionFactory,
                                           state: FSMContext):
    questions_data = await state.get_data()
    question_num = callback_data.question_num

    option_num = callback_data.option_num
    questions_data[question_num] = option_num
    await state.update_data(questions_data)

    if question_num == 9:
        await call.message.edit_text(
            "Загружаю следующий вопрос.."
        )

        media_msg = await call.message.answer_media_group(
            media=[
                types.InputMediaPhoto(
                    media=FSInputFile(consts.QUESTION_IMAGES[i]),
                ) for i in range(5)
            ]
        )

        questions_data['media_msg'] = media_msg
        await state.update_data(questions_data)

        question_num += 1
        await call.message.answer(
            text=consts.QUESTIONS_TEXT[question_num],
            reply_markup=get_question_options_keyboard(question_num)
        )

        await call.message.delete()

        return

    if question_num == 10:
        text = get_result(questions_data)
        await call.message.edit_text(
            text=text,
            reply_markup=get_start_again_keyboard(),
            parse_mode=ParseMode.HTML
        )

        if 'media_msg' in questions_data:
            await delete_media(questions_data)

        await state.clear()
        return

    question_num += 1
    await call.message.edit_text(
        consts.QUESTIONS_TEXT[question_num], reply_markup=get_question_options_keyboard(question_num)
    )


def get_result(questions_data: dict[int, int]) -> str:
    res_dict = defaultdict(int)
    for value in questions_data.values():
        if isinstance(value, int):
            res_dict[value] += 1
    max_value = max(res_dict.values())
    for key, value in res_dict.items():
        if value == max_value:
            return consts.RESULTS[key]


async def delete_media(question_data):
    media_msg = question_data['media_msg']
    try:
        for msg in media_msg:
            await msg.delete()
    except Exception:
        pass
    del question_data['media_msg']
