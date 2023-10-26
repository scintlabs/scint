import aiohttp
import json
from datetime import datetime

from services.config import OPENWEATHER_API_KEY
from services.logger import log
from core.message import Message


async def eval_function_call(res_message):
    log.info("Evaluating function call.")

    function_call = res_message.get("function_call")
    function_name = function_call.get("name")
    function_args = function_call.get("arguments")
    function_args = json.loads(function_args)

    if not function_name or not function_args:
        log.error("Function name or arguments missing.")
        return

    if function_name.strip() == "get_weather":
        log.info("Proceeding to fetch weather...")

        city = function_args.get("city")

        if not city:
            log.error("City argument missing for get_weather function.")
            return

        try:
            log.info(f"Fetching weather for city: {city}")
            response = await get_weather(city)
            return response

        except Exception as e:
            log.error(f"Error while fetching weather: {e}")
    else:
        log.error("Function name is not 'get_weather'.")


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
    base_url = "http://api.openweathermap.org/data/2.5/weather"
    params = {"q": city, "appid": OPENWEATHER_API_KEY, "units": "metric"}

    async with aiohttp.ClientSession() as session:
        async with session.get(base_url, params=params) as response:
            data = await response.json()

            log.info(f"OpenWeather API response status: {response.status}")
            log.info(f"OpenWeather API response data: {data}")

            if response.status == 200:
                reply = await format_weather_message(data)
                log.info(f"Formatted weather message: {reply}")
                return reply
            else:
                error_message_content = {
                    "role": "system",
                    "content": data.get("message", "Error fetching weather data"),
                    "name": "function_call",
                }
                error_reply = Message("scint", "user", error_message_content)
                log.error(f"Error fetching weather: {error_reply}")
                return error_reply
