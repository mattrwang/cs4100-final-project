""" transport_utils.py
Compute transportation time between two locations.
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
            start_addr: address of the start location
            end_addr: address of the end location
            mode: mode of transporation (i.e.walking, driving, bicycling, transit)
        Returns:
            est_time: transportation time in minutes
    """ 
    mode2speed = {'walking':3.1, 'bicyling':10.0, 'driving':45.0}
    distance = get_distance(start_addr, end_addr)
    est_time = distance/mode2speed[mode]*60 if distance >= 0 else -1
    return est_time

def get_distance(start_addr: str, end_addr: str) -> float:
    """
        Computed distance between two locations in miles.

        Args:
            start_addr: address of the start location
            end_addr: address of the end location
        Returns:
            distance: distance between locations in miles
    """ 

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

def get_transport_time_google(start_addr: str, end_addr: str, mode: str, api_key: str='None') -> float:
    """
        Gets transportation time from the start address to the end address in minutes using the Google Maps API.
        Time of departure is set as Noon of next occuring Sunday so all computations made under the same traffic conditions.

        Args:
            start_addr: address of the start location
            end_addr: address of the end location
            mode: mode of transporation (i.e.walking, driving, bicycling, transit)
            api_key: api key for Google Maps
        Returns:
            transport_time: transportation time in minutes (-1 if not able to be computed)
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

def get_next_sunday(date:datetime = datetime.now()):
    """
        Gets the unix time of the next Sunday.

        Args:
            date: date to find next Sunday from
        Returns:
            sunday_unix: unix time of the next Sunday
    """ 
    # compute days until next Sunday
    days_until_sunday = (6 - date.weekday()) % 7 
    next_sunday = date + timedelta(days=days_until_sunday)
    # set the time as 12:00 PM on the Sunday
    time = next_sunday.replace(hour=12, minute=0, second=0, microsecond=0)
    # donvert the departure time to seconds since the Unix epoch
    sunday_unix = int(time.timestamp())
    return sunday_unix