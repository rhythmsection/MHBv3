from flask import Flask, session, render_template, redirect, request, flash
from werkzeug.utils import secure_filename
import os
import comparison
import time
import json



app = Flask(__name__)
app.secret_key = '\xf5!\x07!qj\xa4\x08\xc6\xf8\n\x8a\x95m\xe2\x04g\xbb\x98|U\xa2f\x03'

#Where the music goes.
app.config['UPLOAD_FOLDER'] = ''

#Returns the "main page" with getUserMedia() API for recording.
@app.route("/")
def index():
    return render_template("receiveaudio.html")

#Takes in the file from getUserMedia, names it "user_input.wav", uploads it and then
#runs compare_fingerprint_to_database on it, returning the results as a JSON object. 
@app.route("/music_recognition", methods=['POST'])   
def music_recognition():
	file = request.files['user_audio']
	filename = secure_filename("user_input.wav")
	file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
	comparison.change_stereo_to_mono(filename)
	time.sleep(1)
	database_iteration = comparison.compare_fingerprint_to_database("new_user_input.wav")
	return json.dumps(database_iteration)


@app.route("/success")
def successful_ident():
	return render_template("generateresults.html")



if __name__ == "__main__":
    app.run(debug=True)