from datastore import DataStore
import pandas as pd
from sklearn.metrics import mean_squared_error
from sklearn.metrics import mean_absolute_error
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats
from scipy.stats import gaussian_kde
import seaborn as sns
import matplotlib 
import scipy.stats as ss

def mac_to_int(mac_str):
    # takes mac address as tring and converts to int
    return int(''.join(mac_str.split(":")), 16)

def int_to_mac(mac_int):
    mac_hex = "{:012x}".format(mac_int)
    mac_str = ":".join(mac_hex[i:i+2] for i in range(0, len(mac_hex), 2))
    return mac_str

def get_passengers(df):
    flag = True
    current_station = set()
    next_station = set() 
    count = 1
    time = 0
    speed_flag = False
    start_index = 0
    stop_count = 0
    for index, row in df.iterrows():
        if count%2 == 1:
            current_station.add(row['mac_address'])
        else:
            next_station.add(row['mac_address'])
        if row['speed_over_ground_knots'] < 0.3:
            speed_flag = True
        if row['speed_over_ground_knots'] > 2 and speed_flag:
            count += 1
            flag = False
            speed_flag = False
        if count == 4:
            flag = True
            count = 0
            intersection = set.intersection(current_station, next_station)
            passenger_count = len(intersection)
            df.loc[start_index:index, 'passengers'] = passenger_count
            start_index = index
            current_station = set()
            next_station = set()
    return df

def MAE(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Absolute Error """
    return mean_absolute_error(actual, predicted)

def MSE(actual: np.ndarray, predicted: np.ndarray):
    """ Mean Squared Error """
    return mean_squared_error(actual, predicted)

def Evaluate(Y_true, predictions):
    print('MAE '+str(MAE(Y_true, predictions)))
    # print('MSE '+str(MSE(Y_true, predictions)))

def uniqueIndexes(l):
    seen = set()
    res = []
    for i, n in enumerate(l):
        if n not in seen:
            res.append(i)
            seen.add(n)
    return res



def calculate_accuracy(ground_truth, approximation):
    ground_truth = list(ground_truth)
    approximation = list(approximation)
    assert len(ground_truth) == len(approximation)
    # uniquie_indices = uniqueIndexes(ground_truth)
    # unique_list = []
    # unique_list2 = []
    # for i in range(len(uniquie_indices)):
    #     unique_list.append(ground_truth[uniquie_indices[i]])
    #     unique_list2.append(approximation[uniquie_indices[i]])
    # # unique_list = ground_truth[uniquie_indices]
    # print(unique_list)
    # print(unique_list2)
    Evaluate(ground_truth, approximation)

def plot(ground_truth, approximation):
    sns.set(style="white", font_scale=1.8, font='Times New Roman')
    # serif less font yu gothic


    fig, ax = plt.subplots()
    # ax.plot([0, 10, 20, 30], [0, 2, 1, 2])
    # ax.tick_params(axis ='both', which ='major', 
    #             labelsize = 16, pad = 12, 
    #             colors ='r')
    
    # ax.tick_params(axis ='both', which ='minor',
    #             labelsize = 8, colors ='b')
    matplotlib.rcParams['font.size'] = 12
    matplotlib.rcParams['figure.dpi'] = 100
    # plt.figure()
    # # sns.kdeplot(ground_truth,  label='Ground Truth', linewidth=2, linestyle="--", color='blue')
    # # sns.displot(ground_truth, label='Ground Truth')
    bins = np.linspace(0, 2, 40)
    binwidth = 2
    plt.hist(approximation, bins=[i for i in range(1,30)], histtype='bar',density=True, label='Ground Truth') ;
    sns.kdeplot(approximation, label='Predictions', linewidth=2, linestyle="-", color='red') # dot

    # # font size
    plt.legend(prop={'size': 18},loc='upper right')
    # # plt.title('Density Plot for Actual Number of Passengers vs Predicitons')
    plt.xlabel('Number of Passengers')
    plt.ylabel('Frequency');
    plt.xticks(range(30))
    plt.show()
    # plt.savefig("dist_dam.png", bbox_inches='tight')


if __name__ == "__main__":
    # ds = DataStore(debug=True)
    # data = ds.data
    # wifi = ds.wifi
    # had too save first as a CSV, due to some merging issues
    # data.to_csv('data.csv', sep='\t')
    # wifi.to_csv('wifi.csv', sep='\t')

    data = pd.read_csv('data.csv', sep = '\t')
    wifi = pd.read_csv('wifi.csv', sep='\t')
 
    wifi['epoch_ts'] = wifi['epoch_ts'].str.split('.').str[0]
    df = pd.merge(wifi, data, on=['epoch_ts'])

    addresses = list(df['mac_address'])
    for i in df.index:
        df.at[i, 'mac_address'] = mac_to_int(addresses[i])

    df = df.sort_values(by='epoch_ts',ascending=True)
    df = df.reset_index(drop=True)
    df['passengers'] = 0
    df = get_passengers(df)
    # Drop all the rows where number of passengers==-1,(unknown data samples)
    df = df[df['Number_of_Passengers'] > 0]
    # df = df[df['Number_of_Passengers'] < 20]
    calculate_accuracy(df['Number_of_Passengers'], df['passengers'])
    plot(df['Number_of_Passengers'], df['passengers'])
