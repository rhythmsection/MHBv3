import os
import fingerprint
import model
import sys
import pickle

wav_file = sys.argv[1]

session = model.connect()

#creates and stores fingerprints for individual songs. 
def load_test_data(wav_file):
	song_fingerprint = fingerprint.location_fingerprint(wav_file)
	pickled_song_fingerprint = pickle.dumps(song_fingerprint)
	song = model.Fingerprint(fingerprint = pickled_song_fingerprint)
	session.add(song)
	session.commit()

def main(wav_file):
	load_test_data(wav_file)

if __name__ == '__main__':
	main(wav_file)

