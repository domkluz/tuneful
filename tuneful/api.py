import os.path
import json

from flask import request, Response, url_for, send_from_directory
from werkzeug.utils import secure_filename
from jsonschema import validate, ValidationError

from . import models
from . import decorators
from . import app 
from .database import session
from .utils import upload_path


@app.route("/api/songs", methods=["GET"])
@decorators.accept("application/json")
def get_songs():
    """ Return a list of all the songs as JSON """

    # get the songs from the database
    songs = session.query(models.Song).all()

    # convert the songs to JSON and return a Response
    data = json.dumps([song.as_dictionary() for song in songs])
    return Response(data, 200, mimetype="application/json")


@app.route("/api/songs", methods=["POST"])
@decorators.accept("application/json")
@decorators.require("application/json")
def post_song():
    """ Add a new song """
    data = request.json
  
    # add the song to the database
    song = models.Song(song_file_id=data["file"]["id"])
    session.add(song)
    session.commit()

    # return a 201 Created, containing the post as JSON and with the
    # location header set to the location of the post
    data = json.dumps(song.as_dictionary())
    headers = {"Location": url_for("get_songs")}
    return Response(data, 201, headers=headers, mimetype="application/json")
    
    
@app.route("/api/songs", methods=["PUT"])
@decorators.accept("application/json")
@decorators.require("application/json")
def update_song():
    """ Update a song """
    data = request.json
  
    song = session.query(models.Song).get(data["id"])

    if not song:
        message = "could not find post with id {}".format(data["id"])
        data = json.dumps({"message":message})
        return Response(data,404,mimetype = "application/json")
    

    file0=session.query(models.File).filter(models.File.id==song.song_file_id).first()
    file0.file = data["file"]["name"]
    session.commit()
    
    message = "File name updated for song id {}".format(data["id"])
    
    data = json.dumps({"message":message})
    return Response(data,200,mimetype = "application/json")
    

@app.route("/api/songs", methods=["DELETE"])
@decorators.accept("application/json")
def delete_song():
    """Delete a single song"""
    
    data = request.json
    
    song = session.query(models.Song).get(data["id"])
    
    if not song:
        message = "could not find post with id {}".format(data["id"])
        data = json.dumps({"message":message})
        return Response(data,404,mimetype = "application/json")
    
    file=session.query(models.File).filter(models.File.id==song.song_file_id).first()
    
    session.delete(song)
    session.delete(file)
    
    message = "Song deleted with id {}".format(data["id"])
    data = json.dumps({"message":message})
    return Response(data,200,mimetype = "application/json")
    

@app.route("/uploads/<filename>", methods=["GET"])
def uploaded_file(filename):
    return send_from_directory(upload_path(), filename)
    
    
@app.route("/api/files", methods=["POST"])
@decorators.require("multipart/form-data")
@decorators.accept("application/json")
def file_post():
    file = request.files.get("file")
    if not file:
        data = {"message": "Could not find file data"}
        return Response(json.dumps(data), 422, mimetype="application/json")

    filename = secure_filename(file.filename)
    db_file = models.File(file=filename)
    session.add(db_file)
    session.commit()
    file.save(upload_path(filename))

    data = db_file.as_dictionary()
    return Response(json.dumps(data), 201, mimetype="application/json")