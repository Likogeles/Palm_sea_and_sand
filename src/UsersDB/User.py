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
    # Время прибытия
    __time_arrival = None
    # Время отъезда
    __time_departure = None
    # Место прибытия
    __place_arrival = None
    # Место отъезда
    __place_departure = None

    def __str__(self):
        pre_name = "ID\t\t\tculture\thistory\treligy\tart\t\tnature\tpopular\ttime\ttime_arrival\ttime_departure" \
                   "\tplace_arrival\tplace_departure\n"
        return pre_name + f"{self.__user_id}:\t\t{self.__is_culture}\t\t{self.__is_historic}\t\t" \
               f"{self.__is_religious}\t\t{self.__is_art}\t\t{self.__is_natural}\t\t" \
               f"{self.__popularity}\t\t{self.__time}\t\t{self.__time_arrival}\t{self.__time_departure}\t" \
               f"{self.__place_arrival}\t{self.__place_departure}"

    def __init__(self, user_id):
        '''
        Класс пользователя
        :param user_id: Int - ID пользователя в телеграм
        '''
        self.__user_id = int(user_id)

    def __update_user_in_db(self):
        try:
            con = sqlite3.connect(users_db_name)
            cur = con.cursor()
            cur.execute(f"""
                    UPDATE users
                    SET is_culture = '{str(self.__is_culture)}', is_historic = '{str(self.__is_historic)}',
                    is_religious = '{str(self.__is_religious)}', is_art = '{str(self.__is_art)}', is_natural =
                    '{str(self.__is_natural)}', popularity = '{str(self.__popularity)}', time = '{str(self.__time)}'
                    , time_arrival = '{str(self.__time_arrival)}', time_departure = '{str(self.__time_departure)}',
                    place_arrival = '{str(self.__place_arrival)}', place_departure = '{str(self.__place_departure)}'
                    WHERE user_id = {str(self.__user_id)};
                    """)
            con.commit()
            con.close()
        except Exception as ex:
            print("User: update_user_in_db error: " + str(ex))

    def set_user_id(self, user_id):
        '''
        Устанавливает ID пользователя
        :param user_id: Int - ID пользователя
        '''
        self.__user_id = user_id
        self.__update_user_in_db()

    def get_user_id(self):
        '''
        Возвращает ID пользователя
        :return: Int - ID пользователя
        '''
        return int(self.__user_id or 0)

    def add_culture(self, added_culture_num):
        self.__is_culture += float(added_culture_num)
        self.__update_user_in_db()

    def set_culture(self, is_culture):
        '''
        Устанавливает значение культуры
        :param is_culture: Float - параметр культуры
        '''
        self.__is_culture = float(is_culture)
        self.__update_user_in_db()

    def get_culture(self):
        '''
        Возвращает значение культуры
        :return: Float - значение культуры
        '''
        return self.__is_culture

    def add_historic(self, added_historic_num):
        self.__is_historic += float(added_historic_num)
        self.__update_user_in_db()

    def set_historic(self, is_historic):
        '''
        Устанавливает значение историчности
        :param is_historic: Float - параметр историчности
        '''
        self.__is_historic = float(is_historic)
        self.__update_user_in_db()

    def get_historic(self):
        '''
        Возвращает значение историчности
        :return: Float - значение историчности
        '''
        return self.__is_historic

    def add_religious(self, added_religious_num):
        self.__is_religious += float(added_religious_num)
        self.__update_user_in_db()

    def set_religious(self, is_religious):
        '''
        Устанавливает значение религии
        :param is_religious: Float - параметр религии
        '''
        self.__is_religious = float(is_religious)
        self.__update_user_in_db()

    def get_religious(self):
        '''
        Возвращает значение религии
        :return: Float - значение религии
        '''
        return self.__is_religious

    def add_art(self, added_art_num):
        self.__is_art += float(added_art_num)
        self.__update_user_in_db()

    def set_art(self, is_art):
        '''
        Устанавливает значение искусства
        :param is_art: Float - параметр искусства
        '''
        self.__is_art = float(is_art)
        self.__update_user_in_db()

    def get_art(self):
        '''
        Возвращает значение искусства
        :return: Float - значение искусства
        '''
        return self.__is_art

    def add_natural(self, added_natural_num):
        self.__is_natural += float(added_natural_num)
        self.__update_user_in_db()

    def set_natural(self, is_natural):
        '''
        Устанавливает значение природности
        :param is_natural: Float - параметр природности
        '''
        self.__is_natural = float(is_natural)
        self.__update_user_in_db()

    def get_natural(self):
        '''
        Возвращает значение природности
        :return: Float - значение природности
        '''
        return self.__is_natural

    def add_popularity(self, added_popularity_num):
        self.__popularity += float(added_popularity_num)
        self.__update_user_in_db()

    def set_popularity(self, popularity):
        '''
        Устанавливает значение популярности
        :param popularity: Float - параметр популярности
        '''
        self.__popularity = float(popularity)
        self.__update_user_in_db()

    def get_popularity(self):
        '''
        Возвращает значение популярности
        :return: Float - значение популярности
        '''
        return self.__popularity

    def add_time(self, added_time_num):
        self.__time += float(added_time_num)
        self.__update_user_in_db()

    def set_time(self, time):
        '''
        Устанавливает значение желаемого времени пребывания в точке
        :param popularity: Float - параметр желаемого времени пребывания в точке
        '''
        self.__time = float(time)
        self.__update_user_in_db()

    def get_time(self):
        '''
        Возвращает значение желаемого времени пребывания в точке
        :return: Float - значение желаемого времени пребывания в точке
        '''
        return self.__time

    def set_time_arrival(self, time_arrival):
        '''
        Устанавливает значение времени прибытия
        :param time_arrival: String - значение времени прибытия
        '''
        self.__time_arrival = time_arrival
        self.__update_user_in_db()

    def get_time_arrival(self):
        '''
        Возвращает значение времени прибытия
        :return: String - значение времени прибытия
        '''
        return self.__time_arrival

    def set_time_departure(self, time_departure):
        '''
        Устанавливает значение времени прибытия
        :param time_departure: String - значение времени прибытия
        '''
        self.__time_departure = time_departure
        self.__update_user_in_db()

    def get_time_departure(self):
        '''
        Возвращает значение времени отъезда
        :return: String - значение времени отъезда
        '''
        return self.__time_departure

    def set_place_arrival(self, place_arrival):
        '''
        Устанавливает значение места прибытия в формате строки
        :param place: String - значение места прибытия
        '''
        self.__place_arrival = place_arrival
        self.__update_user_in_db()

    def get_place_arrival(self):
        '''
        Возвращает значение места прибытия в формате строки
        :return: String - значение места прибытия
        '''
        return self.__place_arrival

    def set_place_departure(self, place_departure):
        '''
        Устанавливает значение места отъезда в формате строки
        :param place: String - значение места отъезда
        '''
        self.__place_departure = place_departure
        self.__update_user_in_db()

    def get_place_departure(self):
        '''
        Возвращает значение места отъезда в формате строки
        :return: String - значение места отъезда
        '''
        return self.__place_departure
