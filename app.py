# Import the dependencies
from flask import Flask, jsonify

#################################################
# Database Setup
#################################################
# Import additional dependencies
import numpy as np
import pandas as pd
import datetime as dt
from sqlalchemy import create_engine, func
from sqlalchemy.orm import Session
from sqlalchemy.ext.automap import automap_base

# Create engine to hawaii.sqlite
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# Reflect an existing database into a new model
Base = automap_base()

# Reflect the tables
Base.prepare(engine, reflect=True)

# Save references to each table
Measurement = Base.classes.measurement
Station = Base.classes.station

# Create our session (link) from Python to the DB
session = Session(engine)

#################################################
# Flask Setup
#################################################
app = Flask(__name__)

#################################################
# Flask Routes
#################################################

# Home route
@app.route("/")
def home():
    return (
        f"Welcome to the Climate App API!<br/><br/>"
        f"Available Routes:<br/>"
        f"<a href='/api/v1.0/precipitation'>/api/v1.0/precipitation</a><br/>"
        f"<a href='/api/v1.0/stations'>/api/v1.0/stations</a><br/>"
        f"<a href='/api/v1.0/tobs'>/api/v1.0/tobs</a><br/>"
        f"<a href='/api/v1.0/start_date'>/api/v1.0/start_date</a><br/>"
        f"<a href='/api/v1.0/start_date/end_date'>/api/v1.0/start_date/end_date</a>"
    )

# Precipitation route
@app.route("/api/v1.0/precipitation")
def precipitation():
    # Query the last 12 months of precipitation data
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)
    precipitation_data = session.query(Measurement.date, Measurement.prcp).\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a dictionary using date as the key and prcp as the value
    precipitation_dict = {date: prcp for date, prcp in precipitation_data}

    return jsonify(precipitation_dict)

# Stations route
@app.route("/api/v1.0/stations")
def stations():
    # Query all stations
    stations = session.query(Station.station, Station.name).all()

    # Convert the query results to a list of dictionaries
    stations_list = []
    for station, name in stations:
        stations_list.append({"station": station, "name": name})

    return jsonify(stations_list)

# Temperature Observations (tobs) route
@app.route("/api/v1.0/tobs")
def tobs():
    # Find the most recent date and calculate the date one year ago
    recent_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()[0]
    one_year_ago = dt.datetime.strptime(recent_date, "%Y-%m-%d") - dt.timedelta(days=365)

    # Query the temperature observations for the most active station in the last 12 months
    tobs_data = session.query(Measurement.date, Measurement.tobs).\
        filter(Measurement.station == "USC00519281").\
        filter(Measurement.date >= one_year_ago).all()

    # Convert the query results to a list of dictionaries
    tobs_list = []
    for date, tobs in tobs_data:
        tobs_list.append({"date": date, "tobs": tobs})

    return jsonify(tobs_list)

# Start Date route
@app.route("/api/v1.0/start_date")
def start_date():
    # Calculate the minimum, average, and maximum temperatures for all dates in the dataset
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all()

    # Convert the query results to a list of dictionaries
    stats_list = []
    for Tmin, Tavg, Tmax in temperature_stats:
        stats_list.append({"TMIN": Tmin, "TAVG": Tavg, "TMAX": Tmax})

    return jsonify(stats_list)

# Start and End Dates route
@app.route("/api/v1.0/start_date/end_date")
def start_end_dates():
    # Calculate the minimum, average, and maximum temperatures for all dates in the dataset
    temperature_stats = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).all()

    # Convert the query results to a list of dictionaries
    stats_list = []
    for Tmin, Tavg, Tmax in temperature_stats:
        stats_list.append({"TMIN": Tmin, "TAVG": Tavg, "TMAX": Tmax})

    return jsonify(stats_list)

# Close the session at the end of the program
session.close()

# Run the Flask application
if __name__ == "__main__":
    app.run()
