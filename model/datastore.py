import pandas as pd 
import os
import datetime

class DataStore:
    def __init__(self, debug=False, path_root='', fake_data=False, common_timestamp=datetime.datetime.now()):
        trips = sorted(os.listdir(os.path.join(path_root, 'data')), key=len)
        trips = filter(lambda x: os.path.isdir(os.path.join(path_root, 'data', x)), trips)

        #= Parse the data =#
        df1l = []; df2l = []; df3l = []
        if fake_data:
            df1lf = []; df2lf = []; df3lf = []
        df2_time = []
        self.time_adjustment = None
        for trip in trips:
            df1 = pd.read_csv(os.path.join(path_root, 'data', trip, 'gps_data.csv'), ',')
            df1 = df1.drop('date_time', 1)
            df1['epoch_ts'] = pd.to_datetime(df1['epoch_ts'], unit = 's')
            df1['line'] = trip
            df1['bus'] = 'Line ' + trip[5:]
            if common_timestamp is None:
                self.time_adjustment = df1['epoch_ts'].min() - df1['epoch_ts'].min()  # TODO nicer
            else:
                self.time_adjustment = common_timestamp - df1['epoch_ts'].min()
            df1['epoch_ts'] = df1['epoch_ts'] + self.time_adjustment
            df1l.append(df1)
            if fake_data:
                df1lf.append(df1)
                starting_time = df1['epoch_ts'].min()
                ending_time = df1['epoch_ts'].max()
                delta = ending_time - starting_time
                for i in range(1,10):
                    df1_cp = df1.copy(deep=True)
                    df1_cp['epoch_ts'] = df1['epoch_ts'] + i*delta
                    df1lf.append(df1_cp)

            df2 = (pd.read_csv(os.path.join(path_root, 'data', trip, 'passenger_count_nums'), ',',comment='S'))
            df2['epoch_ts'] = pd.to_datetime(df2['Epoch_Time'].astype(float).round().astype(int), unit = 's')
            df2 = df2.drop('Epoch_Time', 1)
            df2['epoch_ts'] = df2['epoch_ts'] + self.time_adjustment
            with open(os.path.join(path_root, 'data', trip, 'passenger_count_nums'), 'r') as f:
                line = f.readlines()[1]
                df2_time.append(line)
                if debug:
                    print(line)
            df2l.append(df2)
            if fake_data:
                df2lf.append(df2)
                starting_time = df2['epoch_ts'].min()
                ending_time = df2['epoch_ts'].max()
                delta = ending_time - starting_time
                for i in range(1,10):
                    df2_cp = df2.copy(deep=True)
                    df2_cp['epoch_ts'] = df2_cp['epoch_ts'] + i*delta
                    df2lf.append(df2_cp)

            df3 = (pd.read_csv(os.path.join(path_root, 'data', trip, 'wifi_data.csv'), ';'))
            df3['epoch_ts'] = pd.to_datetime(df3['epoch_ts'].astype(float).round().astype(int), unit = 's')
            df3 = df3.drop('arr_ts', 1)
            df3['epoch_ts'] = df3['epoch_ts'] + self.time_adjustment
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
        self._data = pd.merge(gpsdata, passenger, how='left', on=['epoch_ts'])

        if debug:
            print(self._data)
            print(self._data.head(50))
        
        idx_close = self._data[self._data['Number_of_Passengers']==-10].index.values
        idx_open = self._data[self._data['Number_of_Passengers']==-99].index.values
        idx_value = self._data[self._data['Number_of_Passengers']>=0].index.values

        # TODO Ensure suitable data: i_c < i_v < i_o !!

        for i_c, i_o, i_v in zip(idx_close, idx_open, idx_value):
            if debug:
                print(f'Setting {i_c} : {i_o} = {i_v}')
            self._data.loc[(i_c+1):(i_o-1), 'Number_of_Passengers'] = self._data['Number_of_Passengers'][i_v]

        self.data = self._data.copy()
        self.data['epoch_ts'] = pd.to_datetime(self.data['epoch_ts'], unit = 's')
        self.data = self.data.drop_duplicates(subset='epoch_ts')
        wifi['epoch_ts'] = pd.to_datetime(wifi['epoch_ts'], unit = 's')
        self.data = self.data.merge(wifi, how='left', left_on='epoch_ts', right_on='epoch_ts')

        if debug:
            print(self.data)
            print(self.data.head(50))

        self.data.loc[self.data['Number_of_Passengers']<0, 'Number_of_Passengers'] = -1
        self.data['Number_of_Passengers'] = self.data['Number_of_Passengers'].fillna(-1)
        self.data = self.data.drop(['lat_dir','lon_dir'],1)
        self.data.set_index('epoch_ts')

        if fake_data:
            gpsdata   = pd.concat(df1lf)
            passenger = pd.concat(df2lf)
            self.data2 = pd.merge(gpsdata, passenger, how='left', on=['epoch_ts'])
            idx_close = self.data2[self.data2['Number_of_Passengers']==-10].index.values
            idx_open = self.data2[self.data2['Number_of_Passengers']==-99].index.values
            idx_value = self.data2[self.data2['Number_of_Passengers']>=0].index.values
            for i_c, i_o, i_v in zip(idx_close, idx_open, idx_value):
                if debug:
                    print(f'Setting {i_c} : {i_o} = {i_v}')
                self.data2.loc[(i_c+1):(i_o-1), 'Number_of_Passengers'] = self.data2['Number_of_Passengers'][i_v]
            self.data2.loc[self.data2['Number_of_Passengers']<0, 'Number_of_Passengers'] = -1
            self.data2['Number_of_Passengers'] = self.data2['Number_of_Passengers'].fillna(-1)
            self.data2 = self.data2.drop(['lat_dir','lon_dir'],1)
            self.data2.set_index('epoch_ts')
        else:
            self.data2 = self._data.copy()
        del self._data

        self.wifi = wifi
        if debug:
            print(self.data.head(50))
            print(self.data)
    
    def get(self, start_time, end_time, lineid, busid, station):
        timeframe =  self.data[(self.data['epoch_ts'] > start_time) & (self.data['epoch_ts'] <= end_time)]
        print(timeframe)
        return dummy_response_dict


if __name__ == "__main__":
    ds = DataStore(debug=False, fake_data=True)