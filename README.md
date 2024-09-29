# Piano-Tutor

This project aims to find a method for piano learners to assess their performance during self-practice. After users inputs their recordings of piano pieces, this app can compare them with samples, and generate feedback about users’ performances, which are scored in three dimensions as below. 

- Tempo: Tempo is the speed or pace of a music piece. The app can extract the tempo from the recording in BPM with librosa.beat. 
- Strength: Strength is the change of volume. Librosa.onset.onset_strength is used to find the strength changing over time. To avoid influences of noise, we need to filter the data, keeping data at the onset of notes only.
- Note Accuracy: To find whether the user plays the correct notes, librosa.cqt is used to generate a constant-Q spectrogram using librosa.cqt. We can get a chroma vector with a 12-elements feature describing the energy of each pitch class ({C, C#, D, D#, E, ..., B}), and extract the pitch of notes as an array.
- The information extracted from the recording and the sample about strength and note accuracy will be turned into time series, and the dynamic time warping (DTW) algorithm will be applied to find the best alignment and calculate their similarity.

## To run the program:  
1: open the terminal  
2: open the folder "fyp19069" in terminal  
3: run the command "python3 interface.py"  
