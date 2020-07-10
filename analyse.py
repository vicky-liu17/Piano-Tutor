from __future__ import print_function
import matplotlib.pyplot as plt
import vamp
import librosa.display
import librosa
import scipy.stats
from scipy.spatial.distance import euclidean
import numpy as np
from fastdtw import fastdtw
import pandas as pd

class Analysis:

	def __init__(self, TEST, SAMPLE):
		self.test = TEST
		self.sample = SAMPLE
		self.dict = {"Larghissimo": 0,  "Grave":1,  "Lento":2, "Larghetto": 3,
		"Adagio":4,  "Andante": 5, "Moderato": 6, "Allegro": 7, 
		 "Vivace": 8, "Presto": 9, "Prestissimo": 10}
		self.charact = ["very, very slow (25 bpm and under)",  "slow and solemn(25–45 bpm)", 
		"slowly(45–60 bpm)", "rather broadly (60–66 bpm)", "slowly with great expression(66–76 bpm)",
		"at a walking pace (76–100 bpm)", "at a moderate speed (100–120 bpm)",
		"fast, quick, and bright (120–156 bpm) ", "lively and fast (156–176 bpm)", 
		"very fast (176–200 bpm)", "very very fast (200 bpm and over)"]
		self.tempoScore = 0
		self.strengthScore = 0
		self.accuracyScore = 0
		self.result = ""
		self.result2 = ""

		self.y, self.sr = librosa.load(SAMPLE, sr=None,duration=None)
		self.y2, self.sr2 = librosa.load(TEST, sr=None,duration=None)

		self.o_env = librosa.onset.onset_strength(self.y, sr=self.sr)
		self.tempo = librosa.beat.tempo(onset_envelope=self.o_env, sr=self.sr)

		self.o_env2 = librosa.onset.onset_strength(self.y2, sr=self.sr2)
		self.tempo2 = librosa.beat.tempo(onset_envelope=self.o_env2, sr=self.sr2)

		self.onset_frames = librosa.onset.onset_detect(y=self.y, sr=self.sr)
		self.onset_time = librosa.frames_to_time(self.onset_frames, sr=self.sr)

		self.onset_frames2 = librosa.onset.onset_detect(y=self.y2, sr=self.sr2)
		self.onset_time2 = librosa.frames_to_time(self.onset_frames2, sr=self.sr2)

		self.chroma=librosa.feature.chroma_cqt(y=self.y, sr=self.sr)
		self.chroma2=librosa.feature.chroma_cqt(y=self.y2, sr=self.sr2) 

		self.note_values = self.getNotes(self.chroma)
		self.note_values2 = self.getNotes(self.chroma2)

		self.times = librosa.times_like(self.o_env, sr=self.sr)
		self.times2 = librosa.times_like(self.o_env2, sr=self.sr2)

	def evaluateTempo(self, value):
		result = ""
		if(value<=25):
			result = "Larghissimo"
		elif(value>25 and value<=45):
			result = "Grave"
		elif(value>45 and value<=60):
			result = "Lento"
		elif(value>60 and value<=66):
			result = "Larghetto"
		elif(value>66 and value<=76):
			result = "Adagio"
		elif(value>76 and value<=100):
			result = "Andante"
		elif(value>100 and value<=120):
			result = "Moderato"
		elif(value>120 and value<=156):
			result = "Allegro"
		elif(value>156 and value<=176):
			result = "Vivace"
		elif(value>176 and value<=200):
			result = "Presto"
		else:
			result = "Prestissimo"

		return result



	def getTempo(self):

		#print(self.tempo[0])
		self.result = self.evaluateTempo(self.tempo[0])
		print(self.result)
		#print(self.charact[self.dict[result]])

		#print(self.tempo2[0])
		self.result2 = self.evaluateTempo(self.tempo2[0])
		print(self.result2)
		#print(self.charact[self.dict[result2]])

		self.tempoScore = 10 - abs(self.dict[self.result2] - self.dict[self.result])
		#print("Tempo: ")
		#print(self.tempoScore)
		return str(self.tempoScore)

	def makeList(self, frames, item):
		List = []
		for i in frames:
			List.append(item[i])

		return List

	def makeArray(self, x, y):
		a = np.array([x[0],y[0]])
		for i in range (1, len(y)):
			b = np.array([x[i], y[i]])
			a = np.vstack((a, b))

		return a

	def getSimilarity(self, x, y):
		distance, path = fastdtw(x, y ,dist=euclidean)
		averageTime = (librosa.get_duration(y=self.y, sr=self.sr) + librosa.get_duration(y=self.y2, sr=self.sr2))/2
		similarity = distance/averageTime
		return similarity

	def getNotes(self, chroma):
		c=pd.DataFrame(chroma)
		c0=(c==1)
		c1=c0.astype(int)
		labels=np.array(range(1,13))
		note_values=labels.dot(c1)
		return note_values

	def strength(self):

		List = self.makeList(self.onset_frames, self.o_env)
		List2 = self.makeList(self.onset_frames2, self.o_env2)


		array1 = self.makeArray(self.onset_time, List)
		array2 = self.makeArray(self.onset_time2, List2)

		similarity = self.getSimilarity(array1, array2) - 2

		if(similarity < 0):
			similarity = 0
		elif(similarity > 10):
			similarity = 10
		self.strengthScore = 10 - round(similarity)
		
		return str(self.strengthScore)

	def accuracy(self):
		
		notes = self.filter(self.note_values, self.onset_frames)
		notes2 = self.filter(self.note_values2, self.onset_frames2)
		array1 = self.makeArray(self.times, notes)
		array2 = self.makeArray(self.times2, notes2)

		similarity = self.getSimilarity(array1, array2)
		self.accuracyScore = 10 - round((similarity - 150)/100)
		
		if(self.accuracyScore < 0):
			self.accuracyScore = 0
		elif(self.accuracyScore > 10):
			self.accuracyScore = 10
		
		return str(self.accuracyScore)

	def calculateAverage(self):
		av = (self.tempoScore + self.strengthScore + self.accuracyScore)/3
		return round(av, 2)


	def filter(self, notes, frame):
		var = notes[0]
		num = notes.shape[0]
		counter = 0
		for i in range (0, num):
			if(i == frame[counter]):
				var = notes[i]
				if(counter < len(frame) -1):
					counter+=1
			notes[i] = var
		return notes

	def accuracyGraph(self):

		notes = self.filter(self.note_values, self.onset_frames)
		notes2 = self.filter(self.note_values2, self.onset_frames2)
		plt.figure()
		plt.grid(linewidth=0.5)
		plt.yticks(range(1,13),["C","C#","D","D#","E","F","F#","G","G#","A","A#","B"])
		plt.scatter(self.times,notes,marker="s",s=10,color="green", label='sample', alpha = 0.3)
		plt.scatter(self.times2,notes2,marker="s",s=0.75,color="red", label='recording')
		# plt.plot(self.times, self.note_values, color = 'green', alpha=0.3, lw = 0.5, )
		# plt.plot(self.times2, notes2, color = 'red', alpha=0.3, lw = 0.5, )
		plt.show()

	def strengthGraph(self):
		plt.figure()
		plt.subplots_adjust(wspace=1.5, hspace=0.5)
		plt.subplot(1,1,1)
		List = self.makeList(self.onset_frames, self.o_env)
		List2 = self.makeList(self.onset_frames2, self.o_env2)
		plt.plot(self.onset_time, List, color = 'green', label='Onset strength - sample')
		plt.plot(self.onset_time2, List2,color='red', alpha=0.9, label='Onset strength - recording')
		plt.xlabel('time(s)')
		plt.axis('tight')
		plt.legend(frameon=True, framealpha=0.75)
		plt.show()

	def comment(self):
		comments = ""
		if(self.dict[self.result2] == self.dict[self.result]):
			comments = "Well done! You did well in tempo!"
		elif(self.dict[self.result2] > self.dict[self.result]):
			comments = "You should play this piece of music " + self.charact[self.dict[self.result]] + ".\n" +"However, you played it " + self.charact[self.dict[self.result2]] + ".\n" + "You need to play a bit slower."
				
		else:
			comments = "You should play this piece of music " + self.charact[self.dict[self.result]] + ".\n" + "However, you played it " + self.charact[self.dict[self.result2]] + ".\n" + "You need to play a bit faster."

		return comments