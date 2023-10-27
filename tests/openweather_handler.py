from datetime import datetime

from core.message import Message
from core.config import envar
from services.logger import log


OPENWEATHER_API_KEY = envar("OPENWEATHER_API_KEY")


async def format_weather_message(response):
    main_data = response.get("main", {})
    wind_data = response.get("wind", {})
    clouds_data = response.get("clouds", {})
    sys_data = response.get("sys", {})
    sunrise = datetime.utcfromtimestamp(sys_data.get("sunrise", 0)).strftime("%H:%M:%S")
    sunset = datetime.utcfromtimestamp(sys_data.get("sunset", 0)).strftime("%H:%M:%S")

    parsed_data = (
        f"Current Temp: {main_data.get('temp')}°C\n"
        f"High: {main_data.get('temp_max')}°C\n"
        f"Low: {main_data.get('temp_min')}°C\n"
        f"Feels Like: {main_data.get('feels_like')}°C\n"
        f"Pressure: {main_data.get('pressure')} hPa\n"
        f"Humidity: {main_data.get('humidity')}%\n"
        f"Wind Speed: {wind_data.get('speed')} m/s\n"
        f"Cloud Coverage: {clouds_data.get('all')}%\n"
        f"Sunrise: {sunrise}\n"
        f"Sunset: {sunset}"
    )

    message_content = {
        "role": "system",
        "content": parsed_data,
        "name": "function_call",
    }
    reply = Message("scint", "user", message_content)

    return reply


async def get_weather(city):
    log.info(f"Calling OpenWeather API.")

    mock_data = {
        "main": {
            "temp": 20,
            "temp_max": 22,
            "temp_min": 18,
            "feels_like": 19,
            "pressure": 1012,
            "humidity": 60,
        },
        "wind": {"speed": 5},
        "clouds": {"all": 20},
        "sys": {"sunrise": 1634879180, "sunset": 1634919600},
    }

    return await format_weather_message(mock_data)


# city = "London"
# weather_data = asyncio.run(get_weather(city))
# print(weather_data)
