from sqlalchemy import Table, Column, Integer, String, Float, ForeignKey, MetaData
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import pandas as pd

engine = create_engine('sqlite:///database.db')

Base = declarative_base()

meta = MetaData()

class Clean_stations(Base):
    __tablename__ = "clean_stations"
    id = Column(Integer, primary_key=True)
    station = Column(String, unique=True)
    latitude = Column(Float)
    longitude = Column(Float)
    elevation = Column(Float)
    name = Column(String)
    country = Column(String)
    state = Column(String)

class Clean_measure(Base):
    __tablename__ = "clean_measure"
    id = Column(Integer, primary_key=True)
    station = Column(String, ForeignKey('clean_stations.station'))
    date = Column(String)
    precip = Column(Float)
    tobs = Column(Integer)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

#csv_file = "clean_stations.csv"
#csv_file = "clean_measure.csv"
#df = pd.read_csv(csv_file)

#records = [Clean_stations(station=row["station"], latitude=float(row["latitude"]), longitude=float(row["longitude"]), elevation=float(row['elevation']), name=row['name'], country=row["country"], state=row["state"]) for _, row in df.iterrows()]
#records = [Clean_measure(station=row["station"], date=row["date"], precip=row["precip"], tobs=row["tobs"]) for _, row in df.iterrows()]

#session.add_all(records)
#session.commit()

#meta.create_all(engine)
#print(engine.table_names())
conn = engine.connect()
result = conn.execute("SELECT * FROM clean_stations LIMIT 5").fetchall()

print(result)

conn.close()
session.close()