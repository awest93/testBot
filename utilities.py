from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram import types
import callbacks

#base code
def generate_options_keyboard(answer_options, right_answer):
    builder = InlineKeyboardBuilder()

    i = 0
    for option in answer_options:
        builder.add(types.InlineKeyboardButton(
            text=option,
            callback_data=callbacks.quizCallback(answerCorrect = True if option == right_answer else False, answerIndex = i).pack())
        )
        i+=1

    builder.adjust(1)
    return builder.as_markup()