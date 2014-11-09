

![alt tag](https://raw.githubusercontent.com/rhythmsection/MHB/master/static/readme/readme_logo.gif)
===


MyHipsterBoyfriend is a music recognition system that enables the user to record audio through their computer's microphone and compare it, using acoustic fingerprinting and interval matching, to a self-seeded database of existing acoustic fingerprints to find the best match for that song.


Technology Stack: Python (Libraries: ffmpeg, numpy, scipy), Flask, SQLAlchemy, SQLite, JSON, JavaScript, Angular.js, WebRTC, Recorder.js, HTML, CSS

###Set-Up

Before the magic happens, the user needs to create and store fingerprints for the database that the user wishes to query from. The following tools can help to streamline that process:

######(model.py)

Creates a SQLAlchemy class that establishes the needed variables for "fingerprints" table that holds the information necessary for comparison to a submitted music clip. 

######(seed.py)

Fills a pre-existing database with fingerprints in concert with the fingerprint.py acoustic fingerprinting algorithm, assigning them to unique ID numbers. Please note that, currently, the rest of the song information must be filled in manually. *For optimal results, a minimum of the song title (title) and artist name (artist) should be input into the database for each song*

###Implementation

To start this circuit, the user records audio using WebRTC, which requests access to the computer's microphone, recording ten seconds of audio. Using the Recorder.js plug-in, it saves that audio information as a .wav file, ready to be fingerprinted. 

######(fingerprint.py)

The fingerprinting algorithm works by taking in a mono .wav file and running a Fast Fourier Transform on the file, returning a location-ordered list of the amplitudes in the song. Since the amplitudes themselves are relative, the end result is ordered by frequencies determined by the individual locations of each of the amplitudes. 

Because of the large amount of data, the main goal of the algorithm is to create a stripped down model of the results of the Fourier transform, which starts by sorting the amplitudes in overlapped bins (currently 0.5 seconds long with a 50% overlap), and then sorting each bin into logarithmically determined 'pockets' containing frequency/amplitude pairs. It then uses the pockets to strip data, saving only the pair with the highest amplitude as the representative data for that pocket. 

Also in order to trim excess data, the algorithm trims any very low amplitudes. 0.0hz amplitudes are prevalent in almost any clip and not very helpful in creating unique signatures for any given song, so let's get rid of them! 

Finally, it discards the amplitudes and takes only the frequencies from the tuple data pairs, tying them to their respective time markers, indicated by the bins that hold them. This data (frequency, time) becomes the individual fingerprint. 

######(align.py)

In order to compare fingerprints between the submitted clip and the database, the algorithm looks for points that align and records the offset. For example, if the same frequencies occur within bin 4 in the clip and bin 23 in a song in the database, the offset would be 19. If the clip is from the song being queried, a high number of reoccuring offset intervals would be expected at the point where the song and the clip overlap. This returns a tally of those intervals.

######(comparison.py)

Finally, comparison.py brings the aforementioned processes together and combines them to iterate over the new clip and compare it to the entries in the database. 

###User Experience

######(receiveaudio.html)

The front-end uses HTML, CSS and JavaScript (including the magic of Angular.js, Recorder.js, GetUserMedia()) in order to create a user-friendly one-button input. The application requires and must be granted permission to use the computer's microphone through the browser's interface in order to activate functionality. *Please note that full-functionality is currently limited to modern Chrome browsers.*

![alt tag](https://raw.githubusercontent.com/rhythmsection/MHB/master/static/readme/screen_shot2.gif)
