import numpy as np
from datastore import DataStore
import matplotlib.pyplot as plt
import pandas as pd
from utils import *

class DataProvider:

    def __init__(self, path_root=''):
        obj_datastore = DataStore(debug=False, path_root=path_root)
        self.data = obj_datastore.data
        self.wifi = obj_datastore.wifi

    def get_workload_manual_counting(self, str_bus_trip: str, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        df_trip = self.data[self.data['line'] == str_bus_trip]
        df_trip_timeslot = df_trip[(df_trip['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]
        df_between_stations = df_trip_timeslot[~df_trip_timeslot['Number_of_Passengers'].isin([-1])]
        return df_between_stations

    def get_stations(self, str_bus_trip: str, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        df_trip = self.data[self.data['line'] == str_bus_trip]
        df_trip_timeslot = df_trip[(df_trip['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]
        df_stations = df_trip_timeslot[df_trip_timeslot['Number_of_Passengers'].isin([-1])]
        df_stations = df_stations[df_stations['speed_over_ground_knots'] < 1.0]
        return df_stations

    def get_real_world_data(self, df):
        real_workload = df['Number_of_Passengers'].values
        curr_workload = 0
        for counter, i in enumerate(real_workload):
            if i != -1:
                curr_workload = i
                continue
            if i == -1:
                real_workload[counter] = curr_workload
        return df[['epoch_ts', 'Number_of_Passengers']]

    def get_workload_wifi_data(self, str_bus_trip: str, df_stations, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        df_trip = self.data[self.data['line'] == str_bus_trip]
        df_trip_timeslot = df_trip[(df_trip['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]


        list_mac_addresses = df_trip_timeslot.mac_address.unique()
        dict_mac_addresses = {}

        start_end_timestamp_wifi = df_trip_timeslot.iloc[[0, -1]].epoch_ts
        last_timestamp_wifi = df_trip_timeslot.iloc[-1].epoch_ts
        len_timeinterval = np.diff(start_end_timestamp_wifi).astype('timedelta64[s]').astype('int')
        counting_array = np.zeros(len_timeinterval)

        for mac_address in list_mac_addresses:
            df_mac_address = df_trip[df_trip_timeslot['mac_address'] == mac_address]
            #time_diff: Time in seconds from to first detection of the device with this address till the last detection. This is used as
            #hop-on and hop-off time of the costumer with this sepcific device
            time_diff = np.sum(np.diff(df_mac_address['epoch_ts'].values).astype('timedelta64[s]')).astype('int')
            num_frames = len(df_mac_address.frame_nr.unique())
            average_rssi = np.mean(df_mac_address['rssi'].values)
           
            #Just a random time to decide wether a measured time slot is a ride or not
            if time_diff > 30:
                 #Insert it to counting array
                arr_begin_wifi_first_mes = np.array([start_end_timestamp_wifi[0], df_mac_address.iloc[0].epoch_ts])
                start_mes = np.diff(arr_begin_wifi_first_mes).astype('timedelta64[s]').astype('int')
                end_mes = start_mes + time_diff + 1
                counting_array[int(start_mes) : int(end_mes)] += 1

                dict_mac_addresses[mac_address] = {'hop-on': df_mac_address.iloc[0],
                                                    'hop-off': df_mac_address.iloc[-1],
                                                    'diff_seconds': time_diff}

        real_world_data = self.get_real_world_data(df_trip_timeslot)

        fig = plt.figure()
        plt.plot(real_world_data['Number_of_Passengers'].values)
        plt.xlabel('Time')
        plt.ylabel('Passenger count')
        #plt.title(f'Passenger count for {str_bus_trip} from {start_time.strftime('%Y.%m.%d %H:%M%s')} to {end_time.strftime('%Y.%m.%d %H:%M%s')}')
        fig.savefig('passenger_count_real')

        fig = plt.figure()
        plt.plot(counting_array)
        plt.xlabel('Time')
        plt.ylabel('Passenger count')
        #plt.title(f'Passenger count for {str_bus_trip} from {start_time.strftime('%Y.%m.%d %H:%M%s')} to {end_time.strftime('%Y.%m.%d %H:%M%s')}')
        fig.savefig('passenger_count')

        workload = counting_array/np.max(counting_array)
        fig = plt.figure()
        plt.plot(workload)
        plt.xlabel('Time')
        plt.ylabel('occupancy')
        #plt.title(f'Passenger count for {str_bus_trip} from {start_time.strftime('%Y.%m.%d %H:%M%s')} to {end_time.strftime('%Y.%m.%d %H:%M%s')}')
        fig.savefig('occupancy')

        return dict_mac_addresses

        

            
        