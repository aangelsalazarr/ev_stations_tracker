import requests
import pandas as pd
import seaborn as sns
from functions import *
import time

# recording the start time
start = time.time()

# api key from NREL
# associated with aa**********rr@gmail.com
key = 'bcnLjN07rYalJDg3Xpc4sxzbCSDkRf4OUYsZ5GTM'

# creating a list of 2 letter state codes
states = [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'FL', 'GA',
    'HI', 'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD',
    'MA', 'MI', 'MN', 'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ',
    'NM', 'NY', 'NC', 'ND', 'OH', 'OK', 'OR', 'PA', 'RI', 'SC',
    'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 'WV', 'WI', 'WY'
]

# main df where we will be storing all data into 1 main df
main_df = pd.DataFrame()

# iterating through each state code and creating a map
for x in states:

    # variables going into url request
    f_type = 'ELEC' #fuel type
    state = str(x)
    network = 'all' 

    # let's find only tesla ev stations
    url = f"https://developer.nrel.gov/api/alt-fuel-stations/v1.json?api_key={key}&fuel_type={f_type}&state={state}&ev_network={network}"


    # make a request
    r = requests.get(url=url)
    data = r.json()

    entries = data['fuel_stations']

    # converting into a df
    df = pd.DataFrame(data=entries) 

    # adding this df instance to our main df
    main_df = pd.concat([main_df, df], axis=0)

    # let's map what we have captured
    gen_path = f"ev_station_tracker/general_maps/{state}_ev_stations.html"
    heat_path = f"ev_station_tracker/heat_maps/{state}_ev_stations_heat.html"
    excel_path = f"ev_station_tracker/data_files/{state}_ev_station_data.xlsx"

    # outputting as an excel file
    df.to_excel(excel_path, index=False)

    # creating a general map
    gen_map(dataframe=df, savepath=gen_path)

    # creating a heat map
    heat_map(dataframe=df, savepath=heat_path)

    # let user know data for state successfully processed
    print(f"Data for {x} successfully processed!")

    # adding a delay period to make sure the requests don't clog server
    time.sleep(10)


# resetting index of our main df
main_df.reset_index(drop=True, inplace=True)

# let's map what the entirety of the united states
main_df.to_excel('ev_station_tracker/data_files/USA_ev_station_data.xlsx', index=False)

# creating our heat map
heat_map(dataframe=main_df, savepath="ev_station_tracker/heat_maps/USA_ev_stations_heat.html")


# record the end time
end = time.time()

# printing time it took to run code
print("time of execution:", (end - start), "seconds")
