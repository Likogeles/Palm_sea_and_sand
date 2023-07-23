from typing import Annotated

class User:
    __user_id = None
    __is_culture = None
    __is_historic = None
    __is_religious = None
    __is_art = None
    __is_natural = None
    __popularity = None
    __time_arrival = None
    __time_departure = None
    __place = None

    def __init__(self, user_id):
        '''
        Класс пользователя
        :param user_id: Int - ID пользователя в телеграм
        '''
        self.user_id = user_id

    def set_culture(self, is_culture):
        '''
        Устанавливает значение культуры
        :param is_culture: Float - параметр культуры
        '''
        self.__is_culture = is_culture

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

    def __str__(self):
        return f"Id: {self.user_id}"
