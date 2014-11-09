import scipy
import numpy
import collections
from scipy.io import wavfile
from numpy.fft import rfft
import math
import sys
import hashlib

# a global variable that represents the number of pockets to split each bin into.
NUM_POCKETS = 60

'''If you want to fingerprint straight from the command line instead of using the interface'''
# filename = sys.argv[1]

#slice the data from the wav file into chunks. 
def slice_some_data(filename):
	#return the rate and the amount of data as separate variables.
	rate, data = wavfile.read(filename)
	index = 0
	#dictionary storage of all of the data
	bins = collections.defaultdict(list)
	#slices data into subsets based on the number of Hz. Note 50% overlap. 
	for i in range(0, len(data), 11025):
		slice = data[i:i+22050]
		#run fourier transform on each slice.
		fourier_transformed = rfft(slice)
		#assign these frequencies to bin entries in bin.
		for frequency in fourier_transformed:
			bins[index].append(frequency.real)
		index += 1
	return bins

#creates and stores frequencies from FFT into logarithmically filled pockets within each bin. 
def slice_frequencies_into_log_pockets(bin_key, bins):
	bin_location = bins[bin_key]
	max_frequencies_in_bin = []
	amplitudes_in_pocket = []
	frequencies_in_bin = []

	#the max log index of the entire bin.
	max_log_idx = math.log10(len(bin_location))
	#the MLI divided by the number of pockets (to find how high we go per pocket)
	pocket_size = float(max_log_idx)/NUM_POCKETS

	#pockets is a list of lists--that is each of the pockets in bin. 
	pockets = [ [] for x in range(NUM_POCKETS) ]
	
	#use enumerate to give both frequency and amplitude for each amp in the bin. Sort into pockets. 
	for frequency, amplitude in enumerate(bin_location):
		if frequency == 0:
			continue
		log_index = math.log10(frequency)
		pocket_idx = int(log_index/pocket_size)
		pockets[min(pocket_idx, NUM_POCKETS-1)].append((abs(amplitude), frequency))
	return pockets

#finds the max amp of each pocket. 
def find_pocket_max(pockets):
	max_pockets = []
	for p in pockets[5:]:
		if p:
			max_pockets.append((max(p), p.index(max(p))))
	return max_pockets

#trims the actual max amplitudes in each pockets by a minimum amplitude
def trim_minimum_amplitudes(max_pockets):
	trimmed_max_pockets = []
	min_amp = 1000.0
	for max_number in max_pockets:
		if max_number[0][0] > min_amp:
		#max frequency and index of max_frequency ala original pockets idx
			trimmed_max_pockets.append((max_number[0][1], max_number[1]))
	return trimmed_max_pockets

# assigning frequencies to time based locations
def assigning_time_to_frequency_points(music_fingerprint):
	frequency_pair_list = []
	for idx, trimmed_max_pockets in enumerate(music_fingerprint):
		for number in trimmed_max_pockets:
			frequency_pair_list.append((number, idx))
	return frequency_pair_list

#creates locational fingerprint
def location_fingerprint(filename):
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



def main(filename):
	location_fingerprint(filename)
	return location_fingerprint


if __name__ == '__main__':	
	main(filename)