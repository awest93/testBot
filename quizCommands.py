import utilities
import db

#modified base code
async def get_question(current_question_index, quiz_data, message):
    # Получение текущего вопроса из словаря состояний пользователя
    correct_index = quiz_data[current_question_index]['correct_option']
    opts = quiz_data[current_question_index]['options']
    kb = utilities.generate_options_keyboard(opts, opts[correct_index])
    await message.answer(f"{quiz_data[current_question_index]['question']}", reply_markup=kb)

async def new_quiz(message, dbName, quiz_data):
    user_id = message.from_user.id
    current_question_index = 0
    await db.registerNewUser(dbName, user_id)
    await db.restartQuizStats(dbName, user_id)
    await get_question(current_question_index, quiz_data, message)

#added code
async def continue_quiz(message, dbName, quiz_data):
    user_id = message.from_user.id
    current_question_index = await db.get_quiz_index(dbName, user_id)
    usrId = await db.getUserId(dbName, message.from_user.id)
    if current_question_index >= len(quiz_data) or usrId<0:
        await message.answer("Не найдены данные для продолжения викторины, будет запущена новая игра!")
        await new_quiz(message, dbName, quiz_data)
    else:
        await get_question(current_question_index, quiz_data, message)