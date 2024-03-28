""" transport_utils.py
Gets the functions to get transportation time using Google Maps API.
"""

import requests    
from datetime import datetime, timedelta
from geopy.geocoders import Nominatim
from geopy.distance import geodesic

def estimate_transport_time(start_addr: str, end_addr: str, mode: str) -> float:
    """
        Estimated transportation time from the start address to the end address in minutes using the average
        speed per mode and distance between start and end addresses.

        Args:
            start_addr (str): address of the start location
            end_addr (str): address of the end location
            mode (str): mode of transporation (i.e.walking, driving, bicycling, transit)
    """ 
    mode2speed = {'walking':3.1, 'bicyling':10.0, 'driving':45.0}
    distance = get_distance(start_addr, end_addr)
    est_time = distance/mode2speed[mode]*60 if distance >= 0 else -1
    return est_time

def get_distance(start_addr: str, end_addr: str):

    geolocator = Nominatim(user_agent="distance_calculator")

    location1 = geolocator.geocode(start_addr)
    location2 = geolocator.geocode(end_addr)

    if location1 and location2:
        coords1 = (location1.latitude, location1.longitude)
        coords2 = (location2.latitude, location2.longitude)
        distance = geodesic(coords1, coords2).miles
    else:
        distance = -1
    return distance

def get_transport_time_google(start_addr: str, end_addr: str, mode: str, api_key: str, departure_time:int=0) -> float:
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