import logging
import re
import osmnx.geocoder as gc
import processing.parser as pr
import processing.model as md

import json
from UsersDB.User import User


from os import environ

from aiogram import Bot, Dispatcher, executor, types
from aiogram.types import ReplyKeyboardMarkup, ReplyKeyboardRemove, KeyboardButton
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


from PlacesDB.PlaceList import PlaceList
from UsersDB.UserList import UserList

API_TOKEN = environ.get('API_TOKEN')
bot = Bot(API_TOKEN)
msg = "Нажмите *_Маршрут_*, чтобы сформировать маршрут\nНажмите *_Анкета_*, чтобы я мог понять ваши препочтения"

main_keyboard = types.ReplyKeyboardMarkup(
    keyboard= [
        [
            types.KeyboardButton(text="Маршрут"),
            types.KeyboardButton(text="Анкета")
        ],
    ],
    resize_keyboard=True,
    input_field_placeholder="Выберите, что вы хотите"
)

time_keyboard = InlineKeyboardMarkup()
time_keyboard.add(InlineKeyboardButton(text="В начале путешествия", callback_data="early"))
time_keyboard.add(InlineKeyboardButton(text="В середине", callback_data="in_a_way"))
time_keyboard.add(InlineKeyboardButton(text="В конце", callback_data="late"))
time_keyboard.add(InlineKeyboardButton(text="Не имеет значения", callback_data="any_time"))
time_keyboard.add(InlineKeyboardButton(text="Я не хочу посещать", callback_data="off"))

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
placeList = PlaceList()
print(*userList.get_all_users())

@dp.message_handler(commands=['start', 'help', 'add_param'])
async def send_welcome(message: types.Message):
    if message.get_command() == '/add_param':
        keyboard_inline = InlineKeyboardMarkup().add(InlineKeyboardButton(text="Да", callback_data="addit_yes"),
                                                 InlineKeyboardButton(text="Нет", callback_data="addit_no"))
        await message.answer("Чтобы подобрать маршрут персонально под вас, необходимо ответить еще на несколько простых вопросов", reply_markup=types.ReplyKeyboardRemove())
        await message.answer("Начнем?", reply_markup=keyboard_inline)
        return
    userList.add_user(message.from_user.id)
    await message.reply("Привет\!\nЯ бот, который поможет проложить маршрут\n\n" + msg, reply_markup=main_keyboard, parse_mode='MarkdownV2')
    await bot.send_sticker(message.from_user.id, sticker = "CAACAgIAAxkBAAEJwlpkun7HJX19BUAerEIc3G7jVD4RjgACrRgAAnmFiUi3haSlMSLa5S8E")

