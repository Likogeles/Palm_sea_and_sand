import sqlite3

from options import users_db_name


class User:
    # ID пользователя
    __user_id = None
    # Культурность
    __is_culture = 0.5
    # Историчность
    __is_historic = 0.5
    # Религиозность
    __is_religious = 0.5
    # Искусство
    __is_art = 0.5
    # Природность
    __is_natural = 0.5
    # Популярность
    __popularity = 0.5
    # Желаемое время пребывания в точке интереса
    __time = 0.5
    # Пользователь хочет передвигаться пешком
    __is_transport = -1
    # Время прибытия
    __time_arrival = None
    # Время отъезда
    __time_departure = None
    # Место прибытия (широта и долгота)
    __place_arrival_alt = None
    __place_arrival_long = None
    # Место отъезда (широта и долгота)
    __place_departure_alt = None
    __place_departure_long = None
    # Флаг места прибытия
    __place_arrival_flag = False
    # Флаг места отбытия
    __place_departure_flag = False
    # Флаг времени прибытия
    __time_arrival_flag = False
    # Флаг времени отбытия
    __time_departure_flag = False

    def __str__(self):
        return f"{self.__user_id}: {self.__is_culture} {self.__is_historic} " \
               f"{self.__is_religious} {self.__is_art} {self.__is_natural} " \
               f"{self.__popularity} {self.__time} {self.__is_transport} {self.__time_arrival} {self.__time_departure} " \
               f"{self.__place_arrival_alt} {self.__place_arrival_long} {self.__place_departure_alt} {self.__place_departure_long}" \
               f"\n{self.__place_arrival_flag} {self.__place_departure_flag} {self.__time_arrival_flag} {self.__time_departure_flag}\n"

    def __init__(self, user_id):
        '''
        Класс пользователя\n
        :param user_id: Int - ID пользователя в телеграм
        '''
        self.__user_id = int(user_id)

    def set_default(self):
        '''
        Устанавливает исходное значение 0.5 всем весам пользователя (и -1 для транспорта)
        '''
        self.__is_culture = 0.5
        self.__is_historic = 0.5
        self.__is_religious = 0.5
        self.__is_art = 0.5
        self.__is_natural = 0.5
        self.__popularity = 0.5
        self.__time = 0.5
        self.__is_transport = -1
        self.__update_user_in_db()

    def get_place_arrival_flag(self):
        '''
        Возвращает флаг места прибытия\n
        :return: Bool - флаг места прибытия
        '''
        return self.__place_arrival_flag

    def set_place_arrival_flag(self, flag):
        '''
        Устанавливает флаг места прибытия\n
        :param flag: Bool - флаг места прибытия
        '''
        self.__place_arrival_flag = flag
        self.__update_user_in_db()

    def get_place_departure_flag(self):
        '''
        Возвращает флаг места отъезда\n
        :return: Bool - флаг места отъезда
        '''
        return self.__place_departure_flag

    def set_place_departure_flag(self, flag):
        '''
        Устанавливает флаг места отъезда\n
        :param flag: Bool - флаг места отъезда
        '''
        self.__place_departure_flag = flag
        self.__update_user_in_db()

    def get_time_arrival_flag(self):
        '''
        Возвращает флаг времени прибытия\n
        :return: Bool - флаг времени прибытия
        '''
        return self.__time_arrival_flag

    def set_time_arrival_flag(self, flag):
        '''
        Устанавливает флаг времени прибытия\n
        :param flag: Bool - флаг времени прибытия
        '''
        self.__time_arrival_flag = flag
        self.__update_user_in_db()

    def get_time_departure_flag(self):
        '''
        Возвращает флаг времени отъезда\n
        :return: Bool - флаг времени отъезда
        '''
        return self.__time_departure_flag

    def set_time_departure_flag(self, flag):
        '''
        Устанавливает флаг времени отъезда\n
        :param flag: Bool - флаг времени отъезда
        '''
        self.__time_departure_flag = flag
        self.__update_user_in_db()

    def __update_user_in_db(self):
        try:
            con = sqlite3.connect(users_db_name)
            cur = con.cursor()
            cur.execute(f"""
                    UPDATE users
                    SET is_culture = '{str(self.__is_culture)}', is_historic = '{str(self.__is_historic)}',
                    is_religious = '{str(self.__is_religious)}', is_art = '{str(self.__is_art)}',
                    is_natural = '{str(self.__is_natural)}', popularity = '{str(self.__popularity)}',
                    time = '{str(self.__time)}', transport = '{str(self.__is_transport)}',
                    time_arrival = '{str(self.__time_arrival)}', time_departure = '{str(self.__time_departure)}',
                    place_arrival = '{str(self.__place_arrival_alt)} {str(self.__place_arrival_long)}',
                    place_departure = '{str(self.__place_departure_alt)} {str(self.__place_departure_long)}',
                    place_arrival_flag = '{str(self.__place_arrival_flag)}', place_departure_flag = '{str(self.__place_departure_flag)}',
                    time_arrival_flag = '{str(self.__time_arrival_flag)}', time_departure_flag = '{str(self.__time_departure_flag)}'
                    WHERE user_id = {str(self.__user_id)};
                    """)
            con.commit()
            con.close()
        except Exception as ex:
            print("User: update_user_in_db error: " + str(ex))

    def set_user_id(self, user_id):
        '''
        Устанавливает ID пользователя\n
        :param user_id: Int - ID пользователя
        '''
        self.__user_id = user_id
        self.__update_user_in_db()

    def get_user_id(self):
        '''
        Возвращает ID пользователя\n
        :return: Int - ID пользователя
        '''
        return int(self.__user_id or 0)

    def add_culture(self, added_culture_num):
        '''
        Прибавляет значение к культуре\n
        :param added_culture_num: Float - значение, которое необходимо прибавить к культуре
        :return:
        '''
        self.__is_culture += float(added_culture_num)
        self.__update_user_in_db()

    def set_culture(self, is_culture):
        '''
        Устанавливает значение культуры\n
        :param is_culture: Float - параметр культуры
        '''
        self.__is_culture = float(is_culture)
        self.__update_user_in_db()

    def get_culture(self):
        '''
        Возвращает значение культуры\n
        :return: Float - значение культуры
        '''
        return self.__is_culture

    def add_historic(self, added_historic_num):
        '''
        Прибавляет значение к историчности\n
        :param added_historic_num: Float - значение, которое необходимо прибавить к историчности\n
        '''
        self.__is_historic += float(added_historic_num)
        self.__update_user_in_db()

    def set_historic(self, is_historic):
        '''
        Устанавливает значение историчности\n
        :param is_historic: Float - параметр историчности\n
        '''
        self.__is_historic = float(is_historic)
        self.__update_user_in_db()

    def get_historic(self):
        '''
        Возвращает значение историчности\n
        :return: Float - значение историчности\n
        '''
        return self.__is_historic

    def add_religious(self, added_religious_num):
        '''
        Прибавляет значение к религии\n
        :param added_religious_num: Float - значение, которое необходимо прибить к историчности
        '''
        self.__is_religious += float(added_religious_num)
        self.__update_user_in_db()

    def set_religious(self, is_religious):
        '''
        Устанавливает значение религии\n
        :param is_religious: Float - параметр религии
        '''
        self.__is_religious = float(is_religious)
        self.__update_user_in_db()

    def get_religious(self):
        '''
        Возвращает значение религии\n
        :return: Float - значение религии
        '''
        return self.__is_religious

    def add_art(self, added_art_num):
        '''
        Прибаляет значение к искусству\n
        :param added_art_num: Float - значение, которое необходимо прибавить к искусству\n
        '''
        self.__is_art += float(added_art_num)
        self.__update_user_in_db()

    def set_art(self, is_art):
        '''
        Устанавливает значение искусства\n
        :param is_art: Float - параметр искусства
        '''
        self.__is_art = float(is_art)
        self.__update_user_in_db()

    def get_art(self):
        '''
        Возвращает значение искусства\n
        :return: Float - значение искусства
        '''
        return self.__is_art

    def add_natural(self, added_natural_num):
        '''
        Прибавляет значение к природности\n
        :param added_natural_num: Float - значение, которое необходимо прибавить к природности
        :return:
        '''
        self.__is_natural += float(added_natural_num)
        self.__update_user_in_db()

    def set_natural(self, is_natural):
        '''
        Устанавливает значение природности\n
        :param is_natural: Float - параметр природности
        '''
        self.__is_natural = float(is_natural)
        self.__update_user_in_db()

    def get_natural(self):
        '''
        Возвращает значение природности\n
        :return: Float - значение природности
        '''
        return self.__is_natural

    def add_popularity(self, added_popularity_num):
        '''
        Прибавляет значение к популярности\n
        :param added_popularity_num: Float - значение, которое необходимо прибавить к популярности
        '''
        self.__popularity += float(added_popularity_num)
        self.__update_user_in_db()

    def set_popularity(self, popularity):
        '''
        Устанавливает значение популярности\n
        :param popularity: Float - параметр популярности
        '''
        self.__popularity = float(popularity)
        self.__update_user_in_db()

    def get_popularity(self):
        '''
        Возвращает значение популярности\n
        :return: Float - значение популярности
        '''
        return self.__popularity

    def add_time(self, added_time_num):
        '''
        Прибавляет значение к желаемому времени прибывания в точке\n
        :param added_time_num: Float - значение, которое необходимо прибавить к желаемомому времени пребывания в точке
        '''
        self.__time += float(added_time_num)
        self.__update_user_in_db()

    def set_time(self, time):
        '''
        Устанавливает значение желаемого времени пребывания в точке\n
        :param popularity: Float - параметр желаемого времени пребывания в точке
        '''
        self.__time = float(time)
        self.__update_user_in_db()

    def get_time(self):
        '''
        Возвращает значение желаемого времени пребывания в точке\n
        :return: Float - значение желаемого времени пребывания в точке
        '''
        return self.__time

    def set_transport(self, transport):
        '''
        Устанавливает значение желания пользователя передвигаться на транспорте\n
        -1: Пешком (автоматически)\n
        1: На автобусе\n
        :param transport: Int - параметр желания пользователя передвигаться на транспорте
        '''
        self.__is_transport = int(transport)
        self.__update_user_in_db()

    def get_transport(self):
        '''
        Возвращает значение желания пользователя передвигаться на транспорте\n
        -1: Пешком (автоматически)\n
        1: На автобусе\n
        :return: Int - значение желания пользователя передвигаться на транспорте
        '''
        return self.__is_transport

    def set_time_arrival(self, time_arrival):
        '''
        Устанавливает значение времени прибытия\n
        :param time_arrival: String - значение времени прибытия
        '''
        self.__time_arrival = time_arrival
        self.__update_user_in_db()

    def get_time_arrival(self):
        '''
        Возвращает значение времени прибытия\n
        :return: String - значение времени прибытия
        '''
        return self.__time_arrival

    def set_time_departure(self, time_departure):
        '''
        Устанавливает значение времени прибытия\n
        :param time_departure: String - значение времени прибытия
        '''
        self.__time_departure = time_departure
        self.__update_user_in_db()

    def get_time_departure(self):
        '''
        Возвращает значение времени отъезда\n
        :return: String - значение времени отъезда
        '''
        return self.__time_departure

    def set_place_arrival(self, place_arrival):
        '''
        Устанавливает значение места прибытия\n
        :param place: (Float, Float) - значение места прибытия
        '''
        self.__place_arrival_alt = place_arrival[0]
        self.__place_arrival_long = place_arrival[1]
        self.__update_user_in_db()

    def get_place_arrival(self):
        '''
        Возвращает значение места прибытия\n
        :return: (Float, Float) - значение места прибытия
        '''
        return self.__place_arrival_alt, self.__place_arrival_long

    def set_place_departure(self, place_departure):
        '''
        Устанавливает значение места отъезда\n
        :param place: (Float, Float) - значение места отъезда
        '''
        self.__place_departure_alt = place_departure[0]
        self.__place_departure_long = place_departure[1]
        self.__update_user_in_db()

    def get_place_departure(self):
        '''
        Возвращает значение места отъезда\n
        :return: (Float, Float) - значение места отъезда
        '''
        return self.__place_departure_alt, self.__place_departure_long