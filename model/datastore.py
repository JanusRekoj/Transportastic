import pandas as pd 

class DataStore:
    def __init__(self, debug=False, path_root=''):
        trips = ["trip_1","trip_2","trip_3","trip_4","trip_5","trip_6","trip_7","trip_8","trip_9","trip_10","trip_11","trip_12"]

        #= Parse the data =#
        df1l = []; df2l = []; df3l = []
        df2_time = []
        for trip in trips:
            df1 = (pd.read_csv(path_root+'data/' + trip + '/gps_data.csv',','))
            df1 = df1.drop('date_time', 1)
            df1['epoch_ts'] = pd.to_datetime(df1['epoch_ts'], unit = 's')
            df1l.append(df1)

            df2 = pd.read_csv(path_root+'data/' + trip + '/passenger_count_nums',',',comment='S') # Ignore Starting Time
            df2['epoch_ts'] = pd.to_datetime(df2['Epoch_Time'].astype(float).round().astype(int), unit = 's')
            df2 = df2.drop('Epoch_Time', 1)
            with open(path_root + 'data/' + trip + '/passenger_count_nums', 'r') as f:
                line = f.readlines()[1]
                df2_time.append(line)
                if debug:
                    print(line)
            df2l.append(df2)

            df3 = (pd.read_csv(path_root+'data/' + trip + '/wifi_data.csv',';'))
            df3['epoch_ts'] = pd.to_datetime(df3['epoch_ts'], unit = 's')
            df3 = df3.drop('arr_ts', 1)
            df3l.append(df3)
        
        #= Merge each dataframe =#
        gpsdata   = pd.concat(df1l)
        passenger = pd.concat(df2l)
        wifi      = pd.concat(df3l)
        
        if debug:
            print(gpsdata)
            print(passenger)
            print(wifi)
        
        #= Merge to one and remove irrelevant data =#
        self.data = pd.merge(gpsdata, passenger, how='left', on=['epoch_ts'])
        if debug:
            print(self.data)
            print(self.data.head(50))
        
        idx_close = self.data[self.data['Number_of_Passengers']==-10].index.values
        idx_open = self.data[self.data['Number_of_Passengers']==-99].index.values
        idx_value = self.data[self.data['Number_of_Passengers']>=0].index.values

        for i_c, i_o, i_v in zip(idx_close, idx_open, idx_value):
            print(f'Setting {i_c} : {i_o} = {i_v}')
            self.data.loc[(i_c+1):(i_o-1), 'Number_of_Passengers'] = self.data['Number_of_Passengers'][i_v]

        self.data.loc[self.data['Number_of_Passengers']<0, 'Number_of_Passengers'] = -1
        self.data['Number_of_Passengers'] = self.data['Number_of_Passengers'].fillna(-1)
        self.data = self.data.drop(['lat_dir','lon_dir'],1)

        if debug:
            print(self.data.head(50))


if __name__ == "__main__":
    ds = DataStore(debug=True)