import aiosqlite
import asyncio
async def create_table():
    # Создаем соединение с базой данных (если она не существует, то она будет создана)
    async with aiosqlite.connect('quiz_bot.sql') as db:
        # Выполняем SQL-запрос к базе данных
        await db.execute('''CREATE TABLE IF NOT EXISTS quiz_state (user_id INTEGER PRIMARY KEY, question_index INTEGER)''')
        await db.execute('''CREATE TABLE IF NOT EXISTS result (user_id INTEGER PRIMARY KEY, quest_right INTEGER)''')
        # Сохраняем изменения
        await db.commit()
#Создаём таблицу
asyncio.run(create_table())

async def update_quiz_index(user_id, index):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect('quiz_bot.sql') as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT OR REPLACE INTO quiz_state (user_id, question_index) VALUES (?, ?)', (user_id, index))
        # Сохраняем изменения
        await db.commit()


async def get_quiz_index(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect('quiz_bot.sql') as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT question_index FROM quiz_state WHERE user_id = (?)', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0

async def result_right(user_id, right):
    # Создаем соединение с базой данных (если она не существует, она будет создана)
    async with aiosqlite.connect('quiz_bot.sql') as db:
        # Вставляем новую запись или заменяем ее, если с данным user_id уже существует
        await db.execute('INSERT INTO result (user_id, quest_right) VALUES (?, ?) ON CONFLICT(user_id) DO UPDATE SET quest_right = excluded.quest_right', (user_id, right))
        # Сохраняем изменения
        await db.commit()

async def get_result_right(user_id):
    # Подключаемся к базе данных
    async with aiosqlite.connect('quiz_bot.sql') as db:
        # Получаем запись для заданного пользователя
        async with db.execute('SELECT quest_right FROM result WHERE user_id = ?', (user_id,)) as cursor:
            # Возвращаем результат
            results = await cursor.fetchone()
            if results is not None:
                return results[0]
            else:
                return 0