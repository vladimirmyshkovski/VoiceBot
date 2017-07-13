from chatterbot import ChatBot
import logging


logging.basicConfig(level=logging.INFO)
bot = ChatBot(
	'Norman',
	storage_adapter='chatterbot.storage.MongoDatabaseAdapter',
	input_adapter='chatterbot.input.VariableInputTypeAdapter',
	output_adapter='chatterbot.output.OutputAdapter',
	logic_adapters=[
		'chatterbot.logic.MathematicalEvaluation',
		'chatterbot.logic.TimeLogicAdapter',
		'chatterbot.logic.BestMatch'
	],
	database='localhost:27017'
)



def get_feedback():
	from chatterbot.utils import input_function

	text = input_function()

	if 'yes' in text.lower():
		return True
	elif 'no' in text.lower():
		return False
	else:
		return get_feedback()

DEFAULT_SESSION_ID = bot.default_session.id
