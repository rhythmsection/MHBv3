import fingerprint
import sys
import model
import base_app
import cPickle
import os
import subprocess
import collections


def change_stereo_to_mono(filename):

	'''
	Change the submitted .wav file from stereo (default through getUserMedia()) to mono 
	for easier fingerprinting.

	'''

	if os.path.exists("new_user_input.wav"):
		os.remove("new_user_input.wav")
	ffmpeg_command = "ffmpeg -i user_input.wav -ac 1  new_user_input.wav" 
 	f_ffmpeg=subprocess.Popen(ffmpeg_command, shell=True)
  	return


def align(audio1, audio2):

	'''
	Align fingerprint to fingerprint and determine time offset
	ex. sig = [ (freq, time), (freq, time) ]

	'''

	aligned_frequencies = {}
	histogram = {}
	
	for peak in audio1:
		freq, time = peak
		if not aligned_frequencies.get(freq):
			aligned_frequencies[freq] = ([], [])

		aligned_frequencies[freq][0].append(time)

	for peak in audio2:
		freq, time = peak
		if not aligned_frequencies.get(freq):
			aligned_frequencies[freq] = ([], [])

		aligned_frequencies[freq][1].append(time)

	for freq, timings in aligned_frequencies.items():
		audio1_timings = timings[0]
		audio2_timings = timings[1]

		for t1 in audio1_timings:
			for t2 in audio2_timings:
				delta = t2-t1
				histogram[delta] = histogram.get(delta, 0) + 1

	matches = histogram.items()
	ranked_matches = sorted(matches, key=lambda x: x[1], reverse=True)
	return ranked_matches


def compare_fingerprint_to_database(filename):

	'''
	Takes the mono .wav file and creates a fingerprint of it, which it then compares 
	to the existing database of fingerprints, returning information of most likely match.

	'''

	user_audio = fingerprint.location_fingerprint(filename)
	fingerprints = model.Fingerprint.query.all()
	database_iteration = []
	max_offset = 0
	for row in fingerprints:
		db_audio = cPickle.loads(row.fingerprint)
		ranked_matches = align(user_audio, db_audio)
		current_song = {}
		song_match = {}

		current_song["title"] = row.title
		current_song["artist"] = row.artist
		current_song["offset"] = ranked_matches[0][1]
		current_song["high_match"] = False
		database_iteration.append(current_song)

	for current_song in database_iteration:
		if current_song["offset"] > max_offset:
			max_offset = current_song["offset"]

	for current_song in database_iteration:
		if current_song["offset"] == max_offset:
			current_song["high_match"] = True

	return database_iteration


if __name__ == '__main__':	
	compare_fingerprint_to_database(filename)


