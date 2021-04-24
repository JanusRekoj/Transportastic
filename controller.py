# Imports
from server import WebServer

import time
import threading
from model import datastore
import pandas as pd

dummy_response_dict = {
    'track_1': {
        'businfo': {
            'seats': 50,
            'capacity': 100
        },
        'trajectory': [{
            'timestamp': 10000,
            'position': {
                'lat': 10.0,
                'lon': 10.0,
                'speed': 10.0,
                'heading': 200.0
            },
            'station': None,
            'occupancy': 10
        },
        {
            'timestamp': 10010,
            'position': {
                'lat': 10.1,
                'lon': 10.1,
                'speed': 0.0,
                'heading': 100.0
            },
            'station': 'Hauptbahnhof',
            'occupancy': 10
        }]
    }
}


class Controller:
    def __init__(self) -> None:
        # Init class attributes
        self.model = datastore.DataStore()
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
        timeframe =  self.model.data[(self.model.data['epoch_ts'] > start_time) & (self.model.data['epoch_ts'] <= end_time)]
        lines = pd.unique(timeframe['line'])
        response = {}
        for l in lines:
            response[l] = {
                'businfo': {
                    'seats': 50,
                    'capacity': 100
                },
                'trajectory': []
            }
            for index, data in timeframe[timeframe['line'] == l].iterrows():
                response[l]['trajectory'].append({
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
