# <p  align="center">Гид Том — бот для путешественников</p>

<p align="center">
<img src="https://cdn.discordapp.com/attachments/883024812950323210/1133522975413506158/tom.png" alt="GuideTomeImage" width="200"/>
</p>

---

## 📋 Оглавление
1) [Описание проекта](#descriptoin)
2) [Используемые технологии](#using_techs)
3) [Используемые библиотеки](#libraries)
4) [База данных объектов](#data_base)
5) [Запуск проекта](#launch)
6) [Структура проекта](#project_structure)
7) [Работа алгоритма](#algorithm_work)

---

## ❗️ <a name="descriptoin">📱 Описание проекта</a>
Наш бот **Том** поможет путешественникам сформировать собственный уникальный маршрут исходя из их собственных предпочтений.
* Попробовать можно по [ссылке](https://t.me/GuideTomBot) (может быть временно отключен)
* Наш [сайт](https://t.me/GuideTomBot)
* [Менеджер проекта](https://t.me/lirik_man_73)
* [Главный разработчик](https://t.me/rare_action)

---

## ❗️ <a name="using_techs">👨‍💻 Используемые технологии</a>
- **🤖 Алгоритм кластеризации** - используется разбиения Базы Данных объектов на соответствующие кластеры.
>Разделение на кластеры необходимо для более быстрого поиска необходимых конкретному опльзователь объектов.*
- **🤖 Генетический алгоритм** - используется для формирования маршрута пользователя.
>Объектов на карте огромное количество и просчитывать все возможные маршуруты слишком трудоёмко.
- **🤖 Машинное обучение (sklearn, numpy, pandas)** - используется для машинного обучения.
>Необходимо для ...
- **Отрисовка карт (osmnx)** - используется для визуального отображения маршрута пользователя.
>Текстовый интерфейс - это меньшее что мы можем предложить.
- **SQL** - Работа с базой данных.
>База данных пользователей и объетов имеет простую, классическую, табличную структуру.
- **Telegram Bot API** - используется для взаимодействия пользователя и приложения.
>Один из самых простых и быстрых в разработке современных интерфейсов

---

## <a name="libraries">🔨 Используемые библиотеки</a>
- **aiogram** - работа с ботами в Telegram.
- **sklearn** - машинное обучение.
- **osmnx** - работа с картой.
- **numpy** - многомерные массивы и их высокоуровневые математические функции.
- **pandas** - обработка и анализа данных.
- **sqlite3** - работа с Базами Данных.

---

## ❗️ <a name="data_base">💼 База данных объектов (опционально, можно добавить ссылки на датасеты)</a>
База данных сформирована из открытых источников и использует в себе открытую информацию

---

## ❗️ <a name="launch">⚙️ Запуск проекта</a>
1) Скачать репозиторий.
2) Установить python и необходимые библиотеки.
3) Указать API-ключ бота в Telegram.
4) Запустить файл main<span></span>.py.
<!-- Span установлен, чтобы название файла не отображалось гиперссылкой -->
```console
pip install aiogram
и прочие
Тут можно указать консольный ввод
```

---

## ❗️ <a name="project_structure">👷 Структура проекта</a>
- **data** - Содержит в себе базы данных пользователей и точек интереса.
- **src.bot** - Модуль для работы с ботом.
- **src.PlaceDB** - Модуль для обработки и хранения информации о точках интереса.
- **src.UsersDB** - Модуль для обработки и хранения пользовательских данных.
- **src.processing** - Модуль, содержащий в себе основные алгоритмы парсинга, Кластеризации и Генетического алгоритма.
- **src.main<span></span>.py** - Файл запуска проекта.
- **src.options<span></span>.py** - Хранит в себе константные названия файлов проекта.

---

## ❗️ <a name="algorithm_work">🤖 Работа алгоритма</a>

Тут нужно добавить описание того, как работает алгоритм (можно с картинками 😉)

1) У точек интереса, как и у пользователей, есть веса опрелелённого типа: *культурность*, *историчность*, *религиозность* и пр.
>У пользователя веса формируются с помощью заполнения анкеты. У точек интереса - при кластеризации.

2) Когда пользователь отправляет запрос на составление маршрута, генетический алгоритм запускает несколько поколений особей пользователей, которые проходят случайные (но сформированные по шаблону) маршруты.

3) Каждый найденный маршрут оценивается исходя из потребностей пользователя и найденых точек интереса. Например, *культурность* пользователя умножается на *культурность* точки. Полученное значение будет использовано при выборе особей для продолжения рода и создания новых поколений.

4) Через несколько поколений будет найден и отображён пользователю тот самый, уникальный для него, маршрут.

---

# ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ ❗️ 
1. Readme-файл, должен быть грамотно структурирован (используются заголовки, абзацы) и содержать 3 раздела:

+ а. Описание проекта (2-4 предложения) - первый заголовок;
+ б. Описание применяемых технологий, моделей, алгоритмов - второй заголовок;
+ в. Описание использованных датасетов и ссылки на них (при необходимости) - третий заголовок;
+ г. Подробная инструкция, как запустить проект - четвертый заголовок.
+ д. Описание структуры проекта (что какая папка за что отвечает) - пятый заголовок.