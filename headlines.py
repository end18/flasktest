import feedparser
from flask import Flask
from flask import render_template
from flask import request

import json
import urllib2
import urllib

app = Flask(__name__)

CURRENY_URL="https://openexchangerates.org/api/latest.json?app_id=720446b0c9e54a1eb70fd084fd6f12ff"
WEATHER_URL="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3352a2398ed7cc04810606642cf417e1"

RSS_FEED = {'bbc' : "http://feeds.bbci.co.uk/news/rss.xml",
            'cnn' : "http://rss.cnn.com/rss/edition.rss",
            'fox' : "http://feeds.foxnews.com/foxnews/latest",
            'iol' : "http://iol.co.za/cmlink/1.640",
            'jtbc': "http://fs.jtbc.joins.com/RSS/newsflash.xml"}

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

DEFAULTS = {'publication' : 'jtbc', 
            'city': 'Chamsil, KR',
            'currency_from' : 'USD',
            'currency_to' : 'KRW'}

@app.route("/", methods=['GET', 'POST'])
def home():
    publication=request.args.get("publication")
    if not publication:
        publication = DEFAULTS['publication']
    articles = get_news(publication)
    city = request.args.get("city")
    if not city:
        city = DEFAULTS['city']
    weather = get_weather(city)
    currency_from = request.args.get("currency_from")
    if not currency_from:
        currency_from = DEFAULTS['currency_from']
    currency_to = request.args.get('currency_to')
    if not currency_to:
        currency_to = DEFAULTS['currency_to']
    rate, currencies = get_rate(currency_from, currency_to)
    
    return render_template("home.html", 
                           articles=articles, 
                           weather=weather,
                           currency_from=currency_from,
                           currency_to=currency_to,
                           rate = rate,
                           currencies=sorted(currencies))

def get_news(query):
    if not query or query.lower() not in RSS_FEED:
        publication='jtbc'
    else:
        publication=query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    weather = get_weather("Lundon, UK")
    return feed['entries']

def get_weather(query):
    api_url="http://api.openweathermap.org/data/2.5/weather?q={}&units=metric&appid=3352a2398ed7cc04810606642cf417e1"
    query = urllib.quote(query)
    url = api_url.format(query)
    data = urllib2.urlopen(url).read()
    parsed = json.loads(data)
    weather = None
    if parsed.get("weather"):
        weather={"description" : parsed["weather"][0]["description"],
                 "temperature" : parsed["main"]["temp"],
                 "city" : parsed["name"],
                 "country" : parsed["sys"]["country"]
        }
        return weather
        
def get_rate(frm, to):
    all_currency = urllib2.urlopen(CURRENY_URL).read()
    parsed = json.loads(all_currency).get('rates')
    frm_rate = parsed.get(frm.upper())
    to_rate = parsed.get(to.upper())
    return (to_rate / frm_rate, parsed.keys())
    
    
    
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)