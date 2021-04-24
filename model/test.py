from utils import *
from gps_class import GPSVis
path_data = r"C:\Users\Admin\Documents\Sciencehack\trunk\data_4_ScienceHack2021"
from PIL import Image, ImageDraw

path_map_data = r"C:\Users\Admin\Documents\Sciencehack\trunk\map"
path_map = r"C:\Users\Admin\Documents\Sciencehack\trunk\map.png"
dict_data = read_data(path_data)
#load_map(path_map_data, path_map)

list_colors = [(255, 0, 0),
               (0, 255, 0),
               (0, 0, 255),
               (255, 255, 0),
               (255, 0, 255),
               (0, 102, 102),
               (255, 255, 255),
               (0,0,0),
               (128, 0, 0),
               (0,128, 0),
               (0,0,128),
               (128, 128, 128)
               ]
img = Image.open(path_map, 'r')
vis = GPSVis(map_path=path_map,  # Path to map downloaded from the OSM.
             points=(48.2228, 11.3870, 48.0622, 11.7437),
             data_path=None,
             img= img) # Two coordinates of the map (upper left, lower right)

for counter, i in enumerate(dict_data):
    str_name = os.path.basename(i)
    df_gps_data_stations, df_stops = get_stations(dict_data[i])
    get_workload_manual_count(dict_data[i]['passenger_count'], str_name)
    get_workload_wifi_data(dict_data[i], df_stops, str_name) 
    df_gps_data = dict_data[i]['gps-data']
    fields = ['latitude', 'longitude']
    df_data_route = df_gps_data[fields]
    df_data_stations = df_gps_data_stations[fields]
    vis.create_image(df_data_route, df_data_stations, str_name, color=list_colors[counter], width=3)  # Set the color and the width of the GNSS tracks.

vis.result_image.save('result_img.png')
print('Test')


