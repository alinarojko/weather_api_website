from flask import Flask, render_template
import pandas

app = Flask("__name__")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/api/v1/<station>/<date>")
def about(station, date):
    df = pandas.read_csv("")
    return render_template("about.html")


app.run(debug=True)