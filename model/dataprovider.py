import numpy as np
from model.datastore import DataStore
import matplotlib.pyplot as plt
import pandas as pd
from model.utils import *
from operator import add
import itertools

class DataProvider:

    def __init__(self, path_root=''):
        self.obj_datastore = DataStore(debug=False, path_root=path_root, fake_data=False)
        self.data = self.obj_datastore.data
        self.wifi = self.obj_datastore.wifi
    
    def get_lines(self):
        return self.data['line'].dropna().unique()

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

    def cluster_data(self, str_bus_trip: str, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        df_trip = self.data[self.data['line'] == str_bus_trip]
        df_time_intverval = df_trip[(df_trip['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]
        num_station = 1
        num_ride = 1
      
        df_phase_transition = df_time_intverval['Number_of_Passengers'].diff()
        list_indices_phase_transition = df_phase_transition[df_phase_transition != 0].index 
        list_indices_phase_transition = list_indices_phase_transition - list_indices_phase_transition[0]
        cluster_indices = list(zip(list_indices_phase_transition[:-1], list_indices_phase_transition[1:]))

        dict_rides = {}
        dict_stations = {}
        for indices in cluster_indices:
            phase = df_time_intverval.iloc[indices[0] : indices[1]]
            if phase.iloc[0].Number_of_Passengers < 0:
                dict_stations[f'station_{num_station}'] = phase
                num_station += 1
            else:
                dict_rides[f'ride_{num_ride}'] = phase
                num_ride += 1
        return dict_stations, dict_rides

    def get_occupancy_wifi_data_third_approach(self, str_bus_trip: str, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        dict_stations, dict_rides = self.cluster_data(str_bus_trip, start_time, end_time)
        mac_addresses_per_ride = list(map(lambda x: dict_rides[x].mac_address.unique(), dict_rides))
        mac_addresses_per_station = list(map(lambda x: dict_stations[x].mac_address.unique(), dict_stations))
        
        manual_counted_passengers_per_ride = list(map(lambda x: dict_rides[x].Number_of_Passengers.values[0], dict_rides))

        combined_addresses = list(zip(mac_addresses_per_ride[:-1], mac_addresses_per_ride[1:]))
        combine_station_before_and_rides = list(zip(mac_addresses_per_ride, mac_addresses_per_station))
        combine_station_after_and_rides = list(zip(mac_addresses_per_ride[:-1], mac_addresses_per_station[1:]))
        #Not valid for first ride!!!
        passengers_per_ride_ride_compared = [0] + list(map(lambda x: len(list(set(list(x[0])).intersection(list(x[1])))), combined_addresses))
        passengers_per_ride_compare_station_before = list(map(lambda x: len(list(set(list(x[0])).intersection(list(x[1])))), combine_station_before_and_rides))
        passengers_per_ride_compare_station_after = list(map(lambda x: len(list(set(list(x[0])).intersection(list(x[1])))), combine_station_after_and_rides)) + [0]

        passengers_per_ride = list(map(add, map(add, passengers_per_ride_ride_compared, passengers_per_ride_compare_station_before), passengers_per_ride_compare_station_after))

        seconds_per_ride = list(map(lambda x: np.sum(np.diff(dict_rides[x]['epoch_ts'].values[[0, -1]]).astype('timedelta64[s]')).astype('int'), dict_rides))
        seconds_per_station = list(map(lambda x: np.sum(np.diff(dict_stations[x]['epoch_ts'].values[[0, -1]]).astype('timedelta64[s]')).astype('int'), dict_stations))
        list_seconds = []
        sum_list = [list_seconds  + [a[1] + a[0]] for a in zip(seconds_per_ride, seconds_per_station[1:] + [0])]
        seconds = list(itertools.chain(*sum_list))

        curve_counted_values = np.zeros(np.sum(seconds))
        curve_measured_values = np.zeros(np.sum(seconds))

        for counter, step in enumerate(seconds):
            curve_counted_values[int(seconds[counter - 1]) : int(step)] = passengers_per_ride[counter]
            curve_measured_values[int(seconds[counter - 1]) : int(step)] = manual_counted_passengers_per_ride [counter]

        fig = plt.figure()
        plt.plot(curve_counted_values, color='r')
        plt.plot(curve_measured_values, color='b')
        plt.xlabel('Time')
        plt.ylabel('Passenger count')
        #plt.title(f'Passenger count for {str_bus_trip} from {start_time.strftime('%Y.%m.%d %H:%M%s')} to {end_time.strftime('%Y.%m.%d %H:%M%s')}')
        fig.savefig('passenger_count')

    def get_occupancy_wifi_data_second_approach(self, str_bus_trip: str, df_stations, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
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


        return dict_mac_addresses, counting_array

    def get_occupancy_wifi_data_first_approach(self, str_bus_trip: str, df_stations, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        #@Nika pls add your code here :D
        pass
        

            
        