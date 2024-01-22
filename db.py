import aiosqlite

#modified base code
async def create_table(DB_NAME):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state 
        (
            user_id INTEGER PRIMARY KEY, 
            question_index INTEGER,
            quizCompleted bool,
            quizCorrectAnswersNum integer
        )''')
        await db.commit()

async def get_quiz_index(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', [user_id]) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def update_quiz_index(DB_NAME, user_id, index):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('update quiz_state set question_index = ? where user_id=?', (index, user_id))
        await db.commit()

#added code
async def registerNewUser(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT * FROM quiz_state WHERE user_id = (?)', [user_id]) as cursor:
            results = await cursor.fetchone()
            if results is None:
                await db.execute('INSERT INTO quiz_state (user_id, question_index, quizCompleted, quizCorrectAnswersNum) VALUES (?, ?, ?, ?)', 
                (user_id, 0, False, 0))
        await db.commit()

async def getUserId(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT user_id FROM quiz_state WHERE user_id = (?)', [user_id]) as cursor:
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return -1

async def populateDB(DB_NAME, populateSQLScript):
    async with aiosqlite.connect(DB_NAME) as db:
        with open(populateSQLScript, "r") as sqlScript:
            await db.execute(sqlScript.read())
            await db.commit()

async def getStatistics(DB_NAME):
    stats={
        "avgCorrectRatio":0,
        "TotalUsers":0,
        "UsersCompletedQuiz":0}
    async with aiosqlite.connect(DB_NAME) as db:
        async with db.execute('SELECT avg(CAST(quizCorrectAnswersNum AS float)/CAST(question_index AS float)) FROM quiz_state where quizCompleted = true') as cursor:
            results = await cursor.fetchone()
            if results is not None:
                stats["avgCorrectRatio"] = results[0]*100
        async with db.execute('SELECT count(*) FROM quiz_state') as cursor:
            results = await cursor.fetchone()
            if results is not None:
                stats["TotalUsers"] = results[0]
        async with db.execute('SELECT count(*) FROM quiz_state where quizCompleted = true') as cursor:
            results = await cursor.fetchone()
            if results is not None:
                stats["UsersCompletedQuiz"] = results[0]
    return stats

async def restartQuizStats(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('update quiz_state set question_index = ?, quizCompleted = ?, quizCorrectAnswersNum = ? where user_id=?', (0, False, 0, user_id))
        await db.commit()

async def registerCorrectAnswer(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('update quiz_state set quizCorrectAnswersNum = (select quizCorrectAnswersNum+1 from quiz_state where user_id=?) where user_id=?', (user_id,user_id))
        await db.commit()

async def registerFinishedQuiz(DB_NAME, user_id):
    async with aiosqlite.connect(DB_NAME) as db:
        await db.execute('update quiz_state set quizCompleted = ? where user_id=?', (True, user_id))
        await db.commit()