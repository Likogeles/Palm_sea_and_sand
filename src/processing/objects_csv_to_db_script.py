'''
Этот скрипт преобразует csv файл культурных мест в базу данных, и НЕ должен использоваться во время работы бота
'''

import csv

from src.PlacesDB.Place import Place
from src.PlacesDB.PlaceList import PlaceList

arr = []
places = []
placesList = PlaceList()

with open('joined.csv', mode='r', encoding='utf-8') as data:
    for line in csv.reader(data):
        arr.append(line)

for i in range(1, len(arr)):
    new_place = Place(int(arr[i][0]),
                      arr[i][1].replace("'", '"'),
                      arr[i][2].replace("'", '"'),
                      arr[i][3].replace("'", '"'),
                      arr[i][4].replace("'", '"'),
                      arr[i][5].replace("'", '"'),
                      arr[i][6].replace("'", '"'),
                      arr[i][7].replace("'", '"'),
                      arr[i][8].replace("'", '"'),
                      arr[i][9].replace("'", '"'),
                      arr[i][10].replace("'", '"'),
                      arr[i][11].replace("'", '"'),
                      arr[i][12].replace("'", '"'),
                      arr[i][13].replace("'", '"'),
                      arr[i][14].replace("'", '"'),
                      arr[i][15].replace("'", '"'),
                      arr[i][16].replace("'", '"'),
                      arr[i][17].replace("'", '"'),
                      arr[i][18].replace("'", '"'),
                      arr[i][19].replace("'", '"'),
                      arr[i][20].replace("'", '"'),
                      arr[i][21].replace("'", '"'),
                      arr[i][22].replace("'", '"'),
                      arr[i][23].replace("'", '"'),
                      arr[i][24].replace("'", '"'),
                      arr[i][25].replace("'", '"'),
                      arr[i][26].replace("'", '"'),
                      arr[i][27].replace("'", '"'),
                      arr[i][28].replace("'", '"'),
                      arr[i][29].replace("'", '"'),
                      arr[i][30].replace("'", '"'),
                      arr[i][31].replace("'", '"'),
                      arr[i][32].replace("'", '"'),
                      arr[i][33].replace("'", '"'),
                      arr[i][34].replace("'", '"'),
                      arr[i][35].replace("'", '"'),
                      arr[i][36].replace("'", '"'),
                      arr[i][37].replace("'", '"'))
    placesList.add_place(new_place)

placesList.save()
# placesList.load()
# for i in placesList.get_all_places():
#     print(i)
