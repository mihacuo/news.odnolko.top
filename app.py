from flask import Flask, g, render_template, flash, request
from config import Config
from forms import SearchForm
from datetime import datetime, timedelta
from rss_news_v2 import Rss_en
from models import Visit

app = Flask(__name__)
app.config.from_object(Config)

@app.before_request
def log_ip():
    if request.environ.get('HTTP_X_FORWARDED_FOR') is None:
        g.ip = request.environ['REMOTE_ADDR']
    else:
        g.ip = request.environ['HTTP_X_FORWARDED_FOR']

@app.route("/", methods = ["GET", "POST"])
def index():
    flash("starting app111")
    flash(f"{g.ip=}")
    Visit.create(ip=g.ip)
    g.form = SearchForm()
    if g.form.validate_on_submit():
        g.search_term = g.form.query.data
        g.duration = int(g.form.duration.data)
        Visit.create(ip=g.ip, type=f"TERM={g.search_term}, days={g.duration}")
        end_date = datetime.now()
        start_date = end_date - timedelta(days=g.duration)

        flash(f"{g.search_term=}")
        flash(f"{g.duration=} days")
        flash(f"{start_date=}")
        flash(f"{end_date=}")
        dated_news = Rss_en.get_news_dated(start=start_date, end=end_date)
        result_news = Rss_en.get_news(dated_news[0], include=[g.search_term])
        g.data_news = result_news[0]
        flashes = dated_news[1]
        flashes += result_news[1]
        for _ in flashes:
            flash(_)


    return render_template("index.html")