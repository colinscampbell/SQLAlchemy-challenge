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
        f"/api/v1.0/precipitation"
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
    results = session.query(Measurement.date, Measurement.tobs).all()
    session.close()
    all_temps = []
    for date, tobs in results:
        temp_dict = {}
        temp_dict[date] = tobs
        all_temps.append(temp_dict)
    return jsonify(all_temps)
    
    # Create a dictionary from the row data and append to a list of all_passengers
    #all_passengers = []
    #for name, age, sex in results:
    #    passenger_dict = {}
    #    passenger_dict["name"] = name
    #    passenger_dict["age"] = age
    #    passenger_dict["sex"] = sex
    #    all_passengers.append(passenger_dict)



@app.route("/api/v1.0/precipitation")
def precipitation():
    return 0

if __name__ == "__main__":
    app.run(debug=True)