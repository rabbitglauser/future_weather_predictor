import requests
import pandas as pd
from datetime import datetime, timedelta

API_KEY = 'ipb_live_qmRqbgoHr0fwBdE7CCRTh16QzVBrd62ZsUw5PDkC'
GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
HISTORICAL_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'


def get_lat_lon(location):
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
