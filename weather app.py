from tkinter import *
from tkinter import ttk
import requests
from datetime import datetime


# Function to format time based on UTC and timezone
def time_format_for_location(utc_with_tz):
    local_time = datetime.utcfromtimestamp(utc_with_tz)
    return local_time.strftime("%H:%M:%S")


# Function to fetch and display weather info
def show_weather():
    api_key = "52248d413ef983bf3feea11157a73738"  # Replace with your actual API key
    city_name = city_value.get()

    if not city_name:
        tfield.delete("1.0", "end")
        tfield.insert(INSERT, "City name cannot be empty!")
        return

    weather_url = f'http://api.openweathermap.org/data/2.5/weather?q={city_name}&appid={api_key}'
    try:
        response = requests.get(weather_url)

        # Check for HTTP errors (e.g., 404, 500)
        if response.status_code == 404:
            weather = f"City '{city_name}' not found. Please enter a valid city name."
        elif response.status_code != 200:
            weather = f"Error fetching weather data: {response.status_code} {response.reason}"
        else:
            weather_info = response.json()

            kelvin = 273.15
            temp = int(weather_info['main']['temp'] - kelvin)
            feels_like_temp = int(weather_info['main']['feels_like'] - kelvin)
            pressure = weather_info['main']['pressure']
            humidity = weather_info['main']['humidity']
            wind_speed = round(weather_info['wind']['speed'] * 3.6, 2)
            sunrise_time = time_format_for_location(weather_info['sys']['sunrise'] + weather_info['timezone'])
            sunset_time = time_format_for_location(weather_info['sys']['sunset'] + weather_info['timezone'])
            cloudy = weather_info['clouds']['all']
            description = weather_info['weather'][0]['description']

            weather = (
                f"\nWeather of: {city_name}\n"
                f"Temperature: {temp}°C\n"
                f"Feels like: {feels_like_temp}°C\n"
                f"Pressure: {pressure} hPa\n"
                f"Humidity: {humidity}%\n"
                f"Wind Speed: {wind_speed} km/h\n"
                f"Sunrise: {sunrise_time}\n"
                f"Sunset: {sunset_time}\n"
                f"Cloudiness: {cloudy}%\n"
                f"Description: {description}"
            )

    except requests.exceptions.RequestException as e:
        weather = f"Error fetching weather data: {str(e)}"

    tfield.delete("1.0", "end")
    tfield.insert(INSERT, weather)


# Tkinter App Interface
app = Tk()
app.geometry("800x400")
app.resizable(0, 0)
app.title("Weather App")

# Set a custom style for the app
style = ttk.Style()
style.configure("TLabel", font=("Arial", 12), padding=5)
style.configure("TButton", font=("Arial", 10), padding=5)
style.configure("TEntry", font=("Arial", 14), padding=5)

# Input Section
Label(app, text="Enter City Name", font="Arial 12 bold", bg="lightblue", fg="black", pady=10).pack(fill=X)
city_value = StringVar()
Entry(app, textvariable=city_value, width=24, font="Arial 14 bold", relief="solid", bd=2).pack(pady=10)
Button(
    app,
    command=show_weather,
    text="Check Weather",
    font="Arial 12 bold",
    bg="darkblue",
    fg="white",
    activebackground="teal",
    activeforeground="white",
    padx=5,
    pady=5,
).pack(pady=20)

# Output Section
Label(app, text="The Weather is:", font="Arial 12 bold", bg="lightgreen", fg="black", pady=10).pack(fill=X)
tfield = Text(app, width=60, height=10, font="Arial 10", relief="groove", bd=2, wrap=WORD, bg="white", fg="black")
tfield.pack(pady=10)

# Add a footer label
Label(app, text="Powered by OpenWeatherMap API", font="Arial 8", bg="lightgrey").pack(side=BOTTOM, fill=X)

app.mainloop()
