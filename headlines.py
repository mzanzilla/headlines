import feedparser
import json
# import urllib.request
from flask import Flask, render_template, request
import urllib.request

app = Flask('__main__')
DEFAULTS = {'publication': 'bbc', 'city': 'London,UK'}
WEATHER_URL = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a5f726dcebb0b386891439f57e5bc6e9"
RSS_FEEDS = {'bbc': 'http://feeds.bbci.co.uk/news/rss.xml',
             'cnn': 'http://rss.cnn.com/rss/edition.rss',
             'fox': 'http://feeds.foxnews.com/foxnews/latest',
             'iol': 'http://www.iol.co.za/cmlink/1.640',
             'ghana': 'https://www.peacefmonline.com/pages/local/rss.xml'
             }


@app.route("/")
def home():
    # gets headlines from RSS feed based on user inputs
    publication = request.args.get("publication")
    if not publication:
        publication = DEFAULTS["publication"]

    articles = get_news(publication)
    # gets weather based on city enter by user
    city = request.args.get("city")
    if not city:
        city = DEFAULTS["city"]
    weather = get_weather(city)
    return render_template('home.html', articles=articles, weather=weather)


def get_news(query):
    if not query or query.lower() not in RSS_FEEDS:
        publication = DEFAULTS['publication']
    else:
        publication = query.lower()
    feed = feedparser.parse(RSS_FEEDS[publication])
    return feed['entries']


def get_weather(query):
    url = WEATHER_URL.format(query)
    data = urllib.request.urlopen(url)
    parsed = json.load(data)
    weather = None
    if parsed.get("weather"):
        weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
                   "city": parsed["name"], 'country': parsed['sys']['country']
                   }
    return weather


# def get_news(query):
#     api_url = "http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=a5f726dcebb0b386891439f57e5bc6e9"
#     url = api_url.format(query)
#     data = urllib.request.urlopen(url)
#     parsed = json.load(data)
#     weather = None
#     if parsed.get("weather"):
#         weather = {"description": parsed["weather"][0]["description"], "temperature": parsed["main"]["temp"],
#                    "city": parsed["name"]
#                    }
#     return weather


if __name__ == '__main__':
    app.run(debug=True)
