import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify
import datetime as dt
import pandas as pd


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///Resources/hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Station = Base.classes.Station
Measurement=Base.classes.Measurement


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

    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results_precipitation=session.query(Measurement.date, Measurement.station, Measurement.prcp).\
                                    group_by(Measurement.date).order_by(Measurement.date.desc()).all()
    session.close()

    # Convert list of tuples into dict
    all_prcp = []
    for r in results_precipitation:
        prcp_dict = {r.station:{r.date:r.prcp}}
        all_prcp.append(prcp_dict)
    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    results = session.query(Measurement.station).group_by(Measurement.station).all
    session.close()

    all_station = list(np.ravel(results))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def tobs():
    # Create our session (link) from Python to the DB
    session = Session(engine)
    latest_date=session.query(Measurement.date).order_by(Measurement.date.desc()).first().date
    latest_date=dt.datetime.strptime(latest_date, '%Y-%m-%d')
    earliest_date=latest_date-dt.timedelta(days=365)
    temp_last12months=session.query(Measurement.date, Measurement.tobs).\
                                    filter(Measurement.date>=earliest_date).filter(Measurement.station=='USC00519281').\
                                    group_by(Measurement.date).order_by(Measurement.date.desc()).all()
    session.close()

    # Convert list of tuples into list
    active_station_list=list(temp_last12months)
    return jsonify(active_station_list)

@app.route("/api/v1.0/<start>")
def start(startdate):
    session = Session(engine)
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).all())

@app.route("/api/v1.0/<start>/<end>")
def startend(startdate,enddate):
    session = Session(engine)
    return jsonify(session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= startdate).filter(Measurement.date <= enddate).all())

if __name__ == '__main__':
    app.run(debug=True)
