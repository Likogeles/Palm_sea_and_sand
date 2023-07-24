import sqlite3
from UsersDB.User import User
from options import users_db_name


class UserList:
    __userList = list()

    def __init__(self):
        self.load()

    def __insert_user(self, cur, user):
        '''
        Вставить пользователя в таблицу
        :param cur: курсор БД
        :param user: Пользователь
        '''
        cur.execute(f"""
                    INSERT INTO users VALUES
                    ('{user.get_user_id()}','{user.get_culture()}','{user.get_historic()}','{user.get_religious()}','{user.get_art()}','{user.get_natural()}','{user.get_popularity()}')
                    """)

    def __create_user_table(self, cur):
        '''
        Создать таблицу пользователей
        :param cur: курсор БД
        '''
        cur.execute("""CREATE TABLE users(
                    user_id varchar(255) UNIQUE,
                    is_culture varchar(255),
                    is_historic varchar(255),
                    is_religious varchar(255),
                    is_art varchar(255),
                    is_natural varchar(255),
                    popularity varchar(255)
                    )""")

    # Удаление и пересохранение списка пользователей
    def save(self):
        '''
        Удаление и пересохранение списка пользователей
        '''
        try:
            con = sqlite3.connect(users_db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if len(table_check.fetchall()) == 0:
                cur.execute("""DROP TABLE users;""")
            self.__create_user_table(cur)

            for user in self.__userList:
                self.__insert_user(cur, user)

            con.commit()
            con.close()
            return True
        except Exception as ex:
            print("UsersList: save error: " + str(ex))
        return False

    # Загрузка списка пользователей
    def load(self):
        '''
        Загрузка списка пользователей
        '''
        try:
            con = sqlite3.connect(users_db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if len(table_check.fetchall()) == 0:
                return False

            result = cur.execute("SELECT * FROM users;")
            result = list(result.fetchall())

            self.__userList.clear()
            for user in result:
                user_id = user[0]
                if user_id != "None":
                    user_id = int(user_id)
                else:
                    user_id = None
                self.__userList.append(User(user_id))
            con.close()
        except Exception as ex:
            print("UsersList: load error: " + str(ex))
        return False

    # Добавить пользователя
    def add_user(self, user_id):
        '''
        Добавить пользователя
        '''
        for old_user in self.__userList:
            if user_id == old_user.get_user_id():
                print("UsersList: add_user error: Пользователь уже существует")
                return False
        new_user = User(user_id)
        self.__userList.append(new_user)
        # try:
        con = sqlite3.connect(users_db_name)
        cur = con.cursor()

        table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
        if len(table_check.fetchall()) == 0:
            self.__create_user_table(cur)
        self.__insert_user(cur, User(user_id))

        con.commit()
        con.close()
        return True
        # except Exception as ex:
        #     print("UsersList: add user error: " + str(ex))
        # return False

    # Получить польщователя по его ID. Возвращает None если пользователя не существует
    def get_user_by_id(self, user_id):
        '''
        Получить польщователя по его ID. Возвращает None если пользователя не существует
        '''
        for user in self.__userList:
            if user.get_user_id() == user_id:
                return user
        return None

    # Получить всех пользователей
    def get_all_users(self):
        '''
        Получить всех пользователей
        '''
        return self.__userList

    # Очистить список пользователей (не удаляет Базу Данных!)
    def clear(self):
        '''
        Очистить список пользователей (не удаляет Базу Данных!)
        '''
        self.__userList.clear()
