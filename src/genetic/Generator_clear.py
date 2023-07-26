#!/usr/bin/env python
# coding: utf-8

# In[1]:


import numpy as np
import osmnx as ox
import random
import pandas as pd
import copy as cp
import networkx as nx
import sys
import matplotlib.pyplot as plt
from more_itertools import locate


# In[204]:


def get_pul(G,eat_pul,place_pul):
    dots = place_pul.copy()
    dots['eat'] = np.zeros(dots.shape[0])
    dots['time'] = dots['time'].apply(lambda x: abs(x)*13800+600)
    dots = dots[['osmid', 'type', 'object', 'name', 'lat', 'lon', 'is_culture',
       'is_historic', 'is_religious', 'is_art', 'is_natural', 'popularity',
       'time', 'eat']]
    
    eat = eat_pul.copy()
    eat['is_culture'] = np.ones(eat.shape[0])*0.5
    eat['is_historic'] = np.ones(eat.shape[0])*0.5
    eat['is_religious'] = np.ones(eat.shape[0])*0.5
    eat['is_art'] = np.ones(eat.shape[0])*0.5
    eat['is_natural'] = np.ones(eat.shape[0])*0.5
    eat['eat'] = np.ones(eat.shape[0])
    eat['time'] = eat['time'].apply(lambda x: abs(x)*13800+600)
    eat = eat[['osmid', 'type', 'object', 'name', 'lat', 'lon', 'is_culture',
       'is_historic', 'is_religious', 'is_art', 'is_natural', 'popularity',
       'time', 'eat']]
    pul = pd.concat([dots,eat])
    pul_id = ox.distance.nearest_nodes(G, *pul[['lon','lat']].to_numpy().T, return_dist=False)
    pul['pul_id'] = pul_id
    return pul


# In[203]:


def get_map_graf(place,drive_type="drive"):
    G = ox.graph_from_place(place, network_type=drive_type)
    G = ox.utils_graph.get_largest_component(G, strongly=True)
    G = ox.add_edge_speeds(G)
    speed = 11.
    if drive_type == "drive":
        speed = 11.
    if  drive_type == "walk":
        speed = 1.39
    return G,speed


# ## Функция проверки возможности добавления точки в маршрут
# dt_route_to - Время следования из последней точки маршрута в новую точку
# dt_route_from - Время следования из новой точки в конечную точку
# dt_in - Время нахождения на точке
# dt - Свободное время
# tau_to,tau_from,tau_in - доп задержки для dt_route_to,dt_route_from,dt_in соответственно

# In[93]:


def wey_control(dt_route_to,dt_route_from,dt_in,dt,tau_to=0,tau_from=0,tau_in=0):
    return True if dt >= dt_route_to+dt_in+dt_route_from+tau_to+tau_from+tau_in else False


# ## Класс объекта 'маршрут' и Функция расчета характеристик маршрута

# In[165]:



