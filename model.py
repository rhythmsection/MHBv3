from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

####################################################

class Fingerprint(db.Model):

    __tablename__ = "fingerprints"

    id = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(50), nullable = True)
    artist = db.Column(db.String(50), nullable = True)
    fingerprint = db.Column(db.PickleType, nullable = True)


class AppTest(db.Model):

    __tablename__ = "apptests"

    id = db.Column(db.Integer, primary_key = True)
    song_played = db.Column(db.String(50), nullable = True)
    artist_played = db.Column(db.String(50), nullable = True)
    highest_match_title = db.Column(db.String(50), nullable = True)
    highest_match_artist = db.Column(db.String(50), nullable = True)
    highest_offset = db.Column(db.Integer, nullable = True)
    noise_level = db.Column(db.Integer, nullable = True)
    match = db.Column(db.Boolean, nullable = True)


def connect_to_db(app):
    app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///fingerprints.db'
    db.app = app
    db.init_app(app)


if __name__ == "__main__":

    from base_app import app
    connect_to_db(app)
    print "Connected to DB."

