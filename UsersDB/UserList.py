import sqlite3
from UsersDB.User import User


class UserList:
    __userList = list()

    db_name = "TomasBot.db"

    def __init__(self):
        self.load()

    # Удаление и пересохранение списка пользователей
    def save(self):
        '''
        Удаление и пересохранение списка пользователей
        '''
        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if len(table_check.fetchall()) == 0:
                cur.execute("""DROP TABLE users;""")
            cur.execute("""CREATE TABLE users(
            user_id varchar(255)
            )""")

            for user in self.__userList:
                cur.execute(f"""
                INSERT INTO users VALUES
                ('{user.user_id}')
                """)

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
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if len(table_check.fetchall()) == 0:
                return False

            result = cur.execute("SELECT * FROM users;")
            result = list(result.fetchall())

            self.__userList.clear()
            for user in result:
                user_id = user[1]
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
            if str(user_id) == old_user.user_id:
                print("UsersList: save error: Пользователь уже существует")
                return False
        new_user = User(user_id)
        self.__userList.append(new_user)

        try:
            con = sqlite3.connect(self.db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users';")
            if len(table_check.fetchall()) == 0:
                cur.execute("""CREATE TABLE users(
                user_id varchar(255)
                )""")

            cur.execute(f"""
            INSERT INTO users VALUES
            ('{new_user.user_id}')
            """)

            con.commit()
            con.close()
            return True
        except Exception as ex:
            print("UsersList: save error: " + str(ex))
        return False

    # Получить польщователя по его ID. Возвращает None если пользователя не существует
    def get_user_by_id(self, user_id):
        '''
        Получить польщователя по его ID. Возвращает None если пользователя не существует
        '''
        for user in self.__userList:
            if user.user_id == user_id:
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
