import osmnx as ox
import numpy as np
import pandas as pd

# Тэги для запросов OSM API
tags = [ 
        {'building':'church'}, {'amenity':'place_of_worship'},
        {'historic': 'memorial'}, {'historic': 'monument'}, {'historic': 'yes'},
        {'natural': 'beach'}, {'tourism': 'viewpoint'}, {'tourism': 'gallery'},
        {'tourism':'museum'}, {'tourism':'attraction'},
        {'amenity':'theatre'},      
]
    
tags_food = [
        {'amenity':'cafe'}, {'amenity':'fast_food'},
        {'amenity':'restaurant'}
]

columns_normilized = [
    'is_culture', 'is_historic', 'is_religious', 'is_art', 'is_natural', 'popularity', 'time'
]

filter_tags = ['osmid', 'type', 'object', 'name', 'lat', 'lon', 'geometry', 'city', 'historic',
               'addr:street', 'addr:housenumber','start_date', 
               'opening_hours', 'phone', 'contact:website', 
               'building:levels', 'wikipedia', 'contact:phone', 
               'ref:temples.ru', 'contact:email', 'website', 
               'description', 'contact:vk', 'service_times',
               'contact:facebook', 'contact:instagram', 'contact:twitter', 'contact:youtube', 'email'
              ]
filter_tags_food = ['osmid', 'type', 'object', 'name', 'geometry', 'city',
               'addr:street', 'addr:housenumber','start_date', 
               'opening_hours', 'phone', 'contact:website', 
               'building:levels', 'wikipedia', 'contact:phone', 'contact:email', 'website', 'description', 'contact:vk',
               'contact:facebook', 'contact:instagram', 'contact:twitter', 'contact:youtube', 'email'
              ]

def osm_query(tag, city):
    gdf = ox.features_from_place(city, tag).reset_index()
    gdf['city'] = np.full(len(gdf), city.split(',')[0])
    gdf['object'] = np.full(len(gdf), list(tag.keys())[0])
    gdf['type'] = np.full(len(gdf), tag[list(tag.keys())[0]])
    return gdf

def get_lat_lon(geometry):   
    lon = geometry.apply(lambda x: x.x if x.geom_type == 'Point' else x.centroid.x)
    lat = geometry.apply(lambda x: x.y if x.geom_type == 'Point' else x.centroid.y)
    return lat, lon

def get_raw_data(tags, cities):
    gdfs = []
    for city in cities:
        for tag in tags:
            gdfs.append(osm_query(tag, city))
    gdf = pd.concat(gdfs)
    gdf_f = gdf[gdf['name'].notna()].copy()
    lat, lon = get_lat_lon(gdf_f['geometry'])
    gdf_f['lat'] = lat
    gdf_f['lon'] = lon
    return gdf_f.loc[:, filter_tags].reset_index(drop = True)

def get_normilized(gdfs):
    new = gdfs[['osmid', 'name', 'type']].copy()
    new['is_culture'] = (gdfs['type'] != 'beach') & (gdfs['type'] != 'viewpoint')
    new['is_culture'] = new['is_culture'].replace({True: float(1), False: float(0)})
    new['is_historic'] = (gdfs['type'] == 'museum') | (gdfs['type'] == 'monument') | (gdfs['type'] == 'memorial')
    new['is_historic'] = new['is_historic'].replace({True: float(1), False: float(0)})
    new['is_religious'] = (gdfs['type'] == 'church') | (gdfs['type'] == 'place_of_worship')
    new['is_religious'] = new['is_religious'].replace({True: float(1), False: float(0)})
    new['is_art'] = (gdfs['type'] == 'museum') | (gdfs['type'] == 'gallery')
    new['is_art'] = new['is_art'].replace({True: float(1), False: float(0)})
    new['is_natural'] = (gdfs['type'] == 'beach') | (gdfs['type'] == 'viewpoint') | (gdfs['type'] == 'monument')
    new['is_natural'] = new['is_art'].replace({True: float(1), False: float(0)})
    new['popularity'] = (gdfs['opening_hours'].notna()).replace({True: float(1), False: float(0)}) +\
    (gdfs['phone'].notna() | gdfs['contact:phone'].notna()).replace({True: float(1), False: float(0)}) +\
    (gdfs['contact:website'].notna() | gdfs['website'].notna()).replace({True: float(1), False: float(0)}).apply(lambda x: x * 2) +\
    (gdfs['wikipedia'].notna()).replace({True: float(1), False: float(0)}).apply(lambda x: x * 3) +\
    (gdfs['contact:email'].notna() | gdfs['email'].notna()).replace({True: float(1), False: float(0)})
    new['time'] = (gdfs['building:levels']).replace({np.nan : float(1)}).apply(lambda x: float(x))
    new = new.reset_index(drop = True)
    data = new[['is_culture', 'is_historic', 'is_religious', 'is_art', 'is_natural', 'popularity', 'time']].apply(lambda x: (x - x.min())/(x.max() - x.min()))
    return data