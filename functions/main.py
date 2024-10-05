import os
from dotenv import load_dotenv
import requests
import pandas as pd
from datetime import datetime
import matplotlib.pyplot as plt
from geopy.geocoders import Nominatim

load_dotenv()

USERNAME = os.getenv("METEOMATICS_USERNAME")
PASSWORD = os.getenv("METEOMATICS_PASSWORD")

def get_lat_lon(city, country):
    geolocator = Nominatim(user_agent="weather_app")
    location = geolocator.geocode(f"{city}, {country}")
    if location:
        return location.latitude, location.longitude
    else:
        print("Location not found!")
        return None, None

def get_precipitation_data(lat, lon, start_date, end_date, username, password):
    base_url = "https://api.meteomatics.com"
    parameters = "precip_1h:mm"  
    time_range = f"{start_date}--{end_date}:PT1H" 

    url = f"{base_url}/{time_range}/{parameters}/{lat},{lon}/json"

    response = requests.get(url, auth=(username, password))

    if response.status_code == 200:
        data = response.json()
        #print("API Response: ", data)

        precip_data = []
        for entry in data['data']:
            for coordinate in entry['coordinates']:
                for date_data in coordinate['dates']:
                    precip_data.append({
                        "datetime": date_data['date'],
                        "precipitation_mm": date_data['value']
                    })

        df = pd.DataFrame(precip_data)
        df['datetime'] = pd.to_datetime(df['datetime']) 
        return df
    else:
        print(f"Error: {response.status_code}, {response.text}")
        return None

def analyze_flood_risk(df):
    flood_threshold = 50
    plt.figure(figsize=(10, 6))
    plt.plot(df['datetime'], df['precipitation_mm'], label="Hourly Precipitation (mm)", color='blue')
    flood_risk = df['precipitation_mm'] > flood_threshold
    if flood_risk.any():
        plt.fill_between(df['datetime'], df['precipitation_mm'], where=flood_risk, color='red', alpha=0.5, label='Flood Risk')
        plt.title("Precipitation and Flood Risk")
        plt.legend()
        plt.ylabel("Precipitation (mm)")
        plt.xlabel("Date and Time")
        plt.grid(True)
        plt.show()
        print("Warning: Possible flood risk detected! Heavy precipitation in the area.")
    else:
        plt.title("Precipitation")
        plt.legend()
        plt.ylabel("Precipitation (mm)")
        plt.xlabel("Date and Time")
        plt.grid(True)
        plt.show()
        print("No flood risk detected.")

def main():
    city = input("Enter city name: ")
    country = input("Enter country name: ")

    lat, lon = get_lat_lon(city, country)
    if lat is None or lon is None:
        return  

    start_date = input("Enter start date (YYYY-MM-DD): ")
    end_date = input("Enter end date (YYYY-MM-DD): ")

    try:
        start_date = f"{start_date}T00:00:00Z"
        end_date = f"{end_date}T23:59:59Z"
    except Exception as e:
        print(f"Error in date format: {e}")
        return

    precip_df = get_precipitation_data(lat, lon, start_date, end_date, USERNAME, PASSWORD)

    if precip_df is not None:
        analyze_flood_risk(precip_df)
    else:
        print("Failed to retrieve precipitation data.")

if __name__ == "__main__":
    main()

