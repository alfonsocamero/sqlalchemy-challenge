import numpy as np
import datetime as dt
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

# Save references to each table
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
    return (
        f"Welcome to the Hawaii vacation trip API!<br/>"
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]<br/>"
        f"/api/v1.0/[start_date format:yyyy-mm-dd]/[end_date format:yyyy-mm-dd]<br/>"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():
    #Create session
    session = Session(engine)

    # Query all dates and precipitation
    results = session.query(Measurement.date, Measurement.prcp).all()

    session.close()

     #Convert the query results to a dictionary using date as the key and prcp as the value
    all_prcp = []
    for date, prcp in results:
        prcp_dict = {}
        prcp_dict["date"] = date
        prcp_dict["prcp"] = prcp
        all_prcp.append(prcp_dict)

    return jsonify(all_prcp)

@app.route("/api/v1.0/stations")
def stations():
    #Create session
    session = Session(engine)

    # Query all stations
    results = session.query(Station.station, Station.name).all()

    session.close()

    # Create a dictionary of stations
    stations = []
    for station, name in results:
        stations_dict = {}
        stations_dict["station"] = station
        stations_dict["name"] = name
        stations.append(stations_dict)
    
    #Return a JSON list of stations from the dataset.
    return jsonify(stations)

@app.route("/api/v1.0/tobs")
def tobs():
    #Create session
    session = Session(engine)

    #Find last date in database
    last_date = session.query(Measurement.date).order_by(Measurement.date.desc()).first()
    year_ago = (dt.datetime.strptime(last_date[0], "%Y-%m-%d") - dt.timedelta(days=365)).strftime('%Y-%m-%d')

    #Find most active station
    most_active = session.query(Measurement.station,func.count(Measurement.station)).group_by(Measurement.station).\
        order_by(func.count(Measurement.station).desc()).first()

    #Query dates and temperature observations for the most active station in the last year of data 
    results = session.query(Measurement.tobs).filter(Measurement.date >= year_ago).\
filter(Measurement.station == most_active[0]).all()

    session.close()

    #Convert list of tuples into normal list
    most_active_data = list(np.ravel(results))

    return jsonify(most_active_data)

@app.route("/api/v1.0/<start>")
def start_date(start):
    #Create session
    session = Session(engine)

    date_range = Measurement.date
    minimum = func.min(Measurement.tobs)
    average = func.avg(Measurement.tobs)
    maximum = func.max(Measurement.tobs)
    
    #calculate TMIN, TAVG, and TMAX for all dates greater than and equal to the start date
    results = session.query(\
                            func.min(Measurement.tobs),\
                            func.avg(Measurement.tobs),\
                            func.max(Measurement.tobs).\
             filter(Measurement.date >= start)).all()
             
    session.close()
    
    temps = list(np.ravel(results))
    return jsonify(temps)
    
    #Create dictionary to hold info 
    start_info = []
    for date_range, minimum, average, maximum in results:
        start_dict = {}
        start_dict["DATE"] = date_range
        start_dict["TMIN"] = minimum
        start_dict["TAVG"] = average
        start_dict["TMAX"] = maximum
        start_info.append(start_dict)

    return jsonify(start_info)


#@app.route("/api/v1.0/<start>/<end>")
#def start_end_date(start, end):
    #Create session
    #session = Session(engine)
    
    #Calculate the TMIN, TAVG, and TMAX for dates between the start and end date inclusive
    #results = session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
       #filter(Measurement.date >= start).\
       #filter(Measurement.date <= end).all()
    # Unravel results into a 1D array and convert to a list
    #temps = list(np.ravel(results))
    #return jsonify(temps=temps)

    #session.close()        
    
#Create dictionary to hold info
    #start_end_info = []

    #for min, avg, max in results:
        #start_end_dict = {}
        #start_end_dict["TMIN"] = min
        #start_end_dict["TAVG"] = avg
        #start_end_dict["TMAX "] = max
        #start_end_info.append(start_end_dict)

    #return jsonify(start_end_info)
    
if __name__ == "__main__":
    app.run(debug=True)

