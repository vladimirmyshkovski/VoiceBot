# coding=utf-8
import ujson as json
from os.path import join, dirname, realpath
from watson_developer_cloud import TextToSpeechV1
#from ..settings import text_to_speech as t
#from ..settings import UPLOAD_FOLDER
#text_to_speech = TextToSpeechV1(
#	username='e7ce4e67-f26d-4d85-afde-56dd9816e67d',
#	password='Ag7GeK1iX6Nj',
#	x_watson_learning_opt_out=True)  # Optional flag

text_to_speech = TextToSpeechV1(
	username='e7ce4e67-f26d-4d85-afde-56dd9816e67d',
	password='Ag7GeK1iX6Nj',
	x_watson_learning_opt_out=True)

def text_to_speach(text):
	#print(json.dumps(s.text_to_speech.voices(), indent=2))
	#print(join(dirname(__file__)-3))
	#print(os.path.join(os.path.dirname(__file__),'/static/resources/'))
	#s = join(dirname(__file__),'/resources/')
	#print(join(UPLOAD_FOLDER),, '/static/resources')
	with open(join(dirname(__file__),'resources/text.wav'),
	          'wb') as audio_file:
	    audio_file.write(
	        text_to_speech.synthesize(str(text), accept='audio/wav',
	                                  voice="en-US_AllisonVoice"))
	#print(
	#    json.dumps(text_to_speech.pronunciation(
	#        'Watson', pronunciation_format='spr'), indent=2))

	#print(json.dumps(text_to_speech.customizations(), indent=2))


