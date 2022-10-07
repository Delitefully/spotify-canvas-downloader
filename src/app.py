from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import asyncio
import canvas
import google.protobuf

app = FastAPI()

ORIGIN = os.getenv('HOST_ORIGIN')
origins = [
    ORIGIN,
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

access_token = ""

@app.get('/api/canvas/{track_id}')
def get_track_canvas(track_id):
    try:
        canvas_url = canvas.get_canvas_for_track(access_token, track_id)
        return {'success': 'true', 'canvas_url': canvas_url}
    except AttributeError:
        return {'success': 'false', 'message': 'No canvas found for this track'}
    except ConnectionError:
        return {'success': 'false', 'message': 'failed to connect to Spotify'}

@app.get('/api/health')
def health():
    return "up"

async def refresh_token():
    global access_token
    while True:
        print('INFO:     Getting a fresh Spotify access token')

        try:
            access_token = canvas.get_access_token()
        except Exception as e:
            print('ERROR:   Failed to get a new access token: %s' % e)

        await asyncio.sleep(1800)

@app.on_event("startup")
async def startup_event():
    asyncio.get_event_loop().create_task(refresh_token())
