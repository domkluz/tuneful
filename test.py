from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Sequence, ForeignKey

#from . import app

#engine = create_engine(app.config["DATABASE_URI"])
engine = create_engine("postgresql://ubuntu:thinkful@localhost:5432/tuneful")
Base = declarative_base()
Session = sessionmaker(bind=engine)
session = Session()


class Song(Base):
    __tablename__ = "songs"
    
    id = Column(Integer, primary_key=True)
    song_file_id = Column(Integer,ForeignKey("files.id"), nullable = False)
    
    def as_dictionary(self):
        song_file_info = session.query(File).filter_by(id=self.song_file_id).first()
        return {"id": self.id, "file":{"id":song_file_info.id,"name":song_file_info.filename}}


class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    file = Column(String(300))
    song = relationship("Song",uselist = False, backref ="song_name")
    
    def as_dictionary(self):
        file_post = {"id":self.id,"name":self.file}
        return file_post

Base.metadata.create_all(engine)

# Create your models here
