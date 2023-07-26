import sqlite3

from options import places_db_name
from PlacesDB.Place import Place


class PlaceList:
    __placeList = list()

    def __init__(self):
        self.load()

    def __create_places_table(self, cur):
        '''
        Создать таблицу пользователей
        :param cur: курсор БД
        '''
        cur.execute("""CREATE TABLE places(
                    id varchar(255),
                    osmid varchar(255),
                    type_ varchar(255),
                    object_ varchar(255),
                    name varchar(255),
                    lat varchar(255),
                    lon varchar(255),
                    geometry varchar(255),
                    city varchar(255),
                    historic varchar(255),
                    addr_street varchar(255),
                    addr_housenumber varchar(255),
                    start_date varchar(255),
                    opening_hours varchar(255),
                    phone varchar(255),
                    contact_website varchar(255),
                    building_levels varchar(255),
                    wikipedia varchar(255),
                    contact_phone varchar(255),
                    ref_temples_ru varchar(255),
                    contact_email varchar(255),
                    website varchar(255),
                    description varchar(255),
                    contact_vk varchar(255),
                    service_times varchar(255),
                    contact_facebook varchar(255),
                    contact_instagram varchar(255),
                    contact_twitter varchar(255),
                    contact_youtube varchar(255),
                    email varchar(255),
                    class_ varchar(255),
                    is_culture varchar(255),
                    is_historic varchar(255),
                    is_religious varchar(255),
                    is_art varchar(255),
                    is_natural varchar(255),
                    popularity varchar(255),
                    time varchar(255)
                    )""")

    def __insert_place(self, cur, place):
        cur.execute(f"""INSERT INTO places VALUES
                           ('{place.id}', '{place.osmid}', '{place.type_}', '{place.object_}', '{place.name}',
                           '{place.lat}', '{place.lon}', '{place.geometry}', '{place.city}', '{place.historic}',
                           '{place.addr_street}', '{place.addr_housenumber}', '{place.start_date}',
                           '{place.opening_hours}', '{place.phone}', '{place.contact_website}',
                           '{place.building_levels}', '{place.wikipedia}', '{place.contact_phone}',
                           '{place.ref_temples_ru}', '{place.contact_email}', '{place.website}',
                           '{place.description}', '{place.contact_vk}', '{place.service_times}',
                           '{place.contact_facebook}', '{place.contact_instagram}', '{place.contact_twitter}',
                           '{place.contact_youtube}', '{place.email}', '{place.class_}', '{place.is_culture}',
                           '{place.is_historic}', '{place.is_religious}', '{place.is_art}', '{place.is_natural}',
                           '{place.popularity}', '{place.time}')
                           """)

    def get_place_by_type(self, place_type) -> list[Place]:
        '''
        Возвращает список мест определённого типа\n
        :param place_type: тип места

        На данный момент доступны:\n
        place_of_worship\n
        museum\n
        memorial\n
        gallery\n
        viewpoint\n
        monument\n
        church\n
        beach\n
        theatre\n
        yes\n
        attraction
        '''
        return list(filter(lambda x: x.type_ == place_type, self.__placeList))

    # def get_theatre_places(self):
    #     '''
    #     Возвращает список объектов типа 'theatre'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'theatre', self.__placeList))
    #
    # def get_place_of_worship_places(self):
    #     '''
    #     Возвращает список объектов типа 'place_of_worship'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'place_of_worship', self.__placeList))
    #
    # def get_beach_places(self):
    #     '''
    #     Возвращает список объектов типа 'beach'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'beach', self.__placeList))
    #
    # def get_yes_places(self):
    #     '''
    #     Возвращает список объектов типа 'yes'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'yes', self.__placeList))
    #
    # def get_attraction_places(self):
    #     '''
    #     Возвращает список объектов типа 'attraction'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'attraction', self.__placeList))
    #
    # def get_memorial_places(self):
    #     '''
    #     Возвращает список объектов типа 'memorial'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'memorial', self.__placeList))
    #
    # def get_monument_places(self):
    #     '''
    #     Возвращает список объектов типа 'monument'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'monument', self.__placeList))
    #
    # def get_viewpoint_places(self):
    #     '''
    #     Возвращает список объектов типа 'viewpoint'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'viewpoint', self.__placeList))
    #
    # def get_gallery_places(self):
    #     '''
    #     Возвращает список объектов типа 'gallery'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'gallery', self.__placeList))
    #
    # def get_museum_places(self):
    #     '''
    #     Возвращает список объектов типа 'museum'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'museum', self.__placeList))
    #
    # def get_church_places(self):
    #     '''
    #     Возвращает список объектов типа 'church'\n
    #     :return: List(Place)
    #     '''
    #     return list(filter(lambda x: x.type_ == 'church', self.__placeList))

    def add_place(self, new_place):
        self.__placeList.append(new_place)

    def get_all_places(self) -> list[Place]:
        return self.__placeList

    def save(self):
        try:
            con = sqlite3.connect(places_db_name)
            cur = con.cursor()

            # table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='places';")
            # if len(table_check.fetchall()) == 0:
            #     cur.execute("""DROP TABLE places;""")
            self.__create_places_table(cur)

            for place in self.__placeList:
                self.__insert_place(cur, place)

            con.commit()
            con.close()
            return True
        except Exception as ex:
            print("PlaceList: save error: " + str(ex))
        return False

    def load(self):
        try:
            con = sqlite3.connect(places_db_name)
            cur = con.cursor()

            table_check = cur.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='places';")
            if len(table_check.fetchall()) == 0:
                return False

            result = cur.execute("SELECT * FROM places;")
            result = list(result.fetchall())

            self.__placeList.clear()
            for place in result:
                new_place = Place(
                    place[0],
                    place[1],
                    place[2],
                    place[3],
                    place[4],
                    place[5],
                    place[6],
                    place[7],
                    place[8],
                    place[9],
                    place[10],
                    place[11],
                    place[12],
                    place[13],
                    place[14],
                    place[15],
                    place[16],
                    place[17],
                    place[18],
                    place[19],
                    place[20],
                    place[21],
                    place[22],
                    place[23],
                    place[24],
                    place[25],
                    place[26],
                    place[27],
                    place[28],
                    place[29],
                    place[30],
                    place[31],
                    place[32],
                    place[33],
                    place[34],
                    place[35],
                    place[36],
                    place[37]
                )
                self.__placeList.append(new_place)
            con.close()
        except Exception as ex:
            print("UsersList: load error: " + str(ex))
        return False