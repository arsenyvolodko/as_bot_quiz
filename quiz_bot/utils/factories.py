from aiogram.filters.callback_data import CallbackData


class QuestionSubmissionFactory(CallbackData, prefix="question_submission_factory"):
    question_num: int
    option_num: int | None = None
    get_back: bool = False
