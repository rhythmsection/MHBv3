from flask import Flask, session, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
from model import connect_to_db, db, Fingerprint
import fingerprint
import cPickle
import os
import comparison
import time
import json



app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

#Where the music goes.
app.config['UPLOAD_FOLDER'] = ''


@app.route("/")
def index():

	'''Load main app page.'''

	songs_in_db = Fingerprint.query.all()
	return render_template("admin.html", songs_in_db = songs_in_db)


@app.route('/database')
def database_tools():

	'''Load database tools page.'''

	songs_in_db = Fingerprint.query.all()
	return render_template("database.html", songs_in_db = songs_in_db)

@app.route('/mini_base')
def user_database():
	songs_in_db = Fingerprint.query.all()
	return render_template("tiny_database.html", songs_in_db = songs_in_db)


@app.route('/add_fingerprint', methods = ['POST'])
def add_fingerprint():

	'''Add individual music data (including fingerprint) to database.'''

	title = request.form.get('title')
	artist = request.form.get('artist')
	music_file = request.files['music_file']
	filename = secure_filename("user_input.wav")
	music_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	comparison.change_stereo_to_mono(filename)
	time.sleep(1)
	music_fingerprint = fingerprint.location_fingerprint(filename)
	pickled_song_fingerprint = cPickle.dumps(music_fingerprint)
	new_fingerprint = Fingerprint(title = title,
								  artist = artist,
								  fingerprint = pickled_song_fingerprint)

	db.session.add(new_fingerprint)
	db.session.commit()

	return redirect("/database")


@app.route('/empty_database', methods=["POST"])
def empty_database():

	'''Delete entire contents of database.'''

	database_entries = Fingerprint.query.all()
	for entry in database_entries:
		db.session.delete(entry)
	db.session.commit()
	return redirect("/database")


@app.route("/delete_song")
def delete_song():

	'''Delete song by id from database.'''

	id = int(request.args.get("delete_song"))
	unwanted_song = Fingerprint.query.get(id)
	db.session.delete(unwanted_song)
	db.session.commit()
	return redirect("/database")


@app.route('/testing')
def testing_tools():

	'''Load testing page.'''

	songs_in_db = Fingerprint.query.all()
	return render_template("testing.html", songs_in_db = songs_in_db)


@app.route('/mini_app')
def testing_app():

	'''Load testing version of MHB. (No Angular, no graphics.)'''

	return render_template("admin_mhb.html")


@app.route('/full_app')
def load_app():

	'''Load user version of MHB.'''

	return render_template("mhb.html")
	

@app.route('/music_recognition', methods=['POST'])
def run_algorithm():

	'''AJAX call takes in the file from getUserMedia, names it "user_input.wav", 
	uploads it and then runs compare_fingerprint_to_database on it, returning 
	the results as a JSON object.'''

	music_file = request.files['music_clip']
	filename = secure_filename("user_input.wav")
	music_file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	comparison.change_stereo_to_mono(filename)
	time.sleep(1)
	database_iteration = comparison.compare_fingerprint_to_database("new_user_input.wav")
	return json.dumps(database_iteration)



if __name__ == "__main__":
    app.debug = True
    connect_to_db(app)
    app.run()