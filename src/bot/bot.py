import logging

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

API_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot = Bot(API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
user_data = []

@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):

    kb = [
        [
            types.KeyboardButton(text="Маршрут"),
            types.KeyboardButton(text="Анкета")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
        input_field_placeholder="Выберите, что вы хотите"
    )

    
    # This handler will be called when user sends `/start` or `/help` command
    
    await message.reply("Привет!\nЯ бот, который поможет проложить маршрут", reply_markup=keyboard)
    await bot.send_sticker(message.from_user.id, sticker = "CAACAgIAAxkBAAEJwlpkun7HJX19BUAerEIc3G7jVD4RjgACrRgAAnmFiUi3haSlMSLa5S8E")

@dp.message_handler(text=["Анкета"])
async def start_form(message: types.Message):

    kb = [
        [
            types.KeyboardButton(text="0:00"),
            types.KeyboardButton(text="1:00"),
            types.KeyboardButton(text="2:00")],
            [types.KeyboardButton(text="3:00"),
            types.KeyboardButton(text="4:00"),
            types.KeyboardButton(text="5:00")],
            [types.KeyboardButton(text="6:00"),
            types.KeyboardButton(text="7:00"),
            types.KeyboardButton(text="8:00")],
            [types.KeyboardButton(text="9:00"),
            types.KeyboardButton(text="10:00"),
            types.KeyboardButton(text="11:00")],
            [types.KeyboardButton(text="12:00"),
            types.KeyboardButton(text="13:00"),
            types.KeyboardButton(text="14:00")],
            [types.KeyboardButton(text="15:00"),
            types.KeyboardButton(text="16:00"),
            types.KeyboardButton(text="17:00")],
            [types.KeyboardButton(text="18:00"),
            types.KeyboardButton(text="19:00"),
            types.KeyboardButton(text="20:00")],
            [types.KeyboardButton(text="21:00"),
            types.KeyboardButton(text="22:00"),
            types.KeyboardButton(text="23:00")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=kb,
        resize_keyboard=True,
    )
    
    await message.answer("Когда вы пребываете в город?", reply_markup=keyboard)
    user_data.append(text);

    

"""
@dp.callback_query_handler(text=["arrive_1", "arrive_2", "arrive_3", "arrive_4",  "arrive_5", "arrive_6", "arrive_7", "arrive_8", "arrive_9", "arrive_10", 
"arrive_11", "arrive_12", "arrive_13", "arrive_14", "arrive_15", "arrive_16", "arrive_17", "arrive_18", "arrive_19", "arrive_20", "arrive_21", "arrive_22", 
"arrive_23", "arrive_24"])
async def robot_question(call: types.CallbackQuery):

    # Тебе нравится кино или театр?
    
    if call.data == "answer_cinema" or  call.data == "answer_theatre":
        if call.data == "answer_cinema":
            user_data.append("кино")
        else:
            user_data.append("театр")
        btn1 = InlineKeyboardButton(text="Да", callback_data="history_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="history_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Тебе нравится история?", reply_markup=keyboard_inline)

    # Тебе нравится история?
    
    elif call.data == "history_yes" or  call.data == "history_no":
        if call.data == "history_yes":
            user_data.append("Да")
        else:
            user_data.append("Нет")
        btn1 = InlineKeyboardButton(text="Да", callback_data="vegan_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="vegan_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты вегетарианец?", reply_markup=keyboard_inline)

    # Ты вегетарианец?

    elif call.data == "vegan_yes" or  call.data == "vegan_no":
        if call.data == "vegan_yes":
            user_data.append("Да")
        else:
            user_data.append("Нет")
        btn1 = InlineKeyboardButton(text="Да", callback_data="sugar_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="sugar_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты любишь сладкое?", reply_markup=keyboard_inline)

    # Cколько тебе лет?

    elif call.data == "sugar_yes" or  call.data == "sugar_no":
        if call.data == "sugar_yes":
            user_data.append("Да")
        else:
            user_data.append("Нет")
        btn1 = InlineKeyboardButton(text="Мне 15-25 лет", callback_data="teenage")
        btn2 = InlineKeyboardButton(text="Мне 25-35 лет", callback_data="young")
        btn3 = InlineKeyboardButton(text="Мне 35-45 лет", callback_data="adult")
        btn4 = InlineKeyboardButton(text="Мне 45-55 лет", callback_data="aged")
        btn5 = InlineKeyboardButton(text="Мне 65+ лет", callback_data="ancient")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2, btn3, btn4, btn5)
        await call.message.answer("Сколько тебе лет?", reply_markup=keyboard_inline)
        if call.data == "teenage":
            user_data.append("teenage")
        if call.data == "young":
            user_data.append("young")
        if call.data == "adult":
            user_data.append("adult")
        if call.data == "aged":
            user_data.append("aged")
        if call.data == "ancient":
            user_data.append("ancient")
        text = "Спасибо за ответы, можете переходить к построению маршрута"
        await bot.send_message(chat_id = chat_id, text = text)
"""

executor.start_polling(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)