class WayPoints():
    def __init__(self,route_points,route_osmids,prmtrs,prmtrs_arr,points_type_arr,
                 route_points_times,free_time,sum_rout_dist,
                 sum_road_time,sum_stop_time,is_ok):
        self.route_points = route_points 
        self.route_osmids = route_osmids
        self.points_type_arr = points_type_arr
        self.prmtrs_arr = prmtrs_arr
        self.prmtrs = prmtrs
        self.route_points_times = route_points_times
        self.free_time = free_time
        self.sum_rout_dist = sum_rout_dist
        self.sum_road_time = sum_road_time
        self.sum_stop_time = sum_stop_time
        self.is_ok = is_ok
        self.fitnes = 0
    def new_way(self,route_points,route_osmids,prmtrs_arr,points_type_arr):
        self.route_points = route_points
        self.route_osmids = route_osmids
        self.points_type_arr = points_type_arr
        self.prmtrs_arr = prmtrs_arr
        self.route_points_times = []
        self.free_time = 0
        self.sum_rout_dist = 0
        self.sum_road_time = 0
        self.sum_stop_time = 0
        self.is_ok = False
        self.fitnes = 0
    
    def clone(self):
        return (self.route_points[:],
                self.route_osmids[:],
                self.prmtrs[:],
                self.prmtrs_arr[:],
                self.points_type_arr[:],
            self.route_points_times[:],
            self.free_time,
            self.sum_rout_dist, 
            self.sum_road_time,
            self.sum_stop_time,
            self.is_ok )
    def calculate_route_futures(self,G,pul,prmtr_functions,bgn_time,end_time,
                            speed = 11.,tau_to=0,tau_from=0,tau_in=0):
        prmtr_names = ['popularity','is_culture','is_historic','is_religious','is_art','is_natural','eat']
        n_name = len(prmtr_names)
        self.prmtrs = np.zeros(n_name)
        
        free_times = end_time-bgn_time
        sum_routs_dist = 0
        sum_road_times = 0
        sum_stop_times = 0
        is_ok = False
        route_points_times = [0]

        try:
            try:
                routes = ox.shortest_path(G,self.route_points[:-1],
                                     self.route_points[1:], weight="length")
            #print(routes)
            except nx.NodeNotFound:
                self.is_ok = False
                print('NodeNotFound')
                return 0
            for i,dot in enumerate(self.route_points[1:-1],start = 1):
                #print(i,dot)
                group_pp = []
                for way_type in self.points_type_arr[i]:
                    group_pp.append(check_pttern(way_type,prmtr_names[1:],
                                       prmtr_functions,free_times,bgn_time,end_time,i))
                group_p = max(group_pp)
                s_to = int(sum(ox.utils_graph.route_to_gdf(G, routes[i-1], "length")["length"])) if dot != self.route_points[i-1] else 0. 
                r = ox.shortest_path(G,dot,self.route_points[-1], weight="length")
                s_from = int(sum(ox.utils_graph.route_to_gdf(G, r, "length")["length"])) if dot != self.route_points[-1] else 0.
                dt_route_to = s_to/speed
                dt_route_from = int(s_from/speed)
                print('dot',dot)
                point = pul[pul['osmid']==self.route_osmids[i]]
                dt_in = int(point['time'].values[0])
                #dt_in = int(point_pul[point_pul['pul_id']==dot]['time'].values[0])
                print('ok')
                is_ok = wey_control(dt_route_to,dt_route_from,dt_in,free_times,
                                    tau_to=tau_to,tau_from=tau_from,tau_in=tau_in)

                if is_ok:
                    #routes_points[i].append(-1)
                    #routes_points_times[i].append(dt_route_to+tau_to)

                    #routes_points_times[i].append(dt_in+tau_in)
                    #print(len(routes_points[i]))
                    free_times = free_times-(dt_route_to+dt_in+tau_to+tau_in)
                    #print(i)
                    #print(free_times[i])
                    self.prmtrs_arr[i] = point[prmtr_names]
                    self.prmtrs+= group_p*point[prmtr_names]
                    sum_routs_dist += s_to
                    sum_road_times += dt_route_to+tau_to
                    sum_stop_times += dt_in+tau_in

                else:
                    break
            s_to = int(sum(ox.utils_graph.route_to_gdf(G, routes[-1], "length")["length"]))
            dt_route_to = s_to/speed
            free_times = free_times-(dt_route_to+tau_to)
            sum_routs_dist += s_to
            sum_road_times += dt_route_to+tau_to

            self.free_time = free_times
            self.sum_rout_dist = sum_routs_dist
            self.sum_road_time = sum_road_times
            self.sum_stop_time = sum_stop_times
            self.route_points_times = [0]
            self.is_ok = is_ok
        except ValueError:
            print('err')
            print(routes[i-1])
            self.route_points
            self.is_ok = False
            sys.exit(0) 


# ## Функция генерации маршрута

# #### Генерация паттерна
# x = 1-free_time/(t_end-t_bgn) if len(way)>1 else 0.05

# In[146]:



def early(x):
    a = 0.
    b = 0.05
    c = 0.8
    accessory = 1-(b-x)/(b-a) if (x>=a and x<=b) else 1-(x-b)/(c-b)
    return accessory if x<=c else 0
def in_a_way(x):
    a = 0.1
    b = 0.5
    c = 0.9
    accessory = 1-(b-x)/(b-a) if x>=a and x<=b else 1-(x-b)/(c-b)
    return accessory  if x<=c and x>=a else 0
def late(x):
    a = 0.2
    b = 0.95
    c = 1.
    accessory = 1-(b-x)/(b-a) if x>=a and x<=b else 1-(x-b)/(c-b)
    return accessory if x>=a  else 0
def any_time(x):
    a=0.0
    c=1.
    accessory = 0.7 if x>a and x<c else 0
    return accessory
def off(x):
    return 0 
def get_ver_group(pull,prmtr_names,prmtr_functions,free_time,t_bgn,t_end,way_len):
    functions_dict = {'early':early,
                     'in_a_way':in_a_way,
                     'late':late,
                     'any_time':any_time,
                     'off':off}
    #group = pull[pull[prmtr_name] >= 0.5]
    x = 1-free_time/(t_end-t_bgn) if way_len>1 else 0.05
    acces_arr = []
    for func_name in prmtr_functions:
        acces_arr.append(functions_dict[func_name](x))
    max_acces = max(acces_arr)
    max_indx = list(locate(acces_arr, lambda x: x == max_acces))
    names = []
    group = pd.DataFrame()
    for indx in max_indx:
        group = pd.concat([group,pull[pull[prmtr_names[indx]]>=0.7]])
        names.append(prmtr_names[indx])
    return max_acces,group.drop_duplicates(subset='osmid'),names


