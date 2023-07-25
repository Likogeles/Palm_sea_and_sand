import logging
import re

from os import environ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from UsersDB.UserList import UserList

API_TOKEN = "XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX"
bot = Bot(API_TOKEN)

# Configure logging

logging.basicConfig(level=logging.INFO)

# Initialize bot and dispatcher

bot = Bot(token=API_TOKEN)
dp = Dispatcher(bot)

# Addiing keyboard with different time and flag for location tracking

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

# STARTING POINT

userList = UserList()
print(*userList.get_all_users())


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

# Маршрут


@dp.message_handler(text=["Маршрут"])
async def geolocation(message: types.Message):
    userList.set_user_flag(message.from_user.id, 'place_arrival_flag', True)
    await message.answer("Введите адрес прибывания или отправьте геопозицию", reply_markup=types.ReplyKeyboardRemove())


@dp.message_handler(content_types=['location'])
async def handle_loc(message):
    lat = message.location['latitude']
    lon = message.location['longitude']
    user = userList.get_user_by_id(message.from_user.id)
    if userList.get_user_flag(message.from_user.id, 'place_arrival_flag'):
        user.set_place_arrival((lat, lon))
        userList.set_user_flag(message.from_user.id, 'place_arrival_flag', False)

        userList.set_user_flag(message.from_user.id, 'time_arrival_flag', True)
        await message.answer("Во сколько вы прибываете?", reply_markup=keyboard)
    if userList.get_user_flag(message.from_user.id, 'place_departure_flag'):
        user.set_place_departure((lat, lon))
        userList.set_user_flag(message.from_user.id, 'place_departure_flag', False)

        userList.set_user_flag(message.from_user.id, 'time_departure_flag', True)
        await message.answer("Во сколько уезжаете?", reply_markup=keyboard)


@dp.message_handler()
async def message_accept(message: types.Message):
    if message.text == "Анкета":
        btn1 = InlineKeyboardButton(text="Да", callback_data="history_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="history_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await message.answer("Хорошо, тогда начнем опрос", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Тебе нравится история?", reply_markup=keyboard_inline)
    elif userList.get_user_flag(message.from_user.id, 'place_arrival_flag') or userList.get_user_flag(message.from_user.id, 'place_departure_flag'):
        # Место для кода получения координаты из адреса
        lat = 38.939715
        lon = 46.207076
        user = userList.get_user_by_id(message.from_user.id)
        if userList.get_user_flag(message.from_user.id, 'place_arrival_flag'):
            user.set_place_arrival((lat, lon))

            userList.set_user_flag(message.from_user.id, 'time_arrival_flag', True)

            await message.answer("Во сколько вы прибываете?", reply_markup=keyboard)
        elif userList.get_user_flag(message.from_user.id, 'place_departure_flag'):
            user.set_place_departure((lat, lon))

            userList.set_user_flag(message.from_user.id, 'time_departure_flag', True)
            await message.answer("Во сколько уезжаете?", reply_markup=keyboard)
        userList.set_user_flag(message.from_user.id, 'place_arrival_flag', False)
        userList.set_user_flag(message.from_user.id, 'place_departure_flag', False)

    elif userList.get_user_flag(message.from_user.id, 'time_arrival_flag') or userList.get_user_flag(message.from_user.id, 'time_departure_flag'):
        result = re.fullmatch(r'\d{1,2}:\d\d', message.text)
        if result:
            user = userList.get_user_by_id(message.from_user.id)
            if userList.get_user_flag(message.from_user.id, 'time_arrival_flag'):
                user.set_time_arrival(message.text)
                userList.set_user_flag(message.from_user.id, 'time_arrival_flag', False)
                userList.set_user_flag(message.from_user.id, 'place_departure_flag', True)
                await message.answer("Введите адрес отбытия или отправьте геопозицию", reply_markup=types.ReplyKeyboardRemove())
            if userList.get_user_flag(message.from_user.id, 'time_departure_flag'):
                user.set_time_departure(message.text)
                userList.set_user_flag(message.from_user.id, 'time_departure_flag', False)
                await message.answer("Отлично!", reply_markup=types.ReplyKeyboardRemove())
        else:
            await message.answer("Время введено в неправильном формате")
    # print(userList.get_user_by_id(message.from_user.id))


# Анкета
"""

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

@dp.message_handler(text=["Анкета"])
async def start_form(message: types.Message):
    btn1 = InlineKeyboardButton(text="Да", callback_data="history_yes")
    btn2 = InlineKeyboardButton(text="Нет", callback_data="history_no")
    keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
    await message.answer("Хорошо, тогда начнем опрос", reply_markup=types.ReplyKeyboardRemove())
    await message.answer("Тебе нравится история?", reply_markup=keyboard_inline)
"""

@dp.callback_query_handler(
    text=["history_yes", "history_no", "vegan_yes", "vegan_no", "sugar_yes",
          "sugar_no", "teenage", "young", "adult", "aged", "ancient", "answer_bar", "answer_club", "avto", "hiking",
        "activ_yes", "activ_no", "art_yes", "art_no", "advanture", "calm"])
async def resume_question(call: types.CallbackQuery):

    # Тебе нравится история?

    #elif call.data == "history_yes" or call.data == "history_no":
    if call.data == "history_yes" or call.data == "history_no":
        if call.data == "history_yes":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.3)
            user.add_culture(0.2)
            user.add_religious(0.1)
            user.add_popularity(0.1)
            user.add_time(-0.1)
        else:
            user = userList.get_user_by_id(call.from_user.id)
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
            user = userList.get_user_by_id(call.from_user.id)
            user.add_religious(-0.2)
            user.add_popularity(0.3)
            user.add_natural(0.1)
            user.add_time(0.3)
        elif call.data == "young":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_popularity(0.2)
            user.add_time(0.2)
        elif call.data == "adult":
            user = userList.get_user_by_id(call.from_user.id)
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
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_natural(0.3)
            user.add_time(0.3)
        else:
            user = userList.get_user_by_id(call.from_user.id)
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
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_culture(0.2)
            user.add_art(0.3)
            user.add_natural(-0.2)
            user.add_popularity(0.2)
            user.add_time(0.2)
        else:
            user = userList.get_user_by_id(call.from_user.id)
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
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.2)
            user.add_religious(-0.1)
            user.add_art(0.2)
            user.add_natural(-0.2)
            user.add_time(-0.2)
        else:
            user = userList.get_user_by_id(call.from_user.id)
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
            user = userList.get_user_by_id(call.from_user.id)
            user.add_religious(-0.3)
            user.add_natural(-0.2)
            user.add_popularity(0.3)
            user.add_time(-0.2)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_religious(0.2)
            user.add_natural(0.2)
            user.add_time(0.3)
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
        await call.message.answer("Спасибо, можете переходить к составлению маршрута", reply_markup=keyboard)

executor.start_polling(dp)

if __name__ == '__main__':
    executor.start_polling(dp, skip_updates=True)