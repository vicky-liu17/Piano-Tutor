#!/usr/bin/python3
 
import tkinter
import record
from record import Recording
import play
import os
from play import playAudio
from play import play_audio
from tkinter import messagebox
import time
from tkinter import filedialog
from tools import Homepage
from converter import convert
from analyse import Analysis
#from plot import wavePlot

def recordMusic():
   rec = Recording()
   global theFile
   localtime = time.asctime( time.localtime(time.time()))
   rec.start()
   hideHome(B1, B3, B8)
   b = tkinter.messagebox.askokcancel('tips', 'Recording...\nPress OK to stop.')

   if b:
   		print("Stop recording")
   		rec.stop()
   		
   		theFile = localtime + ".wav"
   		rec.save(theFile)

   		#wavePlot(theFile)
   		messagebox.showinfo( "Notification", "Your recording has been saved.")
   		
   		B2 = App.getNewButton("Rename", 1, 1)
   		B5 = App.getNewButton("Back", 3, 0)
   		B6 = App.getNewButton("Play", 0, 1)
   		B7 = App.getNewButton("Delete", 2, 1)
   		B11 = App.getNewButton("Analyse", 3, 1)

   		B2['command'] = lambda: Rename(B2,B5,B6, B7, B11)
   		B5['command'] = lambda: switchButton(B1, B2, B5, B6, B7, B3, B8, B11)
   		B7['command'] = lambda: [switchButton(B1, B2, B5, B6,  B7, B3, B8, B11), delete(theFile)]
   		B6['command'] = lambda: play_audio(theFile)
   		B11['command'] = lambda: goToAnalyse(B1, B3, B8, B2, B5, B6, B7, B11)
   		#wavePlot(theFile)
   		
   else:
   		rec.stop()
   		appearHome(B1, B3, B8)

def delete(my_file):
	if os.path.exists(my_file):
		os.remove(my_file)

def hideHome(B1, B3, B8):
	App.hide(B1)
	App.hide(B3)
	App.hide(B8)

def appearHome(B1, B3, B8):
	App.appear(B1)
	App.appear(B3)
	App.appear(B8)

def localFile():
	a=tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("wav files","*.wav")])
	print(a)
	global theFile
	if a.endswith(".wav") and len(a)>4:
		theFile = a

		B6 = App.getNewButton("Play", 0, 1)
		B6['command'] = lambda: play_audio(theFile)
		B5 = App.getNewButton("Back", 1, 1)
		B5['command'] = lambda: continueTo(B5, B6, B1, B3, B8, B11)
		B11 = App.getNewButton("Analyse", 2, 1)
		B11['command'] = lambda: goToAnalyse2(B1, B3, B8, B5, B6, B11)


		hideHome(B1, B3, B8)

def continueTo(B5, B6, B1, B3, B8, B11):
	B5.grid_forget()
	B6.grid_forget()
	B11.grid_forget()
	appearHome(B1, B3, B8)

def Rename( B2, B5,B6, B7, B11):
	global theFile

	e1 = App.getNewEntry(1, 2, theFile)
	B4 = App.getNewButton("OK", 1, 3)
	B4['command'] = lambda:saveNewName(e1, B4, B2, B6, B5, B7, B11)
	
	App.hide(B2)
	App.hide(B5)
	App.hide(B7)
	App.hide(B11)


def saveNewName(e1, B4, B2, B6, B5, B7, B11):
	print(e1.get())
	newName = e1.get()
	global theFile
	#print ("目录为: %s"%os.listdir(os.getcwd()))
	if not newName.endswith(".wav"):
            newName = newName + ".wav"	
	i = 1
	dulplicate = False
	while (os.path.exists(newName)):
		if dulplicate:
			newName = newName[:-7] + "("+str(i)+").wav"
		else:
			newName = newName[:-4] + "("+str(i)+").wav"
		i+=1
		dulplicate = True

	os.rename(theFile, newName)
	theFile = newName
	#print ("目录为: %s" %os.listdir(os.getcwd()))
	B4.grid_forget()
	e1.grid_forget()
	App.appear(B2)
	App.appear(B5)
	App.appear(B7)
	App.appear(B11)
	

def switchButton(B1, B2, B5, B6, B7, B3, B8, B11):
	B2.grid_forget()
	B5.grid_forget()
	B6.grid_forget()
	B7.grid_forget()
	B11.grid_forget()

	theFile = ""
	appearHome(B1, B3, B8)

def getSelection(sb, lb, B9, B10, B1):
	restore(sb, lb, B9, B10)
	global theFile
	value = lb.get(lb.curselection())
	print(value)
	if value.endswith(".wav") and value != ".wav":
		theFile = value
	
	B2 = App.getNewButton("Rename", 1, 1)
	B5 = App.getNewButton("Back", 3, 0)
	B6 = App.getNewButton("Play", 0, 1)
	B7 = App.getNewButton("Delete", 2, 1)
	B11 = App.getNewButton("Analyse", 3, 1)
	B2['command'] = lambda: Rename(B2,B5, B6, B7,B11)
	B5['command'] = lambda: switchButton(B1, B2, B5, B6, B7, B3, B8, B11)
	B7['command'] = lambda: [switchButton(B1, B2, B5, B6,  B7, B3, B8, B11), delete(theFile)]
	B6['command'] = lambda: play_audio(theFile)
	B11['command'] = lambda: goToAnalyse(B1, B3, B8, B2, B5, B6, B7, B11)

	

