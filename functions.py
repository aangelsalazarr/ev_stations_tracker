import requests
import pandas as pd
import seaborn as sns
import folium 

# importing necessary code for creating a heat map
from folium import plugins
from folium.plugins import HeatMap

def gen_map(dataframe, savepath, color='red', tiles='OpenStreetMap', size=(10, 10)):

    # creating dictionary of types of [insert here] to color our markers
    color = {
        'public': 'green', 
        'private': 'red'
    }

    # create a map centered on the USA
    map = folium.Map(location=[39.8283, -98.5795], 
                     zoom_start = 3,
                      tiles = tiles)
    
    # iterating through our df to add markers to the map
    for index, row in dataframe.iterrows():

        # setup the content of the popup
        iframe = folium.IFrame(f'Station Name: {str(row["station_name"])} <br> Station Open Date: {str(row["open_date"])} <br> Fuel Type: {str(row["fuel_type_code"])} <br> Access: {str(row["access_days_time"])} <br> Network Provider: {str(row["ev_network"])} <br> Pricing: {str(row["ev_pricing"])}')

        # initialize the popup using the iframe
        popup = folium.Popup(iframe, min_width=300, max_width=500)

        try: 
            # if cell value matches key from colors, then it will be colored
            # accordingly
            icon_color = color[row['access_code']]

        except: 

            # catch NANs
            icon_color = 'gray'

        folium.Marker(
            location=[row['latitude'], row['longitude']], 
            icon = folium.Icon(
            color = icon_color, 
            icon = '', 
            shadow = None, 
            size = size, 
            ), 
            popup = popup
        ).add_to(map)

    # saving map given our save path
    map.save(savepath)


def heat_map(dataframe, savepath):

    # initiaing our map
    map = folium.Map(location=[39.8283, -98.5795], zoom_start = 4)

    # making sure our df lat and long col values are in floats
    dataframe['latitude'] = dataframe['latitude'].astype(float)
    dataframe['longitude'] = dataframe['longitude'].astype(float)

    # filter the dataframe for rows, then cols, then remove NANs
    heat_df = dataframe[['latitude', 'longitude']]

    # list comprehension to make out lists of lists
    heat_data = [[row['latitude'], 
                  row['longitude']] for index, row in heat_df.iterrows()]
    
    # plot it on the map
    HeatMap(heat_data).add_to(map)

    # saving our map
    map.save(savepath)

