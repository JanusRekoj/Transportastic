import numpy as np
from datastore import DataStore

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

    def get_workload_wifi_data(self, str_bus_trip: str, df_stations, start_time=np.datetime64('1900-01-01T00:00:00+00'), end_time=np.datetime64('2100-12-31T23:59:59')):
        df_trip = self.data[self.data['line'] == str_bus_trip]
        df_trip_timeslot = df_trip[(df_trip['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]

        df_trip_wifi = self.wifi[self.wifi['line'] == str_bus_trip]
        df_wifi_timeslot = df_trip_wifi[(df_trip_wifi['epoch_ts']>start_time) & (df_trip['epoch_ts']<end_time)]

        