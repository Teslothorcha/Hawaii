from sqlalchemy.ext.automap import automap_base
from sqlalchemy.orm import Session
from sqlalchemy import create_engine
import os


basedir = os.path.abspath(os.path.join('../', os.path.dirname(__file__)))

Base = automap_base()

engine = create_engine("sqlite:///{}hawaii.sqlite".format(basedir[:-3]))

# reflect the tables
Base.prepare(engine, reflect=True)

Station = Base.classes.station
Measurement = Base.classes.measurement

session = Session(engine)
