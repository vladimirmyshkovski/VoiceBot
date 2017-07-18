from sanic import Sanic
from sanic.response import json, file
from sanic_session import InMemorySessionInterface
from os.path import join, dirname, realpath
from text_to_speach import text_to_speach
import string
import random
import requests

def generator(size=36, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))


app = Sanic()
app.static('/resources', './resources')
si = InMemorySessionInterface()


@app.middleware('request')
async def add_session_to_request(request):
    await si.open(request)


@app.middleware('response')
async def save_session(request, response):
    await si.save(request, response)


@app.route("/")
async def test(request):
    response = file(join(dirname(__file__),'websocket.html'))
    if not request['session'].get('sessionid'):
        request['session']['sessionid'] = generator()
    return await response

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
            "sessionid": request['session']['sessionid']
        }
        r = requests.get('http://localhost:5000/api/v1.0/ask', data)
        await ws.send(r.json()['response']['answer'])#bot_input.serialize()['text'])
        #await file(join(dirname(__file__),'resources/text.wav'.format(filename)))



if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
