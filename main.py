from sanic import Sanic
from sanic.response import json
from sanic.response import file
from bot import bot, DEFAULT_SESSION_ID
from chatterbot.conversation import Statement
from chatterbot.conversation import Response


app = Sanic()


@app.route("/")
async def test(request):
    return await file('websocket.html')


@app.websocket('/feed')
async def feed(request, ws):
    while True:
        #input_statement = bot.input.process_input_statement(data)
        #statement, response = bot.generate_response(input_statement, DEFAULT_SESSION_ID)
        data = await ws.recv()
        bot_input = bot.get_response(data)
        z = Response(data)
        print('RESPONSE: ' + str(z))
        print('STATEMENT: ' + str(Statement(data)))
        print(bot_input.serialize()['text'])
        await ws.send(bot_input.serialize()['text'])
    	

if __name__ == "__main__":
    app.run(
    	host="0.0.0.0",
    	port=8080,
    	debug=True
    )