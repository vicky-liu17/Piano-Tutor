from os import path
from pydub import AudioSegment

# files                                                                         
# src = "Rain.mp3"
# dst = "Rain.wav"

# convert wav to mp3                                                            
def convert(src, dst):
	sound = AudioSegment.from_mp3(src)
	sound.export(dst, format="wav")