def restore(sb, lb, B9, B10):
	B9.grid_forget()
	B10.grid_forget()
	sb.grid_forget()
	lb.grid_forget()

def goToAnalyse(B1, B3, B8, B2, B5, B6, B7, B11):
	
	hideHome(B1, B3, B8)
	App.hide(B2)
	App.hide(B5)
	App.hide(B6)
	App.hide(B7)
	App.hide(B11)
	B12 = App.getNewButton("Load Sample", 0, 2, "nw", 14, 2)
	B13 = App.getNewButton("Back", 0, 3)
	B12['command'] = lambda: loadSample(B12, B13)
	B13['command'] = lambda: backAnalyse(B2, B5, B6, B7, B11, B12, B13)


def backAnalyse(B2, B5, B6, B7, B11, B12, B13):
	App.appear(B2)
	App.appear(B5)
	App.appear(B6)
	App.appear(B7)
	App.appear(B11)
	B12.grid_forget()
	B13.grid_forget()

def goToAnalyse2(B1, B3, B8, B5, B6, B11):
	fromFile = True
	hideHome(B1, B3, B8)
	App.hide(B5)
	App.hide(B6)
	App.hide(B11)
	B12 = App.getNewButton("Load Sample", 0, 2, "nw", 14, 2)
	B13 = App.getNewButton("Back", 0, 3)
	B12['command'] = lambda: loadSample(B12, B13)
	B13['command'] = lambda: backAnalyse2(B5, B6, B11, B12, B13)

def backAnalyse2(B5, B6, B11, B12, B13):
	App.appear(B5)
	App.appear(B6)
	App.appear(B11)
	B12.grid_forget()
	B13.grid_forget()

def loadSample(B12, B13):
	a=tkinter.filedialog.askopenfilename(initialdir = "/",title = "Select file",filetypes = [("wav files","*.wav"), ("mp3 files","*.mp3")])
	#print(a)
	global sampleFile
	global theFile
	if a.endswith(".wav") and len(a)>4:
		sampleFile = a
	elif a.endswith(".mp3") and len(a)>4:
		newName = a[:-4]+".wav"
		convert(a, newName)
		sampleFile = newName

	print(sampleFile)
	B12.grid_forget()
	#App.getNewLabel(sampleFile, 6, 0)
	App.moveItem(B13, 3, 3)

	

	if(theFile != "" and theFile.endswith(".wav") and sampleFile != "" and sampleFile.endswith(".wav")):
		App.hide(B13)
		B14 = App.getNewButton("Tempo", 0, 3)
		B15 = App.getNewButton("Strength", 1, 3)
		B16 = App.getNewButton("Accuracy", 2, 3)
		assessment = Analysis(theFile, sampleFile)
		tempo = assessment.getTempo()
		strength = assessment.strength()
		accuracy = assessment. accuracy()
		averageScore = assessment.calculateAverage()

		

		label1 =App.getNewLabel("Tempo: ", 0, 4)
		label2 = App.getNewLabel("Strength: ", 1, 4)
		label3 = App.getNewLabel("Accuracy: ", 2, 4)
		label4 = App.getNewLabel("Average: ", 3, 4)

		label5 = App.getNewLabel(tempo, 0, 5)
		label6 = App.getNewLabel(strength, 1, 5)
		label7 = App.getNewLabel(accuracy, 2, 5)
		label8 = App.getNewLabel(averageScore, 3, 5)

		B14['command'] = lambda: messagebox.showinfo( "Tempo", assessment.comment())
		B15['command'] = lambda: assessment.strengthGraph()
		B16['command'] = lambda: assessment.accuracyGraph()

		B17 = App.getNewButton("Clear", 0, 6)
		B17['command'] = lambda: clear(B13, B14, B15, B16, B17, label1, label2, label3, label4, label5, label6, label7, label8)


def clear(B13, B14, B15, B16, B17, label1, label2, label3, label4, label5, label6, label7, label8):
	label1.grid_forget()
	label2.grid_forget()
	label3.grid_forget()
	label4.grid_forget()
	label5.grid_forget()
	label6.grid_forget()
	label7.grid_forget()
	label8.grid_forget()
	B14.grid_forget()
	B15.grid_forget()
	B16.grid_forget()
	B17.grid_forget()
	App.appear(B13)
	App.moveItem(B13, 0, 3)


def getHistory():
	dir = os.listdir(os.getcwd())
	#print ("目录为: %s" %dir)
	List = []
	for file in dir:
		if file.endswith(".wav") and str(file) != ".wav":
			List.append(str(file))

	sb = App.getScrollbar(2, 2)
	lb =  App.getListbox(2, 1, List, sb)
	sb.config(command=lb.yview)
	lb.select_set(0, 0)
	B9 = App.getNewButton("Select", 0, 1, 'ew')
	B9['command'] = lambda: getSelection(sb, lb, B9, B10, B1)
	
	B10 = App.getNewButton("Cancel", 1, 1, 'ew')
	B10['command'] = lambda: [restore(sb, lb, B9, B10), appearHome(B1, B3, B8)]

	hideHome(B1, B3, B8)



root = tkinter.Tk()
theFile = ""
sampleFile = ""

App = Homepage(root, "Piano Tutor")
App.setInterface()

B1 = App.getNewButton("Record", 0, 0)
B1["command"] = recordMusic
B3 = App.getNewButton("Local File", 1, 0)
B3["command"] = localFile
B8 = App.getNewButton("History", 2, 0)
B8["command"] = getHistory

root.mainloop()