
from .database import Base
from .database import Column, Integer, String, ForeignKey, relationship, session, engine
from flask import url_for


class Song(Base):
    __tablename__ = "songs"

    id = Column(Integer, primary_key=True)
    song_file_id = Column(Integer, ForeignKey("files.id"), nullable=False)


    def as_dictionary(self):
        song_file_info = session.query(File).filter_by(id=self.song_file_id).first()
        
        return {"id": self.id,"file": {"id": song_file_info.id,"name": song_file_info.file}}


class File(Base):
    __tablename__ = "files"
    
    id = Column(Integer, primary_key=True)
    file = Column(String(300))
    song = relationship("Song",uselist = False, backref ="song_name")
    
    def as_dictionary(self):
        file_post = {
            "id":self.id,
        "name":self.file,
        "path": url_for("uploaded_file", filename=self.file)}
        
        return file_post

        
#Base.metadata.create_all(engine)

#songA = File(file = "test2.mp3")
#song = Song()
#songA.song=song
#session.add(songA)
#session.commit()


    
    
    



