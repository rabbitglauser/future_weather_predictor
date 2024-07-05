import requests
import pandas as pd
from datetime import datetime, timedelta
import scipy


class WeatherCollector:
    """
    This class represents a WeatherCollector that collects historical weather data for a given location within a specified date range.

    Attributes:
        API_KEY (str): The API key for OpenWeatherMap.
        GEOCODE_URL (str): The URL for the Geocoding API of OpenWeatherMap.
        HISTORICAL_WEATHER_URL (str): The URL for the Historical Weather API of OpenWeatherMap.
        location (str): The location for which weather data is collected.
        start_date (datetime.datetime): The start date of the data collection.
        end_date (datetime.datetime): The end date of the data collection.

    Methods:
        __init__(self, location: str, start_date: datetime.datetime, end_date: datetime.datetime)
            Initializes a new instance of the WeatherCollector class.

        get_lat_lon(self) -> Tuple[float, float]
            Retrieves the latitude and longitude coordinates for the given location.

        get_weather_data(self, lat: float, lon: float, date: datetime.datetime) -> Optional[Dict]
            Retrieves the weather data for the specified latitude, longitude, and date.

        collect_weather_data(self) -> List[Dict]
            Collects weather data for each day within the specified date range.

        parse_weather_data(self, all_data: List[Dict]) -> None
            Parses the collected weather data and outputs it as a DataFrame.
    """
    API_KEY = 'ipb_live_qmRqbgoHr0fwBdE7CCRTh16QzVBrd62ZsUw5PDkC'
    GEOCODE_URL = 'http://api.openweathermap.org/geo/1.0/direct'
    HISTORICAL_WEATHER_URL = 'http://api.openweathermap.org/data/2.5/onecall/timemachine'

    def __init__(self, location, start_date, end_date):
        self.location = location
        self.start_date = start_date
        self.end_date = end_date

    def get_lat_lon(self):
        url = f'{self.GEOCODE_URL}?q={self.location}&limit=1&appid={self.API_KEY}'
        try:
            response = requests.get(url)
            data = response.json()
            print(f"Response: {data}")
            if response.status_code == 200 and len(data) > 0:
                return data[0]['lat'], data[0]['lon']
        except requests.exceptions.RequestException as err:
            print("Request error:", err)
        except Exception as err:
            print("Unknown error:", err)

        return 0.0, 0.0

    def get_weather_data(self, lat, lon, date):
        url = f'{self.HISTORICAL_WEATHER_URL}?lat={lat}&lon={lon}&dt={int(date.timestamp())}&appid={self.API_KEY}'
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

    def collect_weather_data(self):
        lat, lon = self.get_lat_lon()

        date = self.start_date
        all_data = []
        while date <= self.end_date:
            try:
                data = self.get_weather_data(lat, lon, date)
                if data is not None:
                    all_data.append(data)
            except Exception as e:
                print(e)
            date += timedelta(days=1)

        return all_data


    def parse_weather_data(self, all_data):
        weather_data = []
        for day_data in all_data:
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


# usages
if __name__ == "__main__":
    location = 'London'
    start_date = datetime(2023, 6, 1)
    end_date = datetime(2023, 6, 30)
    collector = WeatherCollector(location, start_date, end_date)
    all_data = collector.collect_weather_data()
    collector.parse_weather_data(all_data)
