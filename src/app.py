from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import os
import canvas

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

@app.get('/api/canvas/{track_id}')
def get_track_canvas(track_id):
    try:
        access_token = canvas.get_access_token()
        canvas_url = canvas.get_canvas_for_track(access_token, track_id)
        return {'success': 'true', 'canvas_url': canvas_url}
    except AttributeError:
        return {'success': 'false', 'message': 'No canvas found for this track'}
    except ConnectionError:
        return {'success': 'false', 'message': 'Failed to connect to Spotify'}
    except Exception as e:
        return {'success': 'false', 'message': f'Authentication error: {str(e)}'}

@app.get('/api/health')
def health():
    return "up"
