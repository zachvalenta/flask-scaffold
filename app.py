import os

from dotenv import find_dotenv, load_dotenv
from flask import Flask, render_template
from flask_marshmallow import Marshmallow
from flask_sqlalchemy import SQLAlchemy

"""
CONF
"""

# db - load env, construct path
load_dotenv(find_dotenv())
basedir = os.path.abspath(os.path.dirname(__file__))
db_path = os.path.join(basedir, os.getenv("DATABASE"))
db_uri = "sqlite:///" + db_path

# app - init, config
app = Flask(__name__, template_folder=basedir)
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SQLALCHEMY_DATABASE_URI"] = db_uri

# db - init
db = SQLAlchemy(app)
ma = Marshmallow(app)

"""
MODELS
"""


class Artist(db.Model):
    artist_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    songs = db.relationship("Song", backref="artist")

    def __repr__(self):
        return f"id {self.artist_id} name {self.name}"


class Song(db.Model):
    song_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    artist_id = db.Column(db.Integer, db.ForeignKey("artist.artist_id"))
    performances = db.relationship("Performance", backref="song")

    def __repr__(self):
        return f"id {self.song_id} name {self.name}"


class Performance(db.Model):
    perf_id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Integer, nullable=False)
    song_id = db.Column(db.Integer, db.ForeignKey("song.song_id"))
    concert_id = db.Column(db.Integer, db.ForeignKey("concert.concert_id"))

    def __repr__(self):
        return f"id {self.perf_id} rating {self.rating}"


class Concert(db.Model):
    concert_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.Text)
    performances = db.relationship("Performance", backref="concert")

    def __repr__(self):
        return f"id {self.concert_id} name {self.name}"


"""
SCHEMAS
"""


class ArtistSchema(ma.ModelSchema):
    class Meta:
        model = Artist


class SongSchema(ma.ModelSchema):
    class Meta:
        model = Song

    artist = ma.Nested(ArtistSchema)


class ConcertSchema(ma.ModelSchema):
    class Meta:
        model = Concert


class PerformanceSchema(ma.ModelSchema):
    class Meta:
        model = Performance

    song = ma.Nested(SongSchema)
    concert = ma.Nested(ConcertSchema)


"""
ROUTES
"""


@app.route("/")
def index():
    results = get_performances()
    return render_template("index.html", results=results)


def get_performances():
    perfs = Performance.query.all()
    performance_schema = PerformanceSchema(many=True)
    return performance_schema.dump(perfs)


@app.route("/api/performances/<int:id>")
def get_performance_single(id):
    perf = Performance.query.get(id)
    performance_schema = PerformanceSchema()
    return performance_schema.dump(perf)
