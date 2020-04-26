
import numpy as np
import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func

from flask import Flask, jsonify


#################################################
# Database Setup
#################################################
engine = create_engine("sqlite:///hawaii.sqlite")

# reflect an existing database into a new model
Base = automap_base()
# reflect the tables
Base.prepare(engine, reflect=True)

# Save reference to the table
Passenger = Base.classes.passenger



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
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/<startdate> or <startdate>/<enddate>"
    )


@app.route("/api/v1.0/precipitation")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Measurement.prcp).all()
    session.close()

    # Convert list of tuples into normal list
    all_prcp = list(np.ravel(results))

    return jsonify(all_prcp)


@app.route("/api/v1.0/stations")
def passengers():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query(Station).all()

    session.close()

    all_station = list(np.ravel(results))

    return jsonify(all_station)

@app.route("/api/v1.0/tobs")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query().all()

    session.close()

    # Convert list of tuples into normal list
    most_active_station = list(np.ravel(results))

    return jsonify(most_active_station)

@app.route("/api/v1.0/<start>")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query().all()

    session.close()

    # Convert list of tuples into normal list
    start_dates = list(np.ravel(results))

    return jsonify(start_dates)

@app.route("/api/v1.0/<start>/<end>")
def names():
    # Create our session (link) from Python to the DB
    session = Session(engine)

    results = session.query().all()

    session.close()

    # Convert list of tuples into normal list
    start_end_dates = list(np.ravel(results))

    return jsonify(start_end_dates)

if __name__ == '__main__':
    app.run(debug=True)
