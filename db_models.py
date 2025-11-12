from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import declarative_base, sessionmaker
from sqlalchemy.dialects.mysql import JSON

DATABASE_URL = "mysql+aiomysql://user:password@localhost:3306/school_db"
engine = create_async_engine(DATABASE_URL, echo=False)
AsyncSessionLocal = sessionmaker(engine, expire_on_commit=False, class_=None)
Base = declarative_base()

class Place(Base):
    __tablename__ = "places"
    place_id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), unique=True)

class PlaceDistance(Base):
    __tablename__ = "place_distances"
    id = Column(Integer, primary_key=True, autoincrement=True)
    from_place_id = Column(Integer, ForeignKey("places.place_id"))
    to_place_id = Column(Integer, ForeignKey("places.place_id"))
    distance = Column(Float)  # distance in meters

class Bus(Base):
    __tablename__ = "buses"
    bus_id = Column(Integer, primary_key=True, autoincrement=True)
    capacity = Column(Integer)

class RouteAssignment(Base):
    __tablename__ = "route_assignments"
    route_id = Column(Integer, primary_key=True, autoincrement=True)
    bus_id = Column(Integer, ForeignKey("buses.bus_id"))
    places = Column(JSON)  # list of place_ids in order
