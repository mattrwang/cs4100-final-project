""" transport_utils.py
Gets the functions to get transportation time using Google Maps API.
"""

import requests    
from datetime import datetime, timedelta

def get_transport_time(start_addr: str, end_addr: str, mode: str, api_key: str, departure_time:int=0) -> float:
    """
        Gets transportation time from the start address to the end address in minutes using the Google Maps API.

        Args:
            start_addr (str): address of the start location
            end_addr (str): address of the end location
            mode (str): mode of transporation (i.e.walking, driving, bicycling, transit)
            api_key (str) api key for Google Maps
            departure_time (int): unix time of departure (default 12pm next Sunday)
    """ 
    departure_time = get_next_sunday()

    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': start_addr,
        'destinations': end_addr,
        'mode': mode,
        'key': api_key,
        'departure_time': departure_time
    }

    response = requests.get(url, params=params)
    json_response = response.json()

    if json_response['status'] == 'OK':
        # get extract transportation time in minutes
        transport_time = json_response['rows'][0]['elements'][0]['duration']['value']/60
        return transport_time
    else:
        return -1

def get_next_sunday():
    # create depature time at 12pm next Sunday
    current_date = datetime.now()
    # compute days until next sunday
    days_until_sunday = (6 - datetime.now().weekday()) % 7 
    next_sunday = current_date + timedelta(days=days_until_sunday)
    # set the departure time to 12:00 PM on the next Sunday
    departure_time = next_sunday.replace(hour=12, minute=0, second=0, microsecond=0)
    # donvert the departure time to seconds since the Unix epoch
    departure_time_unix = int(departure_time.timestamp())
    return departure_time_unix