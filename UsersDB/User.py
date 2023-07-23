import sqlite3

from options import users_db_name


class User:
    # ID пользователя
    __user_id = None
    # Культурность
    __is_culture = None
    # Историчность
    __is_historic = None
    # Религиозность
    __is_religious = None
    # Искусство
    __is_art = None
    # Природность
    __is_natural = None
    # Популярность
    __popularity = None
    # Время прибытия (Не храниться в БД!)
    __time_arrival = None
    # Время отъезда (Не храниться в БД!)
    __time_departure = None
    # Место (Не храниться в БД!)
    __place = None

    def __str__(self):
        return f"{self.__user_id}:\t{self.__is_culture}\t{self.__is_historic}\t" \
               f"{self.__is_religious}\t{self.__is_art}\t{self.__is_natural}\t" \
               f"{self.__popularity}"

    def __init__(self, user_id):
        '''
        Класс пользователя
        :param user_id: Int - ID пользователя в телеграм
        '''
        self.__user_id = int(user_id)

    def __update_user_in_db(self):
        # try:
        con = sqlite3.connect(users_db_name)
        cur = con.cursor()
        cur.execute(f"""
                UPDATE users
                SET is_culture = '{str(self.__is_culture)}', is_historic = '{str(self.__is_historic)}', is_religious = '{str(self.__is_religious)}', is_art = '{str(self.__is_art)}', is_natural = '{str(self.__is_natural)}', popularity = '{str(self.__popularity)}'
                WHERE user_id = {str(self.__user_id)};
                """)
        con.commit()
        con.close()
        # except Exception as ex:
        #     print("User: update_user_in_db error: " + str(ex))

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

    def set_culture(self, is_culture):
        '''
        Устанавливает значение культуры
        :param is_culture: Float - параметр культуры
        '''
        self.__is_culture = is_culture
        self.__update_user_in_db()

    def get_culture(self):
        '''
        Возвращает значение культуры
        :return: Float - значение культуры
        '''
        return self.__is_culture

    def set_historic(self, is_historic):
        '''
        Устанавливает значение историчности
        :param is_historic: Float - параметр историчности
        '''
        self.__is_historic = is_historic
        self.__update_user_in_db()

    def get_historic(self):
        '''
        Возвращает значение историчности
        :return: Float - значение историчности
        '''
        return self.__is_historic

    def set_religious(self, is_religious):
        '''
        Устанавливает значение религии
        :param is_religious: Float - параметр религии
        '''
        self.__is_religious = is_religious
        self.__update_user_in_db()

    def get_religious(self):
        '''
        Возвращает значение религии
        :return: Float - значение религии
        '''
        return self.__is_religious

    def set_art(self, is_art):
        '''
        Устанавливает значение искусства
        :param is_art: Float - параметр искусства
        '''
        self.__is_art = is_art
        self.__update_user_in_db()

    def get_art(self):
        '''
        Возвращает значение искусства
        :return: Float - значение искусства
        '''
        return self.__is_art

    def set_natural(self, is_natural):
        '''
        Устанавливает значение природности
        :param is_natural: Float - параметр природности
        '''
        self.__is_natural = is_natural
        self.__update_user_in_db()

    def get_natural(self):
        '''
        Возвращает значение природности
        :return: Float - значение природности
        '''
        return self.__is_natural

    def set_popularity(self, popularity):
        '''
        Устанавливает значение популярности
        :param popularity: Float - параметр популярности
        '''
        self.__popularity = popularity
        self.__update_user_in_db()

    def get_popularity(self):
        '''
        Возвращает значение популярности
        :return: Float - значение популярности
        '''
        return self.__popularity

    def set_time_arrival(self, time_arrival):
        '''
        Устанавливает значение времени прибытия в формате чч:мм (не сохраняется в Базе Данных!)
        :param time_arrival: String - значение времени прибытия в формате чч:мм
        '''
        self.__time_arrival = time_arrival

    def get_time_arrival(self):
        '''
        Устанавливает значение времени прибытия в формате чч:мм (не сохраняется в Базе Данных!)
        :return: String - значение времени прибытия в формате чч:мм
        '''
        return self.__time_arrival

    def set_time_departure(self, time_departure):
        '''
        Устанавливает значение времени прибытия в формате чч:мм (не сохраняется в Базе Данных!)
        :param time_departure: String - значение времени прибытия в формате чч:мм
        '''
        self.__time_departure = time_departure

    def get_time_departure(self):
        '''
        Устанавливает значение времени отъезда в формате чч:мм (не сохраняется в Базе Данных!)
        :return: String - значение времени отъезда в формате чч:мм
        '''
        return self.__time_departure

    def set_place(self, place):
        '''
        Устанавливает значение места прибытия в формате строки (не сохраняется в Базе Данных!)
        :param place: String - значение места прибытия
        '''
        self.__place = place

    def get_place(self):
        '''
        Устанавливает значение места прибытия в формате строки (не сохраняется в Базе Данных!)
        :return: String - значение места прибытия в формате
        '''
        return self.__place

