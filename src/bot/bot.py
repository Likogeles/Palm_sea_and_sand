import logging
import re
import json
from UsersDB.User import User

from os import environ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from UsersDB.UserList import UserList

API_TOKEN = environ.get('API_TOKEN')
bot = Bot(API_TOKEN)

# Configure logging
logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher
bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)
# Addiing user_data, keyboard with different time and flag for location tracking

user_data = []
kb = [
    [types.KeyboardButton(text="0:00"),
     types.KeyboardButton(text="12:00")],
    [types.KeyboardButton(text="1:00"),
     types.KeyboardButton(text="13:00")],
    [types.KeyboardButton(text="2:00"),
     types.KeyboardButton(text="14:00")],
    [types.KeyboardButton(text="3:00"),
     types.KeyboardButton(text="15:00")],
    [types.KeyboardButton(text="4:00"),
     types.KeyboardButton(text="16:00")],
    [types.KeyboardButton(text="5:00"),
     types.KeyboardButton(text="17:00")],
    [types.KeyboardButton(text="6:00"),
     types.KeyboardButton(text="18:00")],
    [types.KeyboardButton(text="7:00"),
     types.KeyboardButton(text="19:00")],
    [types.KeyboardButton(text="8:00"),
     types.KeyboardButton(text="20:00")],
    [types.KeyboardButton(text="9:00"),
     types.KeyboardButton(text="21:00")],
    [types.KeyboardButton(text="10:00"),
     types.KeyboardButton(text="22:00")],
    [types.KeyboardButton(text="11:00"),
     types.KeyboardButton(text="23:00")],
]
keyboard = types.ReplyKeyboardMarkup(
    keyboard=kb,
    resize_keyboard=True,
)
flag = False

# STARTING POINT
userList = UserList()
@dp.message_handler(commands=['start', 'help'])
async def send_welcome(message: types.Message):
    userList.add_user(message.from_user.id)
    keyb = [
        [
            types.KeyboardButton(text="Маршрут"),
            types.KeyboardButton(text="Анкета")
        ],
    ]
    keyboard = types.ReplyKeyboardMarkup(
        keyboard=keyb,
        resize_keyboard=True,
        input_field_placeholder="Выберите, что вы хотите"
    )
    await message.reply("Привет!\nЯ бот, который поможет проложить маршрут", reply_markup=keyboard)
    await bot.send_sticker(message.from_user.id, sticker = "CAACAgIAAxkBAAEJwlpkun7HJX19BUAerEIc3G7jVD4RjgACrRgAAnmFiUi3haSlMSLa5S8E")


# АНКЕТА

@dp.message_handler(text=["Маршрут"])
async def geolocation(message: types.Message):
    await message.answer("Введите адрес пребывания или отправьте геопозицию", reply_markup=types.ReplyKeyboardRemove())

@dp.message_handler(content_types=['location'])
async def handle_loc(message):
    lat = message.location['latitude']
    lon = message.location['longitude']
    user.__place = (lat, lon)
    print(user.__place)

@dp.message_handler(text=["Лоооол"])
async def arrival_time(message: types.Message):
    await message.answer("Когда вы прибываете в город?", reply_markup=keyboard)

@dp.message_handler()
async def message_accept(message: types.Message):

    # putting arrival time in user's data

    result = re.fullmatch(r'\d{1,2}:\d\d', message.text)
    if result:
        user_data.append(message.text)
        message.reply("")
    await bot.send_message(message.from_user.id, message.text)
    
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
    await bot.send_sticker(message.from_user.id,
                           sticker="CAACAgIAAxkBAAEJwlpkun7HJX19BUAerEIc3G7jVD4RjgACrRgAAnmFiUi3haSlMSLa5S8E")

@dp.message_handler(text=["Анкета"])
async def start_form(message: types.Message):
    btn_prior_1 = InlineKeyboardButton(text="Кино", callback_data="prior_cinema")
    btn_prior_2 = InlineKeyboardButton(text="Театр", callback_data="prior_theatre")
    btn_prior_3 = InlineKeyboardButton(text="Музей", callback_data="prior_museum")
    btn_prior_4 = InlineKeyboardButton(text="Бар", callback_data="prior_bar")
    btn_prior_5 = InlineKeyboardButton(text="Клуб", callback_data="prior_club")
    keyboard_inline = InlineKeyboardMarkup()
    keyboard_inline.add(btn_prior_1)
    keyboard_inline.add(btn_prior_2)
    keyboard_inline.add(btn_prior_3)
    keyboard_inline.add(btn_prior_4)
    keyboard_inline.add(btn_prior_5)
    await message.answer("Выбери в порядке приоритета:", reply_markup=keyboard_inline)

arr_answer = []


@dp.callback_query_handler(text=["prior_cinema", "prior_theatre", "prior_museum", "prior_bar", "prior_club"])
async def track_question(call: types.CallbackQuery):
    if call.data == "prior_cinema" or call.data == "prior_theatre" or call.data == "prior_museum" or call.data == "prior_bar" or call.data == "prior_club":
        if len(arr_answer) < 5:
            arr_answer.append(call.data)
            if len(arr_answer) == 5:
                await call.message.answer("Итоговый приоритет: " + str(arr_answer))
            else:
                await call.message.answer("В порядке приоритета: " + str(arr_answer))


