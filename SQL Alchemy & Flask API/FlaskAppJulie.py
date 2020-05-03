import sqlalchemy
from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine, func
from flask import Flask, jsonify

engine = create_engine("sqlite:///Resources/hawaii.sqlite")

Base = automap_base()
Base.prepare(engine, reflect=True)
Base.classes.keys()
Measurement = Base.classes.measurement
Station= Base.classes.station
session = Session(bind=engine)


app = Flask(__name__)


# 3. Define what to do when routes
@app.route("/")
def home():
    return  (
        f"Available Routes:<br/>"
        f"/api/v1.0/precipitation<br/>"
        f"/api/v1.0/stations<br/>"
        f"/api/v1.0/tobs<br/>"
        f"/api/v1.0/start<br/>"
        f"/api/v1.0/start/end"
    )

@app.route("/api/v1.0/precipitation")
def precipitation():


    
    results=session.query(Measurement.date,Measurement.prcp).\
    order_by(Measurement.date.desc()).all()
    return jsonify (results)
# Convert the query results to a dictionary using `date` as the key and `prcp` as the value.
# Return the JSON representation of your dictionary.


@app.route("/api/v1.0/stations")
def stations():
 
   
   hawaiistations=session.query(Station.station,Station.name).all()
   return jsonify (json_list =hawaiistations)
  
#* Return a JSON list of stations from the dataset.
    
@app.route("/api/v1.0/tobs")
def tobs():

#  Query the dates and temperature observations of the most active station for the last year of data.
 
   tempob=session.query(Measurement.station,Measurement.date,Measurement.tobs).\
   filter(Measurement.station=='USC00519281').order_by(Measurement.date.desc()).all()
   return jsonify(json_list=tempob)
   
#Return a JSON list of temperature observations (TOBS) for the previous year.




#When given the start only, calculate `TMIN`, `TAVG`, and `TMAX` for all dates greater than and equal to the start date.
#Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range

@app.route("/api/v1.0/<start>")
@app.route("/api/v1.0/<start>/<end>")
def calc_temps(start=None,end=None):


# TMIN, TAVG, and TMAX for a list of dates.
    
#     Args:
#         start_date (string): A date string in the format %Y-%m-%d
#         end_date (string): A date string in the format %Y-%m-%d

    if not end:
        startend=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
        filter(Measurement.date >= start).all()
        return jsonify(json_list=startend)
    startend=session.query(func.min(Measurement.tobs), func.avg(Measurement.tobs), func.max(Measurement.tobs)).\
    filter(Measurement.date >= start).filter(Measurement.date <= end).all()
    return jsonify(json_list=startend)
# # When given the start and the end date, calculate the `TMIN`, `TAVG`, and `TMAX` for dates between the start and end date inclusive.
# #Return a JSON list of the minimum temperature, the average temperature, and the max temperature for a given start or start-end range


if __name__ == "__main__":
    app.run(debug=True)