# #### Проверка паттерна

# In[50]:


def check_pttern(point_type,prmtr_names,prmtr_functions,free_time,t_bgn,t_end,way_len):
    functions_dict = {'early':early,
                     'in_a_way':in_a_way,
                     'late':late,
                     'any_time':any_time,
                     'off':off}
    #group = pull[pull[prmtr_name] >= 0.5]
    x = 1-free_time/(t_end-t_bgn) if way_len>1 else 0.05
    acces_arr = []
    for func_name in prmtr_functions:
        acces_arr.append(functions_dict[func_name](x))
    max_acces = max(acces_arr)
    max_indx = list(locate(acces_arr, lambda x: x == max_acces))
    names = []
    for indx in max_indx:
        names.append(prmtr_names[indx])
    if point_type in names:
        return max_acces
    else:
        
        return acces_arr[prmtr_names.index(point_type)]


# #### Генерация

# In[151]:


def route_gen(G,pul,prmtr_functions,start_point,stop_point,bgn_time,end_time,
              n=1,speed=11.,tau_to=0,tau_from=0,tau_in=0,
              max_variant_per_point=3):#m/sec
    way_list = []
    prmtr_names = ['popularity','is_culture','is_historic','is_religious','is_art','is_natural','eat']
    n_name = len(prmtr_names)
    start_id = ox.distance.nearest_nodes(G, *start_point, return_dist=False)
    stop_id = ox.distance.nearest_nodes(G, *stop_point, return_dist=False)
    for i in range(n):
        #print(i)
        free_times = end_time-bgn_time
        routes_points = [start_id]
        route_osmids = [start_id]
        points_type_arr = [[None]]
        prmtrs_arr = []
        prmtrs_arr.append([0])
        routes_points_times = [0]
        prmtrs = np.zeros(n_name)
        sum_routs_dist = 0 
        sum_road_times = 0
        sum_stop_times = 0
        try_counter = 0
        while(free_times>0):
            print(free_times)  
            #print(prmtr_names[1:])
            #print(prmtr_functions)
            group_p,point_pul,pnames = get_ver_group(pul,prmtr_names[1:],prmtr_functions,
                                              free_times,bgn_time,end_time,len(routes_points))
            try:
                point_osmid = random.choice(point_pul['osmid'].to_list())
                #point_id = random.choice(point_pul['pul_id'])
                point_id = point_pul[point_pul['osmid']==point_osmid]['pul_id'].values[0]
                #print(point_id)
                routes = ox.shortest_path(G,[routes_points[-1],point_id],
                                         [point_id,stop_id], weight="length")
                s_to = int(sum(ox.utils_graph.route_to_gdf(G, routes[0], "length")["length"]))
                s_from = int(sum(ox.utils_graph.route_to_gdf(G, routes[1], "length")["length"]))
                dt_route_to = s_to/speed
                dt_route_from = int(s_from/speed)
                #print(s_to,s_from)
                print()
                point = point_pul[point_pul['osmid']==point_osmid]
                dt_in = int(point['time'].values[0])
                print(dt_in)
                if wey_control(dt_route_to,dt_route_from,dt_in,free_times,tau_to=tau_to,tau_from=tau_from,tau_in=tau_in):
                    #routes_points[i].append(-1)
                    #routes_points_times[i].append(dt_route_to+tau_to)
                    print(group_p)
                    routes_points.append(point_id)
                    route_osmids.append(point_osmid)
                    points_type_arr.append(pnames)
                    prmtrs_arr.append(point[prmtr_names])
                    prmtrs+= group_p*point[prmtr_names]
                    #routes_points_times[i].append(dt_in+tau_in)
                    #print(len(routes_points))
                    free_times = free_times-(dt_route_to+dt_in+tau_to+tau_in)
                    #print(free_times[i])
                    sum_routs_dist+=s_to
                    sum_road_times+=dt_route_to+tau_to
                    sum_stop_times+=dt_in+tau_in
                    try_counter = 0

                else:
                    if try_counter > max_variant_per_point:
                        print(i,'end')
                        routes = ox.shortest_path(G,routes_points[-1],
                                         stop_id, weight="length")
                        #routes_points[i].append(-1)
                        
                        routes_points.append(stop_id)
                        route_osmids.append(stop_id)
                        prmtrs_arr.append([0])
                        points_type_arr.append([None])
                        s = int(sum(ox.utils_graph.route_to_gdf(G, routes, "length")["length"]))
                        dt_route = s/speed
                        #routes_points_times[i].append(dt_route+tau_to)
                        routes_points_times.append(0)
                        #print(dt_route)
                        free_times = free_times-(dt_route+tau_to)
                        sum_routs_dist+=s
                        
                        #sum_road_times[i]+=dt_route+tau_to
                        break
                    else:
                        print('не нашел')
                        try_counter+=1
            except Exception:
                try_counter+=1
        way_list.append(WayPoints(routes_points,route_osmids,prmtrs,prmtrs_arr,points_type_arr,
                                  routes_points_times,free_times,
                                  sum_routs_dist,sum_road_times,sum_stop_times,True))
    return way_list   


