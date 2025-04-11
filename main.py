from flask import Flask, render_template
import pandas as pd

app = Flask(__name__)

# Collect the data from the file , skip first 17 rows , to find headers for the columns
stations = pd.read_csv("data_small/stations.txt", skiprows=17, header=0)

# Select only 2 columns to be shown
stations = stations[["STAID", "STANAME                                 "]]

# Start first page , display collected data in html format on the main page
@app.route("/")
def home():
    print(stations.head())
    return render_template("home.html", data=stations.to_html())

# Case to show all information , for one station for one "date" - user input
@app.route("/api/v1/<station>/<date>")
def about(station, date):
    # Create a filename for current station
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"

    # Load the data into a dataframe, skip first 20 rows, parse the date column , to be treated like date
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])
    temperature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10
    return {"station": station,
            "date": date,
            "temperature": temperature}


# Case to show all information , for excact "station"  for all dates - user input
@app.route("/api/vi/<stations>")
def all_data(station):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # Convert a dataframe to a dictionary
    result = df.to_dict(orient="records")
    return result


# Case to show all information , for excact "station"  for one year - user input
@app.route("/api/v1/yearly/<station>/<year>")
def yearly(station, year):
    filename = "data_small/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates=["    DATE"])

    # Convert date column to a str
    df["    DATE"] = df["    DATE"].astype(str)

    # Collecting respond , convert dataframe with data from that one year to the dictionary. add orientation to records to be
    # in the json format
    result = df[df["    DATE"].str.startswith(str(year))].to_dict(orient="records")
    return result

if __name__ == "__main__":
    app.run(debug=True)
