from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.responses import FileResponse

app = FastAPI()
CLIENT_FOLDER = '../client'
HTML_FILE = '/index.html'


class ConnectionManager:
    def __init__(self):
        self.message_count = 0
        self.messages = {}

    async def connect(self, websocket: WebSocket):
        await websocket.accept()


manager = ConnectionManager()


@app.get('/')
async def get():
    return FileResponse(CLIENT_FOLDER + HTML_FILE)


@app.websocket('/ws')
async def websocket_endpoint(websocket: WebSocket):
    await manager.connect(websocket)
    try:
        while True:
            data = await websocket.receive_json()
            if data['text']:
                manager.message_count += 1
                manager.messages[manager.message_count] = data['text']
                await websocket.send_json(data)
    except WebSocketDisconnect:
        pass
