import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = '0fc842512fbabfce10fcb31079322c80'
GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
HISTORICAL_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'


def get_lat_lon(location):
    """
    :param location: The location for which latitude and longitude are needed.
    :return: A tuple containing the latitude and longitude values of the specified location.

    This method sends a GET request to a geocoding API to retrieve latitude and longitude coordinates for a given location. The location parameter should be a string representing the name
    * or address of the desired location.

    If successful, the method will return a tuple containing the latitude and longitude values as (latitude, longitude). If the request fails or no data is returned from the API, the method
    * will return a default set of coordinates (0.0, 0.0).

    Example usage:
        >>> get_lat_lon("New York City")
        (40.7128, -74.0060)
    """
    url = f'{GEOCODE_URL}?q={location}&limit=1&appid={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        print(f"Response: {data}")  # Log the response for debugging purpose
        if response.status_code == 200 and len(data) > 0:
            return data[0]['lat'], data[0]['lon']
    except requests.exceptions.RequestException as err:
        print("Request error:", err)
    except Exception as err:
        print("Unknown error:", err)

    # return default coordinates in case of any errors or no data from API
    return 0.0, 0.0


def get_weather_data(lat, lon, date):
    """
    This method retrieves weather data for a given latitude, longitude,
    and date from a historical weather API.

    :param lat: latitude of the location
    :param lon: longitude of the location
    :param date: date for which weather data is required
    :return: weather data in JSON format

    :raises Exception: if there is an error in retrieving weather data
    """
    url = f'{HISTORICAL_WEATHER_URL}?lat={lat}&lon={lon}&dt={int(date.timestamp())}&appid={API_KEY}'
    try:
        response = requests.get(url)
        data = response.json()
        if response.status_code == 200:
            return data
        else:
            raise Exception(f"Error getting weather data for date: {date}")
    except requests.exceptions.RequestException as err:
        print("Request error:", err)
    except Exception as err:
        print("Unknown error:", err)


# Example usage
location = 'London'
start_date = datetime(2023, 6, 1)
end_date = datetime(2023, 6, 30)

# Get latitude and longitude for the location
lat, lon = get_lat_lon(location)

# Loop through each date in the range and get the weather data
date = start_date
all_data = []
while date <= end_date:
    try:
        data = get_weather_data(lat, lon, date)
        all_data.append(data)
    except Exception as e:
        print(e)
    date += timedelta(days=1)

# Convert the collected data into a DataFrame
# Flatten the JSON data and create a pandas DataFrame
weather_data = []
for day_data in all_data:
    # Check if day_data is not None to avoid TypeError
    if day_data is not None:
        for hourly_data in day_data['hourly']:
            weather_data.append({
                'date': datetime.fromtimestamp(hourly_data['dt']),
                'temperature': hourly_data['temp'],
                'humidity': hourly_data['humidity'],
                'pressure': hourly_data['pressure'],
                'weather': hourly_data['weather'][0]['description']
            })

df = pd.DataFrame(weather_data)
print(df)
