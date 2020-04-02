from flask import Flask, jsonify

import numpy as np
import datetime as dt

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

engine = create_engine("sqlite:///hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)

Measurement = Base.classes.measurement
Station = Base.classes.station

app = Flask(__name__)


@app.route("/")
def home():
    return (
    f"Welcome to my Hawaii Weather API! Available routes:<br/>"
    f"/api/v1.0/precipitation<br/>"
    f"/api/v1.0/stations<br/>"
    f"/api/v1.0/tobs<br/>"
    f"/api/v1.0/start/month-day-year<br/>"
    f"/api/v1.0/startend/start-date/end-date<br/>"
    f"NOTE: Dates have to follow this format: '2010-12-25' (YYYY, MM, DD)<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).all()
    session.close()

    prcp_list = []

    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        prcp_list.append(prcp_dict)

    return jsonify(prcp_list)

@app.route("/api/v1.0/stations")
def stations():
    session = Session(engine)
    stations = engine.execute('SELECT id, station FROM station GROUP BY station').fetchall()
    session.close()

    station_list = []

    for id, station in stations:
        station_dict = {}
        station_dict["id"] = id
        station_dict["station"] = station
        station_list.append(station_dict)

    return jsonify(station_list)

@app.route("/api/v1.0/tobs")
def tobs():
    one_year = dt.date(2017, 8, 23) - dt.timedelta(days=365)
    session = Session(engine)
    tobs = session.query(Measurement.date, Measurement.tobs, Measurement.station).\
    filter(Measurement.date > one_year).\
    filter(Measurement.station == "USC00519281").all()
    session.close()

    tobs_list = []

    for date, tobs, station in tobs:
        tobs_dict = {}
        tobs_dict["date"] = date
        tobs_dict["tobs"] = tobs
        tobs_list.append(tobs_dict)

    return jsonify(tobs_list)

@app.route("/api/v1.0/start/<start>")
def start_date_varaible(start):
    session = Session(engine)
    temps = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
    session.close()


    return jsonify(temps)

@app.route("/api/v1.0/startend/<start>/<end>")
def start_end_date_varaible(start, end):
    session = Session(engine)
    temps_2 = session.query(func.max(Measurement.tobs), func.min(Measurement.tobs), func.avg(Measurement.tobs)).\
        filter(Measurement.date >= start).\
        filter(Measurement.date <= end).all()
    session.close()

    return jsonify(temps_2)

if __name__ == "__main__":
    app.run(debug=True)