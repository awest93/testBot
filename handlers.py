from aiogram.filters.command import Command
from aiogram import types
from aiogram.utils.keyboard import ReplyKeyboardBuilder
from aiogram import F
import quizCommands
import db

def registerHandlers(dp, dbName, quiz_data):
    @dp.message(Command("start"))
    async def cmd_start(message: types.Message):
        builder = ReplyKeyboardBuilder()
        builder.add(types.KeyboardButton(text="Начать новую викторину"))
        builder.add(types.KeyboardButton(text="Продолжить викторину"))
        builder.add(types.KeyboardButton(text="Статистика"))
        await message.answer("Добро пожаловать в викторину!", reply_markup=builder.as_markup(resize_keyboard=True))

    @dp.message(F.text=="Начать новую викторину")
    @dp.message(Command("quizNew"))
    async def newQuizHandler(message: types.Message):
        await message.answer(f"Давайте начнем викторину!")
        await quizCommands.new_quiz(message, dbName, quiz_data)

    @dp.message(F.text=="Продолжить викторину")
    @dp.message(Command("quizContinue"))
    async def continueQuizHandler(message: types.Message):
        await message.answer(f"Продолжаем викторину!")
        await quizCommands.continue_quiz(message, dbName, quiz_data)

    @dp.message(F.text=="Статистика")
    @dp.message(Command("stats"))
    async def quizStats(message: types.Message):
        stats=await db.getStatistics(dbName)
        await message.answer(f"В среднем пользователи, завершившие викторину, дали %.2f процентов правильных ответов!\
                            \nВсего %d пользователей попыталось пройти викторину!\
                            \nИз них %d пользователей завершили прохождение викторины!" % 
                            (stats["avgCorrectRatio"],stats["TotalUsers"],stats["UsersCompletedQuiz"]))