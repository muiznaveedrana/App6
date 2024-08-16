from flask import Flask, render_template
import pandas as pd


app = Flask(__name__)

stations = pd.read_csv("Data/stations.txt", skiprows = 17 )

stations = stations[["ID", "NAME                                 "]]

@app.route("/")
def home():
    return render_template("home.html", data = stations.to_html())

@app.route("/api/<station>/<date>")
def about(station, date):
    filename = "Data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates= ['    DATE'])

    temprature = df.loc[df['    DATE'] == date]['   TG'].squeeze() / 10

    
    return {"station": station,
            "date": date,
            "temperature": temprature}

@app.route("/api/<station>")
def all_data(station):
    filename = "Data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20, parse_dates= ['    DATE'])
    result = df.to_dict(orient = "records")
    return {"station": station,
            "Data": result}

@app.route("/api/year/<station>/<year>")
def year(station, year):
    filename = "Data/TG_STAID" + str(station).zfill(6) + ".txt"
    df = pd.read_csv(filename, skiprows=20)
    df["    DATE"] = df["    DATE"].astype(str)
    result = df[df['    DATE'].str.startswith(str(year))].to_dict(orient="records")
    return {"station": station,
            "Year": year,
            "Data": result}

if __name__ == "__main__":
    app.run(debug=True)