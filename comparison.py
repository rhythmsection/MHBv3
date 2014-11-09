import fingerprint
import sys
import model
import base_app
import pickle
import os
import subprocess
import collections
import align

session = model.connect()


#Change the submitted .wav file from stereo (default through getUserMedia() to mono for easier fingerprinting.)
def change_stereo_to_mono(filename):
	if os.path.exists("new_user_input.wav"):
		os.remove("new_user_input.wav")
	ffmpeg_command = "ffmpeg -i user_input.wav -ac 1  new_user_input.wav" 
 	f_ffmpeg=subprocess.Popen(ffmpeg_command, shell=True)
  	return

#Takes the mono .wav file and creates a fingerprint of it, which it then compares to the existing database
#of fingerprints, returning results.
def compare_fingerprint_to_database(filename):
	file1 = fingerprint.location_fingerprint(filename)
	fingerprints = session.query(model.Fingerprint)
	database_iteration = []
	max_offset = 0
	for row in fingerprints:
		file2 = pickle.loads(row.fingerprint)
		ranked_matches = align.align(file1, file2)
		current_song = {}
		song_match = {}

#assorted song information
		current_song["title"] = row.title
		current_song["artist"] = row.artist
		current_song["album"] = row.album
		current_song["offset"] = ranked_matches[0][1]
		database_iteration.append(current_song)

	for current_song in database_iteration:
		if current_song["offset"] > max_offset:
			max_offset = current_song["offset"]

#information for most likely match
	for current_song in database_iteration:
		if current_song["offset"] == max_offset:
			song_match["title"] = current_song["title"]
			song_match["artist"] = current_song["artist"]
			song_match["album"] = current_song["album"]

	return song_match

def main(filename):
	compare_fingerprint_to_database(filename)