# ## Fitnes function

# In[58]:


def Fitnes(*args,**kwargs):
    
    way = args[0]
    anketa = np.array(args[1])
    anketa_bus = args[2]
    anketa_time = args[3]
    #way.fitnes = way.is_ok*1
    fitnes = way.is_ok*(np.sum(way.prmtrs*anketa)+anketa_bus*anketa_time*way.sum_rout_dist/10000.)
    way.fitnes = fitnes if fitnes > 0 else 0


# ##  Функция Отбора (Селекция)
# Турнирный алгоритм

# In[59]:


def select(chromosome_list ,k=2):
    
    new_chromosome_list = []
    for i in range(len(chromosome_list)):
        rivals = random.choices(chromosome_list,k=k)
        new_chromosome_list.append(rivals[0] if rivals[0].fitnes > rivals[1].fitnes else rivals[1])
    return new_chromosome_list


# ## Функция скрещивания

# In[173]:


def cross(way1,way2):
    
    chaild1 = WayPoints(*way1.clone())
    chaild2 = WayPoints(*way2.clone())
    try:
        point_id1 = random.randint(1, len(chaild1.route_points)-1)
        point_id2 = int(point_id1/len(chaild1.route_points)*len(chaild1.route_points))
        point_id2 = point_id2 if point_id2>0  else 1
        if point_id2==1 and len(chaild1.route_points)-1==1:
            raise ValueError('')
        ##point_id2 = random.randint(1, len(chaild2.route_points)-1)
        #print(point_id1,point_id2,len(chaild1.route_points),len(chaild2.route_points))
    except ValueError:
        print('Not point for cross')
        return way1,way2
    part_points1 = chaild1.route_points[:point_id1]
    part_points1.extend(chaild2.route_points[point_id2:])
    part_points2 = chaild2.route_points[:point_id2]
    part_points2.extend( chaild1.route_points[point_id1:])
    a1 = chaild1.route_osmids[:point_id1]
    a1.extend(chaild2.route_osmids[point_id2:])
    a2 = chaild2.route_osmids[:point_id2]
    a2.extend(chaild1.route_osmids[point_id1:])
    b1 = chaild1.prmtrs_arr[:point_id1]
    b1.extend(chaild2.prmtrs_arr[point_id2:])
    b2 = chaild2.prmtrs_arr[:point_id2]
    b2.extend(chaild1.prmtrs_arr[point_id1:])
    c1 = chaild1.points_type_arr[:point_id1]
    c1.extend(chaild2.points_type_arr[point_id2:])
    c2 = chaild2.points_type_arr[:point_id2]
    c2.extend(chaild1.points_type_arr[point_id1:])
    
    
    #print(type(chaild2.route_osmids[:point_id2]))
    chaild1.new_way(part_points1,a1,b1,c1)
    chaild2.new_way(part_points2,a2,b2,c2)
    return chaild1,chaild2
    
    


# ## Функция мутации
# 

# In[162]:


