# Imports
from server import WebServer

import time
import threading
from model import datastore

class Controller:
    def __init__(self) -> None:
        # Init class attributes
        # self.model = Model() # TODO: Create / Initialize model
        self.server = WebServer(self, host='127.0.0.1', port=10000)
        self._data = datastore.DataStore()
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
        #data = self._model.get_data()
        data = "Data!!"
        self._data_lock.release()
        return data


# Main Script to launch app
Controller()