@dp.callback_query_handler(
    text=["history_yes", "history_no", "vegan_yes", "vegan_no", "sugar_yes",
          "sugar_no", "teenage", "young", "adult", "aged", "ancient", "answer_bar", "answer_club", "avto", "hiking",
        "activ_yes", "activ_no", "art_yes", "art_no",  ])
async def resume_question(call: types.CallbackQuery):
    print(call.data)
    # Тебе нравится кино или театр?

    if call.data == "history_yes" or call.data == "history_no":
        #if call.data == "answer_cinema":
         #   user_data.append("кино")
        #else:
         #   user_data.append("театр")
        btn1 = InlineKeyboardButton(text="Да", callback_data="history_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="history_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Тебе нравится история?", reply_markup=keyboard_inline)

    # Тебе нравится история?

    #elif call.data == "history_yes" or call.data == "history_no":
        if call.data == "history_yes":
            user_data.append("Да")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(0.3)
            user.add_culture(0.2)
            user.add_religious(0.1)
            user.add_popularity(0.1)
            user.add_time(-0.1)
        else:
            user_data.append("Нет")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.1)
            user.add_culture(-0.2)
            user.add_religious(-0.1)
            user.add_popularity(-0.1)
            user.add_time(0.1)
        btn1 = InlineKeyboardButton(text="Мне 15-35 лет", callback_data="teenage")
        btn2 = InlineKeyboardButton(text="Мне 35-35 лет", callback_data="young")
        btn3 = InlineKeyboardButton(text="Мне 55 и более", callback_data="adult")
        keyboard_inline = InlineKeyboardMarkup()
        keyboard_inline.add(btn1)
        keyboard_inline.add(btn2)
        keyboard_inline.add(btn3)
        await call.message.answer("Сколько тебе лет?", reply_markup=keyboard_inline)

    if call.data == "teenage" or call.data == "young" or call.data == "adult":
        if call.data == "teenage":
            user_data.append("teenage")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_religious(-0.2)
            user.add_popularity(0.3)
            user.add_natural(0.1)
            user.add_time(0.3)
        elif call.data == "young":
            user_data.append("young")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_popularity(0.2)
            user.add_time(0.2)
        elif call.data == "adult":
            user_data.append("adult")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_religious(0.2)
            user.add_popularity(-0.1)
            user.add_natural(-0.1)
            user.add_time(-0.2)

        btn1 = InlineKeyboardButton(text="Да", callback_data="activ_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="activ_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты любишь активный отдых?", reply_markup=keyboard_inline)


     # Ты любишь искусство

    elif call.data == "activ_yes" or call.data == "activ_no":
        if call.data == "activ_yes":
            user_data.append("Да")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_natural(0.3)
            user.add_time(0.3)
        else:
            user_data.append("Нет")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.1)
            user.add_art(0.1)
            user.add_natural(-0.3)
            user.add_time(-0.2)
        btn1 = InlineKeyboardButton(text="Да", callback_data="art_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="art_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты любишь искусство?", reply_markup=keyboard_inline)
    #Ты любишь активный отдых?

    elif call.data == "art_yes" or call.data == "art_no":
        if call.data == "art_yes":
            user_data.append("Да")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_culture(0.2)
            user.add_art(0.3)
            user.add_natural(-0.2)
            user.add_popularity(0.2)
            user.add_time(0.2)
        else:
            user_data.append("Нет")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.1)
            user.add_culture(-0.1)
            user.add_religious(0.1)
            user.add_art(-0.3)
            user.add_natural(0.3)
            user.add_popularity(-0.2)
            user.add_time(-0.1)
        btn1 = InlineKeyboardButton(text="На транспорте", callback_data="avto")
        btn2 = InlineKeyboardButton(text="Пешком", callback_data="hiking")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Как ты любишь передвигаться по городу?", reply_markup=keyboard_inline)

    #Ты выберешь отдых на природе или в городе

    elif call.data == "avto" or call.data == "hiking":
        if call.data == "avto":
            user_data.append("На авто :)")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.2)
            user.add_religious(-0.1)
            user.add_art(0.2)
            user.add_natural(-0.2)
            user.add_time(-0.2)
        else:
            user_data.append("Пешком")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_historic(0.2)
            user.add_religious(0.1)
            user.add_art(-0.1)
            user.add_natural(0.3)
            user.add_popularity(-0.2)
            user.add_time(0.3)
        btn1 = InlineKeyboardButton(text="Авантюрный", callback_data="advanture")
        btn2 = InlineKeyboardButton(text="Спокойный", callback_data="calm")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты авантюрный или спокойный", reply_markup=keyboard_inline)

    #Ты авантюрный или спокойный

    elif call.data == "advanture" or call.data == "calm":
        if call.data == "advanture":
            user_data.append("Авантюрный")
            user_data.append("Авантюрный")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_religious(-0.3)
            user.add_natural(-0.2)
            user.add_popularity(0.3)
            user.add_time(-0.2)
        else:
            user_data.append("Спокойный")
            user = UserList.get_user_by_id(call.from_user.id)
            user.add_religious(0.2)
            user.add_natural(0.2)
            user.add_time(0.3)
        await call.message.answer("Спасибо, можете переходить к составлению маршрута")
    print(user)
if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)