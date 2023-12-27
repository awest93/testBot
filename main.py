import asyncio
import logging
from aiogram import Bot, Dispatcher
import db
import handlers
import callbacks
import json

logging.basicConfig(level=logging.INFO)
API_TOKEN=""
DB_NAME = ""
quiz_data = []
populateDBScriptName=""
with open("config.json", encoding="UTF-8") as config:
    configData = json.load(config)
    API_TOKEN=configData["apiToken"]
    DB_NAME = configData["dbName"]
    quiz_data = configData["quizData"]
    populateDBScriptName = configData["populateDBScript"]

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

async def main():
    callbacks.registerCallbacks(quiz_data, DB_NAME, dp)
    handlers.registerHandlers(dp, DB_NAME, quiz_data)
    await db.create_table(DB_NAME)
    await db.populateDB(DB_NAME, populateDBScriptName)
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())