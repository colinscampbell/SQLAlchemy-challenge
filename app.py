import numpy as np

import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Measurement = Base.classes.measurement
Station = Base.classes.station

#################################################
# Flask Setup
#################################################
app = Flask(__name__)


#################################################
# Flask Routes
#################################################

@app.route("/")
def welcome():
    """List all available api routes."""
    return (
        f"Available Routes:<br/>"
        f"/api/v1.0/station<br/>"
        f"/api/v1.0/temperature<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/start=YYYY-MM-DD<br/>"
        f"/api/v1.0/start=YYYY-MM-DDend=YYYY-MM-DD"
    )


@app.route("/api/v1.0/station")
def station():
    session = Session(engine)
    results = session.query(Station.name).all()
    session.close()
    all_stations = list(np.ravel(results))
    return jsonify(all_stations)


@app.route("/api/v1.0/temperature")
def temperature():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.tobs).where((Measurement.station == 'USC00519281') & (Measurement.date > "2016-08-23")).all()
    session.close()
    all_temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict["date"] = date
        temp_dict["temp"] = tobs
        all_temps.append(temp_dict)
    return jsonify(all_temps)


@app.route("/api/v1.0/precipitation")
def precipitation():
    session = Session(engine)
    results = session.query(Measurement.date, Measurement.prcp).where(Measurement.date > "2016-08-23").all()
    session.close()
    all_prcp = []
    for date, prcp in results:
        temp_dict = {}
        temp_dict[date] = prcp
        all_prcp.append(temp_dict)
    return jsonify(all_prcp)

@app.route("/api/v1.0/start=<start_date>")
def start(start_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).where(Measurement.date >= start_date).all()
    session.close()
    weather_data = []
    temp_dict = {}
    temp_dict["min"] = results[0][0]
    temp_dict["max"] = results[0][1]
    temp_dict["avg"] = results[0][2]
    weather_data.append(temp_dict)
    return jsonify(weather_data)

@app.route("/api/v1.0/start=<start_date>end=<end_date>")
def end(start_date, end_date):
    session = Session(engine)
    results = session.query(func.min(Measurement.tobs),func.max(Measurement.tobs),func.avg(Measurement.tobs)).where((Measurement.date >= start_date) & (Measurement.date <= end_date)).all()
    session.close()
    weather_data = []
    temp_dict = {}
    temp_dict["min"] = results[0][0]
    temp_dict["max"] = results[0][1]
    temp_dict["avg"] = results[0][2]
    weather_data.append(temp_dict)
    return jsonify(weather_data)

if __name__ == "__main__":
    app.run(debug=True)