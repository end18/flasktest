import feedparser
from flask import Flask
from flask import render_template
from flask import request

app = Flask(__name__)

RSS_FEED = {'bbc' : "http://feeds.bbci.co.uk/news/rss.xml",
            'cnn' : "http://rss.cnn.com/rss/edition.rss",
            'fox' : "http://feeds.foxnews.com/foxnews/latest",
            'iol' : "http://iol.co.za/cmlink/1.640",
            'jtbc': "http://fs.jtbc.joins.com/RSS/newsflash.xml"}

BBC_FEED = "http://feeds.bbci.co.uk/news/rss.xml"

@app.route("/", methods=['GET', 'POST'])
def get_news():
    query = request.form.get("publication")
    if not query or query.lower() not in RSS_FEED:
        publication='jtbc'
    else:
        publication=query.lower()
    feed = feedparser.parse(RSS_FEED[publication])
    return render_template("home.html", articles=feed['entries'])
    
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080, debug=True)