""" transport_utils.py
Gets the transportation time using Google Maps API.
"""

import requests

def get_transport_time(start_addr: str, end_addr: str, mode: str, api_key: str) -> float:
    """
        Gets transportation time from the start address to the end address in minutes using the Google Maps API.

        Args:
            start_addr (str): address of the start location
            end_addr (str): address of the end location
            mode (str): mode of transporation (i.e.walking, driving, bicycling, transit)
            api_key (str) api key for Google Maps
    """ 
    url = 'https://maps.googleapis.com/maps/api/distancematrix/json'
    params = {
        'origins': start_addr,
        'destinations': end_addr,
        'mode': mode,
        'key': api_key
    }

    response = requests.get(url, params=params)
    json_response = response.json()

    if json_response['status'] == 'OK':
        # get extract transportation time in minutes
        transport_time = json_response['rows'][0]['elements'][0]['duration']['value']/60
        return transport_time
    else:
        return -1