def mute(way,G,point_pul,k=3,p_mute=0.1):
    prmtr_names = ['popularity','is_culture','is_historic','is_religious','is_art','is_natural']
    #new_points = ox.utils_geo.sample_points(GOneGraf, k*len(way.route_points))
    
     
    #point_pul.iloc[random.choices(point_pul.index,k=k*len(way.route_points))]
    #print(new_points)
    #lon = new_points['lon'].to_list()
    #lat = new_points['lat'].to_list()
    #new_points.insert(new_points.shape[1]-1,
    #                  'node',ox.distance.nearest_nodes(G, lon,lat,return_dist=False) , 
    #                  allow_duplicates = False)
    for i,point in enumerate(way.route_points[1:-1],start = 1):
        #print(i)
        new_points = pd.DataFrame()
        if random.random() <= p_mute:
            #print('mutant')
            #lon,lat = point_pul[point_pul['pul_id'] == point][['lon','lat']].values
            #print(len(way.route_osmids),len(way.route_points))
            for type_point in way.points_type_arr[i]:
                new_points = pd.concat([new_points,point_pul[point_pul[type_point]>0.7]])
            new_points = new_points.drop_duplicates(subset = 'osmid')
            new_points = new_points.reset_index(drop=True)
            new_points = new_points.iloc[random.choices(new_points.index,k=k)]
            lon = new_points['lon'].to_list()
            lat = new_points['lat'].to_list()
            new_points.insert(new_points.shape[1]-1,
                      'node',ox.distance.nearest_nodes(G, lon,lat,return_dist=False) , 
                      allow_duplicates = False)
            
            way.route_osmids[i] = random.choice(new_points['osmid'].to_list())
            way.route_points[i] = new_points[new_points['osmid']==way.route_osmids[i]]['node'].values[0]
            way.prmtrs_arr[i] = new_points[new_points['osmid']==way.route_osmids[i]][prmtr_names]


# ## Генетический алгоритм

# In[179]:


MAX_GENERATION =10 #10
POPULATION_SIZE = 6
P_CROSS = 0.9
P_MUTE = 0.2
max_variant_per_point=10
speed=11. # m/sec
start_point = (37.597447,55.906487) #lon, lat
stop_point = (37.747505,55.648280)
bgn_time = 36000 # sec
end_time = 64800
tau_to=0
tau_from=0
tau_in=0
#point_pul = dots[['lon','lat']].to_numpy()
#pul_id = ox.distance.nearest_nodes(G, *point_pul.T, return_dist=False)
#dots['pul_id'] = pul_id
#point_pul = dots
prmtr_functions = ['in_a_way','late','off','early','early','off']


# In[166]:


way_list = route_gen(G,point_pul,prmtr_functions,start_point,stop_point,bgn_time,end_time,
              n=POPULATION_SIZE,speed=speed,tau_to=tau_to,tau_from=tau_from,tau_in=tau_in,
              max_variant_per_point=max_variant_per_point)


# In[205]:


def run_genetic(G,point_pul,way_list,anceta_prmtr,anketa_bus,anketa_time,prmtr_functions,start_point,stop_point,bgn_time,end_time,
                tau_to=0,tau_from=0, tau_in=0, max_generation = 5,p_cross=0.9,p_mute=0.2,speed=11.):
    way_list2 = cp.deepcopy(way_list)
    gen_count = 0
    ways_fit = []
    while(gen_count<max_generation):
        way_new = []
        print(gen_count)
        gen_count+=1
        fitnes_arr = []
        print('fitnes')
        for way in way_list2:

            Fitnes(way,anceta_prmtr,anketa_bus,anketa_time)
            fitnes_arr.append(way.fitnes)
        ways_fit.append(fitnes_arr)
        print('select')
        way_list2 = select(way_list2 ,k=2)

        print('cross\\mute\\new_way')
        for chaild1,chaild2 in zip(way_list2[::2],way_list2[1::2]):
            if random.random()< p_cross:
                chaild1,chaild2 = cross(chaild1,chaild2)
                mute(chaild1,G,point_pul,k=3,p_mute=p_mute)
                mute(chaild2,G,point_pul,k=3,p_mute=p_mute)

                chaild1.calculate_route_futures(G,point_pul,prmtr_functions,bgn_time,end_time,
                                speed=speed,tau_to=tau_to,tau_from=tau_from,tau_in=tau_in)
                chaild2.calculate_route_futures(G,point_pul,prmtr_functions,bgn_time,end_time,
                                speed=speed,tau_to=tau_to,tau_from=tau_from,tau_in=tau_in)
                way_new.append(chaild1)
                way_new.append(chaild2)
            else:
                way_new.append(chaild1)
                way_new.append(chaild2)
        way_list2 = way_new
    return way_list2


# In[209]:


def returt_way(way_list,pul,k=3):
    way_top = []
    for way in way_list:
        way_top.append([way.fitnes,way.route_osmids[1:-1]])
    way_top = sorted(way_top,key=lambda x:x[0])    
    ways = []
    for i in range(k):
        pwn = []
        for i,ids in enumerate(way_top[i].route_osmids[1:-1],start=1):
            #pwn.append([pul[pul["osmid"]==ids]['name'].values[0],way_top[i].points_type_arr[i]])
            pwn.append(ids)
        ways.append(pwn)
    return ways


# In[ ]:




