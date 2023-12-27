from aiogram import F
from aiogram import types
from aiogram.filters.callback_data import CallbackData
import db
import quizCommands

class quizCallback(CallbackData, prefix="quizCallback"):
    answerCorrect: bool
    answerIndex: int

def registerCallbacks(quiz_data, dbName, dp):
    @dp.callback_query(quizCallback.filter(F.answerCorrect == True))
    async def rightAnswerCallback(query: types.CallbackQuery, callback_data: quizCallback):
        await genericAnswerCallback(query, callback_data)

    @dp.callback_query(quizCallback.filter(F.answerCorrect == False))
    async def wrongAnswerCallback(query: types.CallbackQuery, callback_data: quizCallback):
        await genericAnswerCallback(query, callback_data)

    async def genericAnswerCallback(callback, callback_data):
        await callback.bot.edit_message_reply_markup(
            chat_id=callback.from_user.id,
            message_id=callback.message.message_id,
            reply_markup=None
        )
        
        current_question_index = await db.get_quiz_index(dbName, callback.from_user.id)
        correctOptionIndex = quiz_data[current_question_index]['correct_option']
        correct_option = quiz_data[current_question_index]['options'][correctOptionIndex]
        await callback.message.answer("Ваш ответ: " + quiz_data[current_question_index]['options'][callback_data.answerIndex])
        if(callback_data.answerCorrect):
            await callback.message.answer("Верно!")
            await db.registerCorrectAnswer(dbName, callback.from_user.id)
        else:
            await callback.message.answer("Неправильно. Правильный ответ: " + correct_option)
        current_question_index += 1
        await db.update_quiz_index(dbName, callback.from_user.id, current_question_index)

        if current_question_index < len(quiz_data):
            await quizCommands.get_question(current_question_index, quiz_data, callback.message)
        else:
            await callback.message.answer("Это был последний вопрос. Квиз завершен!")
            await db.registerFinishedQuiz(dbName, callback.from_user.id)