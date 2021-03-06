# Imports
from server import WebServer

import time
import threading
from model.dataprovider import DataProvider
import pandas as pd



class Controller:
    def __init__(self) -> None:
        # Init class attributes
        self.model = DataProvider()
        self.server = WebServer(self, host='127.0.0.1', port=10000)
        self._data_lock = threading.Lock()
        self._model_thread = threading.Thread(
            target=self._run_model, daemon=True, args=(self._data_lock, ))

        # Run model in dedicated worker thread
        self._model_thread.start()

        # Start server (blocking)
        self.server.start_server()

    def _run_model(self, lock: threading.Lock) -> None:
        while True:
            time.sleep(1)
            lock.acquire()
            # self._data += 10
            # self._data = self._data % 100
            lock.release()

    def get_data(self, start_time, end_time, lineid, busid, station):
        self._data_lock.acquire()
        data = self._get_data(start_time, end_time, lineid, busid, station)
        self._data_lock.release()
        return data
    
    def _get_data(self, start_time, end_time, lineid, busid, station):
        # timeframe =  self.model.data[(self.model.data['epoch_ts'] > start_time) & (self.model.data['epoch_ts'] <= end_time)]
        lines = self.model.get_lines()
        response = {}
        for l in lines:
            # bus_id = 'bus_' + l
            bus_id = 'Line ' + l[5:]
            response[l] = {
                bus_id: {
                    'businfo': {
                        'seats': 50,
                        'capacity': 100
                    },
                    'trajectory': []
                }
            }
            timeframe = self.model.cluster_data(l, start_time, end_time)
            # timeframe = self.model.obj_datastore.data2[(self.model.obj_datastore.data2['epoch_ts'] > start_time) & (self.model.obj_datastore.data2['epoch_ts'] <= end_time)]
            subframe = timeframe[timeframe['line'] == l]
            if not subframe.empty:
                for index, data in subframe.iterrows():
                    response[l][bus_id]['trajectory'].append({
                        'timestamp': data['epoch_ts'],
                        'position': {
                            'lat': data['latitude'],
                            'lon': data['longitude'],
                            'speed': data['speed_over_ground_knots'],
                            'heading': data['heading_true_course'],
                        },
                        'station': None,
                        'occupancy': data['Number_of_Passengers'],
                    })
        return response

if __name__ == "__main__":
    # Main Script to launch app
    Controller()
