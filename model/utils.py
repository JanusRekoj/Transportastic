import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from PIL import Image, ImageDraw
import time
import datetime

def read_data(path_dir_data):
    dict_data = {}
    #Read out is very specialized
    list_elements = list(os.walk(path_dir_data))
    list_elements = list_elements[1:-1]
    for subdir in list_elements:
        df_gps_data = pd.read_csv(os.path.join(subdir[0], subdir[2][0]))
        df_passenger_count = pd.read_csv(os.path.join(subdir[0], subdir[2][1]))
        df_wifi_data = pd.read_csv(os.path.join(subdir[0], subdir[2][3]), sep=';')
        dict_data[subdir[0]] = {'gps-data': df_gps_data, 'passenger_count': df_passenger_count, 'wifi-data': df_wifi_data}
    return dict_data

def load_map(path_map_data, path_map):
    data = pd.read_csv(path_map_data, names=['LATITUDE', 'LONGITUDE'], sep=',')
    gps_data = tuple(zip(data['LATITUDE'].values, data['LONGITUDE'].values))
    image = Image.open(path_map, 'r')  # Load map image.
    img_points = []
    for d in gps_data:
        x1, y1 = scale_to_img(d, (image.size[0], image.size[1]))  # Convert GPS coordinates to image coordinates.
        img_points.append((x1, y1))
    draw = ImageDraw.Draw(image)
    draw.line(img_points, fill=(255, 0, 0), width=2)  # Draw converted records to the map image.
    
    image.save('resultMap.png')
    return data

def get_stations(data_single_trip):
    gps_data = data_single_trip['gps-data']
    passenger_count = data_single_trip['passenger_count']
    
    #Get stations. When the door is openend, it is assumed that a station is reached
    df_stops = passenger_count.loc[passenger_count['Number_of_Passengers'] == -99]
    station_dates = list(map(lambda x: datetime.datetime.fromtimestamp(float(x)), df_stops['Epoch_Time']))
    #Counts are made two hours after gps date measurement
    station_dates_corrected = list(map(lambda x: x.replace(hour=x.hour - 2), station_dates))
    station_dates_strings = list(map(lambda x: x.strftime('%Y-%m-%d %H:%M:%S'), station_dates_corrected))
    gps_data_stations = gps_data[gps_data['date_time'].isin(station_dates_strings)]
    return gps_data_stations, df_stops

def get_workload_manual_count(data_passenger_count, fig_name='workload'):
    #At first all static moments where no measurements are made (doors openeed, doores closed) are dismissed
    data_measurements_only = data_passenger_count[~data_passenger_count['Number_of_Passengers'].isin(['nan', -99.0, -10.0])]
    array_workload = data_measurements_only['Number_of_Passengers'].values

    #It is assumed, that the highest value is also the maximum capacity
    num_capacity = np.amax(array_workload)
    array_normalized = array_workload/num_capacity

    plt.ioff()
    fig = plt.figure()
    plt.plot(array_normalized, color='red')
    plt.xlabel('Timestamps')
    plt.ylabel('Workload')
    plt.title('Workload per timestamp')
    fig.savefig(fig_name)

    return array_normalized

def get_workload_wifi_data(data_single_trip, stations, fig_name='workload'):
    """
    First step: Cluster data. Wifi dateframe is split into parts, the splits happen at every station
    """
    gps_data = data_single_trip['gps-data']
    wifi_data = data_single_trip['wifi-data']
    epoch_times_stations = stations['Epoch_Time'].values

    list_mac_addresses = wifi_data.mac_address.unique
    dict_stations = {}
    times_between_stations = zip(np.insert(epoch_times_stations[:-1], 0, 0, axis=0), epoch_times_stations)
    for counter, tuple_time_between_station in enumerate(times_between_stations):
        station_measurement = wifi_data[(wifi_data['epoch_ts']>float(tuple_time_between_station[0])) & (wifi_data['epoch_ts']<float(tuple_time_between_station[1]))]
        dict_stations[counter] = station_measurement
        

    