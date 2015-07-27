import scipy
import numpy
import collections
from scipy.io import wavfile
from numpy.fft import rfft
import math
import sys
import hashlib

NUM_POCKETS = 60


def slice_some_data(filename):

	'''
	Turn the music data into frequencies using fourier transform and store them in 
	dictionary "bins" to iterate over them. Data is separated by frequency subsets
	with a 50 percent overlap. 44100Hz per second. 

	'''
	
	rate, data = wavfile.read(filename)
	index = 0
	bins = collections.defaultdict(list)
	for i in range(0, len(data), 11025):
		slice = data[i:i+22050]
		fourier_transformed = rfft(slice)
		for frequency in fourier_transformed:
			bins[index].append(frequency.real)
		index += 1
	return bins


def slice_frequencies_into_log_pockets(bin_key, bins):

	'''
	Within each bin, separates the frequencies again into logarithmically built pockets, 
	using the global NUM_POCKETS variable as determined above. Note that frequency is defined
	by location, hence the use of enumerate.

	'''

	bin_location = bins[bin_key]
	max_frequencies_in_bin = []
	amplitudes_in_pocket = []
	frequencies_in_bin = []

	max_log_idx = math.log10(len(bin_location))
	pocket_size = float(max_log_idx)/NUM_POCKETS

	#pockets is a list of lists--that is each of the pockets in a bin. 
	pockets = [ [] for x in range(NUM_POCKETS) ]
	
	for frequency, amplitude in enumerate(bin_location):
		if frequency == 0:
			continue
		log_index = math.log10(frequency)
		pocket_idx = int(log_index/pocket_size)
		pockets[min(pocket_idx, NUM_POCKETS-1)].append((abs(amplitude), frequency))
	return pockets


def find_pocket_max(pockets):

	'''
	Find the max amplitude in pocket.

	'''

	max_pockets = []
	for p in pockets[5:]:
		if p:
			max_pockets.append((max(p), p.index(max(p))))
	return max_pockets


def trim_minimum_amplitudes(max_pockets):

	'''
	Trims the actual max amplitudes by pocket in each bin by a minimum amplitude
	to filter out very low amplitude "noise"

	'''

	trimmed_max_pockets = []
	min_amp = 1000.0
	for max_number in max_pockets:
		if max_number[0][0] > min_amp:
		#max frequency and index of max_frequency ala original pockets idx
			trimmed_max_pockets.append((max_number[0][1], max_number[1]))
	return trimmed_max_pockets


def assigning_time_to_frequency_points(music_fingerprint):

	'''
	Assigns frequencies to time based locations via index.

	'''

	frequency_pair_list = []
	for idx, trimmed_max_pockets in enumerate(music_fingerprint):
		for number in trimmed_max_pockets:
			frequency_pair_list.append((number, idx))
	return frequency_pair_list


def location_fingerprint(filename):

	'''
	Full fingerprint build relying on prior functions.

	'''

	raw_fingerprint = []
	bins = slice_some_data(filename)
	bin_count = len(bins)
	for idx, bin in enumerate(bins):
		pockets = slice_frequencies_into_log_pockets(bin, bins)
		max_pockets = find_pocket_max(pockets)
		trimmed_max_pockets = trim_minimum_amplitudes(max_pockets)
		raw_fingerprint.append(trimmed_max_pockets)

	location_fingerprint = assigning_time_to_frequency_points(raw_fingerprint)
	return location_fingerprint


if __name__ == '__main__':	
	location_fingerprint(filename)