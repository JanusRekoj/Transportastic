import pandas as pd 

class DataStore:
    def __init__(self, debug=False):
        path_root = ''
        trips = ["trip_1","trip_2","trip_3","trip_4","trip_5","trip_6","trip_7","trip_8","trip_9","trip_10","trip_11","trip_12"]
        df1 = []
        df2 = []
        df3 = []
        for trip in trips:
            df1.append(pd.read_csv(path_root+'data/' + trip + '/gps_data.csv',';'))
            df2.append(pd.read_csv(path_root+'data/' + trip + '/passenger_count_nums',';'))
            df3.append(pd.read_csv(path_root+'data/' + trip + '/wifi_data.csv',';'))
        gpsdata = pd.concat(df1)
        passenger = pd.concat(df2)
        wifi = pd.concat(df3)
        if debug:
            print(gpsdata)
            print(passenger)
            print(wifi)

if __name__ == "__main__":
    ds = DataStore(debug=True)