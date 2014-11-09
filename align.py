def align(sig1, sig2):
	"""Align signature 1 to signature 2 and determine time offset"""

	aligned_frequencies = {}
	histogram = {}

	# Roughly, sig1 is a list of time/frequency pairs
	# sig1 = [ (freq,time), (freq, time)]
	for peak in sig1:
		freq, time = peak
		if not aligned_frequencies.get(freq):
			aligned_frequencies[freq] = ([], [])

		aligned_frequencies[freq][0].append(time)

	for peak in sig2:
		freq, time = peak
		if not aligned_frequencies.get(freq):
			aligned_frequencies[freq] = ([], [])

		aligned_frequencies[freq][1].append(time)

	for freq, timings in aligned_frequencies.items():
		sig1_timings = timings[0]
		sig2_timings = timings[1]

		for t1 in sig1_timings:
			for t2 in sig2_timings:
				delta = t2-t1
				histogram[delta] = histogram.get(delta, 0) + 1

	matches = histogram.items()
	ranked_matches = sorted(matches, key=lambda x: x[1], reverse=True)
	return ranked_matches


