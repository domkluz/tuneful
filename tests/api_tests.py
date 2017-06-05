import unittest
import os
import json
try: from urllib.parse import urlparse
except ImportError: from urlparse import urlparse # Python 2 compatibility

# Configure our app to use the testing databse
os.environ["CONFIG_PATH"] = "tuneful.config.TestingConfig"

from tuneful import app
from tuneful import models
from tuneful.database import Base, engine, session
from tuneful.utils import upload_path
from io import BytesIO


class TestAPI(unittest.TestCase):
    """ Test the API"""
    
    def setUp(self):
        """ Test setup """
        self.client = app.test_client()
        Base.metadata.create_all(engine)
        
    
    def tearDown(self):
        """ Test teardown """
        
        session.close()
        Base.metadata.drop_all(engine)
    
    def test_get_song(self):
        """Getting a song"""
        
        songA = models.File(file = "song1.mp3")
        song = models.Song()
        songA.song=song
        session.add(songA)
        session.commit()
    
        response = self.client.get("/api/songs",headers =[("Accept","application/json")])
        
        self.assertEqual(response.status_code,200)
        self.assertEqual(response.mimetype,"application/json")
        
        data = json.loads(response.data.decode("ascii"))
        print(data)
        self.assertEqual(len(data),1)
        
        postA = data[0]
        self.assertEqual(postA["id"],1)
        self.assertEqual(postA["file"]["id"],1)
        self.assertEqual(postA["file"]["name"],"song1.mp3")
        
        
    def test_post_song(self):
        """Post a Song"""
        
        songA = models.File(file = "song1.mp3")
        session.add(songA)
        session.commit()
        data = {"file": {"id": 1}}
        
        response = self.client.post("/api/songs",data = json.dumps(data),
        content_type="application/json",headers = [("Accept","application/json")])
        
        self.assertEqual(response.status_code,201)
        self.assertEqual(response.mimetype,"application/json")
        self.assertEqual(urlparse(response.headers.get("Location")).path,"/api/songs")
        
        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(data["id"],1)
        self.assertEqual(data["file"]["id"],1)
        self.assertEqual(data["file"]["name"],"song1.mp3")
        
        song = session.query(models.Song).all()
        self.assertEqual(len(song),1)
        
        song = song[0]
        self.assertEqual(song.id,1)
        self.assertEqual(song.song_file_id,1)
        
        
    def test_updating_song(self):
        """Update a song"""
        songA = models.File(file = "songTest.mp3")
        song = models.Song()
        songA.song=song
        session.add(songA)
        session.commit()
        
        data = {"id":songA.song.id,"file":{"name":"songUpdated.mp3"}}
        response = self.client.put("/api/songs",
        data = json.dumps(data), content_type="application/json",
        headers = [("Accept","application/json")])
        
        self.assertEqual(response.status_code,200)
        data = json.loads(response.data.decode("ascii"))
        
        self.assertEqual(data["message"],"File name updated for song id 1")
        
        song = session.query(models.File.file).all()
        print(song[0])

        self.assertEqual(song[0][0],"songUpdated.mp3")

    def test_delete_song(self):
        """Delete a song"""
        
        songA = models.File(file = "songTest.mp3")
        song = models.Song()
        songA.song=song
        session.add(songA)
        session.commit()        
        
        data = {"id":songA.song.id}
        response = self.client.delete("/api/songs",
        data = json.dumps(data), content_type="application/json",
        headers = [("Accept","application/json")])

        self.assertEqual(response.status_code,200)
        data = json.loads(response.data.decode("ascii"))
        
        self.assertEqual(data["message"],"Song deleted with id 1")
        
        song = session.query(models.Song.id).all()
        file = session.query(models.File.id).all()
        
        self.assertEqual(song,[])
        self.assertEqual(file,[])
        
        
    def test_get_uploaded_file(self):
        path =  upload_path("test.txt")
        with open(path, "wb") as f:
            f.write(b"File contents")

        response = self.client.get("/uploads/test.txt")

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.mimetype, "text/plain")
        self.assertEqual(response.data, b"File contents")
    
    
    def test_file_upload(self):
        data = {
            "file": (BytesIO(b"File contents"), "test.txt")}

        response = self.client.post("/api/files",
            data=data,
            content_type="multipart/form-data",
            headers=[("Accept", "application/json")])

        self.assertEqual(response.status_code, 201)
        self.assertEqual(response.mimetype, "application/json")

        data = json.loads(response.data.decode("ascii"))
        self.assertEqual(urlparse(data["path"]).path, "/uploads/test.txt")

        path = upload_path("test.txt")
        self.assertTrue(os.path.isfile(path))
        with open(path, "rb") as f:
            contents = f.read()
        self.assertEqual(contents, b"File contents")    


if __name__ == "__main__":
    unittest.main()

        
        
        
        
        
        
        
        