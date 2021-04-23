import pandas as pd 

class DataStore:
    def __init__(self, debug=False, path_root=''):
        trips = ["trip_1","trip_2","trip_3","trip_4","trip_5","trip_6","trip_7","trip_8","trip_9","trip_10","trip_11","trip_12"]

        #= Parse the data =#
        df1 = []; df2 = []; df3 = []
        df2_time = []
        for trip in trips:
            df1.append(pd.read_csv(path_root+'data/' + trip + '/gps_data.csv',','))
            df2.append(pd.read_csv(path_root+'data/' + trip + '/passenger_count_nums',',',comment='S')) # Ignore Starting Time
            with open(path_root + 'data/' + trip + '/passenger_count_nums', 'r') as f:
                line = f.readlines()[1]
                df2_time.append(line)
                if debug:
                    print(line)
            df3.append(pd.read_csv(path_root+'data/' + trip + '/wifi_data.csv',';'))
        
        #= Merge each dataframe =#
        gpsdata   = pd.concat(df1)
        passenger = pd.concat(df2)
        wifi      = pd.concat(df3)
        gpsdata = gpsdata.drop('date_time', 1)
        gpsdata['epoch_ts'] = pd.to_datetime(gpsdata['epoch_ts'], unit = 's')
        passenger['Epoch_Time'] = pd.to_datetime(passenger['Epoch_Time'], unit = 's')
        wifi['epoch_ts'] = pd.to_datetime(wifi['epoch_ts'], unit = 's')
        wifi = wifi.drop('arr_ts', 1)
        if debug:
            print(gpsdata)
            print(passenger)
            print(wifi)
        
        #= Merge to one =#
        data      = gpsdata


if __name__ == "__main__":
    ds = DataStore(debug=True)