@dp.message_handler(text=["Маршрут"])
async def geolocation(message: types.Message):
    userList.set_user_flag(message.from_user.id, 'place_arrival_flag', True)
    await message.answer("Введите адрес прибытия или отправьте геопозицию", reply_markup=types.ReplyKeyboardRemove())

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
        try:
            lat, lon = gc.geocode(message.text)
        except ValueError:
            await message.answer("Место не найдено:(\nПопробуйте ввести место иначе")
            return
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

                # РАССЧЕТ МОДЕЛИ             
                await message.answer("Подождите, я рассчитываю маршрут...", reply_markup=types.ReplyKeyboardRemove())
                data = pr.get_raw_data(pr.tags, ['Москва'])
                normalized = pr.get_normilized(data)
                knn = md.get_knn(user.get_vector(), normalized.values, 5)
                await message.answer(str(knn))

                # МЕСТО ДЛЯ ГЕНЕТИЧЕСКОГО АЛГОРИТМА

                await message.answer(msg, reply_markup=main_keyboard, parse_mode='MarkdownV2')
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
            user.add_historic(0.2)
            user.add_culture(0.1)
            user.add_religious(0.05)
            user.add_popularity(0.1)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_culture(-0.23)
            user.add_historic(-0.13)
            user.add_religious(-0.1)
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
            user.add_historic(-0.1)
            user.add_culture(-0.1)
            user.add_religious(-0.16)
            user.add_popularity(-0.05)
            user.add_natural(0.05)
        elif call.data == "young":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_popularity(-0.2)
            user.add_popularity(0.08)
            user.add_time(0.12)
        elif call.data == "adult":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.05)
            user.add_culture(0.05)
            user.add_religious(0.13)
            user.add_popularity(-0.07)
            user.add_time(0.22)

        btn1 = InlineKeyboardButton(text="Да", callback_data="activ_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="activ_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты любишь активный отдых?", reply_markup=keyboard_inline)


     # Ты любишь искусство

    elif call.data == "activ_yes" or call.data == "activ_no":
        if call.data == "activ_yes":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.07)
            user.add_natural(0.05)
            user.add_time(-0.2)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(-0.1)
            user.add_art(0.15)
            user.add_time(0.12)
        btn1 = InlineKeyboardButton(text="Да", callback_data="art_yes")
        btn2 = InlineKeyboardButton(text="Нет", callback_data="art_no")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты любишь искусство?", reply_markup=keyboard_inline)
    #Ты любишь активный отдых?

    elif call.data == "art_yes" or call.data == "art_no":
        if call.data == "art_yes":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_culture(0.05)
            user.add_art(0.1)
            user.add_natural(-0.13)
            user.add_popularity(0.1)
            user.add_time(0.1)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_art(-0.15)
            user.add_natural(0.13)
            user = userList.get_user_by_id(call.from_user.id)
        
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
            user.add_time(0.1)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_historic(0.1)
            user.add_religious(0.1)
            user.add_art(-0.1)
            user.add_natural(0.12)
            user.add_popularity(-0.15)
            user.add_time(-0.1)
        btn1 = InlineKeyboardButton(text="Авантюрный", callback_data="advanture")
        btn2 = InlineKeyboardButton(text="Спокойный", callback_data="calm")
        keyboard_inline = InlineKeyboardMarkup().add(btn1, btn2)
        await call.message.answer("Ты авантюрный или спокойный", reply_markup=keyboard_inline)

    #Ты авантюрный или спокойный

    elif call.data == "advanture" or call.data == "calm":
        if call.data == "advanture":
            user = userList.get_user_by_id(call.from_user.id)
            user.add_religious(-0.03)
            user.add_natural(-0.02)
            user.add_popularity(0.03)
            user.add_time(-0.05)
        else:
            user = userList.get_user_by_id(call.from_user.id)
            user.add_religious(0.02)
            user.add_natural(0.02)
            user.add_time(0.03)
        await call.message.answer(str(user.get_vector()))
        await call.message.answer("Спасибо, можете переходить к составлению маршрута", reply_markup=main_keyboard)

@dp.callback_query_handler(text=["addit_yes", "addit_no"])
async def addit_opinion(call: types.CallbackQuery):
    if call.data == "addit_yes":
        await call.message.answer("В какой момент времени вы бы хотели посетить _объекты светской культуры_?", reply_markup=time_keyboard, parse_mode='MarkdownV2')
    else:
        await call.message.answer(msg, reply_markup=main_keyboard, parse_mode='MarkdownV2')

@dp.callback_query_handler(text=['early','in_a_way','late','any_time','off'])
async def addit_opinion(call: types.CallbackQuery):
    user = userList.get_user_by_id(call.from_user.id)
    msg_obj = ""
    match len(user.get_time_vector()):
        case 0:
            user.add_time_vector_value(call.data)
            msg_obj += 'исторически важные объекты'
        case 1:
            user.add_time_vector_value(call.data)
            msg_obj += 'религиозные объекты'
        case 2:
            user.add_time_vector_value(call.data)
            msg_obj += 'выставки или галереи'
        case 3:
            user.add_time_vector_value(call.data)
            msg_obj += 'парки'
        case 4:
            user.add_time_vector_value(call.data)
            msg_obj += 'кафе или ресторан'
        case 5:
            user.add_time_vector_value(call.data)
            await call.message.answer("Спасибо\! Ваш маршрут будет скорректирован\n\n" + msg, reply_markup=main_keyboard, parse_mode='MarkdownV2')
            return
            
        case _:
            msg_obj += 'ERROR'
    await call.message.answer(f"В какой момент времени вы бы хотели посетить _{msg_obj}_?", reply_markup=time_keyboard, parse_mode='MarkdownV2')

def start():
    executor.start_polling(dp, skip_updates=True)