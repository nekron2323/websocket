from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()
CLIENT_FOLDER = '../client'
HTML_FILE = '/index.html'

client_messages = {}

class Messages:
    def __init__(self):
        self.messages = {}
        self.messages_count = 0

    def add_message(self, message):
        self.messages_count += 1
        self.messages[self.messages_count] = message


@app.get('/')
async def get():
    return FileResponse(CLIENT_FOLDER + HTML_FILE)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    messages = Messages()
    try:
        while True:
            data = await websocket.receive_json()
            if data['text']:
                messages.add_message(data['text'])
                await websocket.send_json(data)
    except WebSocketDisconnect:
        client_messages[websocket] = messages.messages
