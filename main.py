from sanic import Sanic
from sanic.response import json
from sanic.response import file
from bot import bot, DEFAULT_SESSION_ID
from chatterbot.conversation import Statement
from chatterbot.conversation import Response
from os.path import join, dirname, realpath
from text_to_speach import text_to_speach
import string
import random
import requests

def generator(size=36, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


app = Sanic()
app.static('/resources', './resources')

@app.route("/")
async def test(request):
    return await file(join(dirname(__file__),'websocket.html'))


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        #input_statement = bot.input.process_input_statement(data)
        #statement, response = bot.generate_response(input_statement, DEFAULT_SESSION_ID)
        question = await ws.recv()
        #bot_input = bot.get_response(data)
        #z = Response(data)
        #print('RESPONSE: ' + str(z))
        #print('STATEMENT: ' + str(Statement(data)))
        #print(bot_input.serialize()['text'])
        #filename = generator()
        #text_to_speach(bot_input.serialize()['text'], 'text')
        data = {
            "question": question,
            "sessionid": "1234567890"
        }
        r = requests.get('http://localhost:5000/api/v1.0/ask', data)
        await ws.send(r.json()['response']['answer'])#bot_input.serialize()['text'])
        #await file(join(dirname(__file__),'resources/text.wav'.format(filename)))
    	
@app.route("/train")
async def train(request):
    bot.train()
    return text('Trained database generated successfully!')

if __name__ == "__main__":
    app.run(
    	host="0.0.0.0",
    	port=8080,
    	debug=True
    )