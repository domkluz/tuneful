from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey

from . import app

engine = create_engine(app.config["DATABASE_URI"])
#engine = create_engine("postgresql://ubuntu:thinkful@localhost:5432/tuneful")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()

# Create your models here

