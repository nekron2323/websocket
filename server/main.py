from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()
CLIENT_FOLDER = '../client'
HTML_FILE = '/index.html'

client_messages = {}


@app.get('/')
async def get():
    return FileResponse(CLIENT_FOLDER + HTML_FILE)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    messages = {}
    messages_count = 0
    try:
        while True:
            data = await websocket.receive_json()
            if data['text']:
                messages_count += 1
                messages[messages_count] = data['text']
                await websocket.send_json(data)
    except WebSocketDisconnect:
        client_messages[websocket] = messages
