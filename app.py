from flask import Flask, g, render_template, flash
from config import Config
from forms import SearchForm

app = Flask(__name__)
app.config.from_object(Config)

@app.route("/", methods = ["GET", "POST"])
def index():
    flash("starting app")
    flash(f"{app.config["OS_NAME"]=}")
    g.form = SearchForm()
    if g.form.validate_on_submit():
        g.search_term = g.form.query.data
        flash(f"{g.search_term=}")

    return render_template("index.html")