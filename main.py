from sanic import Sanic
from sanic.response import json, file
from sanic_session import InMemorySessionInterface
from os.path import join, dirname, realpath
from text_to_speach import text_to_speach
import string
import random
import requests
import ujson as j
import re


def generator(size=36, chars=string.ascii_uppercase + string.digits + string.ascii_lowercase):
    return ''.join(random.choice(chars) for _ in range(size))

def clear_sting(string):
    reg = re.compile('[^a-zA-Z ]')
    return ((reg.sub('', string).strip()).lower()).replace(' ', '-')

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
        question = await ws.recv()
        data = {
            "question": question,
            "sessionid": request['session']['sessionid']
        }
        r = requests.get('http://localhost/api/v1.0/ask', data)
        if r.status_code is not 200:
            answer = "Something went wrong"
        else:
            answer = r.json()['response']['answer']
        filename = clear_sting(answer)
        text_to_speach(answer, filename)
        await ws.send(j.dumps({
            "text": answer, 
            "filename": filename
            }))

if __name__ == "__main__":
    app.run(
        host="0.0.0.0",
        port=8080,
        debug=True
    )
