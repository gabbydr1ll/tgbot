import telebot
import requests
TOKEN = '1261778250:AAGvaGYSTgYaaqVltgPtEG9chv88abCu55E'

bot = telebot.TeleBot(TOKEN)
@bot.message_handler(commands=['start'])
def start_handler(message):
    bot.send_message(message.from_user.id, f"Hello, {message.from_user.first_name}. Enter /weather to find out the current weather and /forecast to get the 5 day weather forecast")
@bot.message_handler(commands=['weather'])
def weather_handler(message):
    bot.send_message(message.from_user.id,"Enter the name of the city in English with a capital letter.")
    bot.register_next_step_handler(message, bb_handler)
def bb_handler(message):
    city = message.text
    weather = get_weather(city)
    bot.send_message(message.from_user.id, weather)
def get_weather(city):
    params = {"access_key": "4eea2154e45f203ca029c4290c7e6969", "query": city}
    api_result = requests.get('http://api.weatherstack.com/current', params)
    api_response = api_result.json()
    return f"It's {api_response['current']['temperature']} degrees in {city} right now"

@bot.message_handler(commands=['forecast'])
def forecast_handler(message):
    bot.send_message(message.from_user.id,"Enter the name of the city in English with a capital letter.")
    bot.register_next_step_handler(message, gg_handler)
def gg_handler(message):
    city2 = message.text
    forecast = get_forecast(city2)
    bot.send_message(message.from_user.id, f' {forecast[7]}\n {forecast[15]}\n {forecast[23]}\n {forecast[31]}\n {forecast[39]}')
def get_forecast(city2):
    s = []
    res = requests.get("http://api.openweathermap.org/data/2.5/forecast", params={'q': city2, 'units': 'metric', 'lang': 'eng', 'APPID': '7feb2657a5a447c8deaca3d5cbfca0e6'})
    data = res.json()
    for i in data['list']:
        s.append(str(i['dt_txt']) + " " + str('{0:+3.0f}'.format(i['main']['temp'])) + "  " + str(i['weather'][0]['description']))
    return s

bot.polling()


