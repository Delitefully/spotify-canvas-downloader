import requests
import random
from constants import *
from protos.canvas_pb2 import EntityCanvazRequest, EntityCanvazResponse

def get_access_token():
    try:
        response = requests.get(TOKEN_ENDPOINT)
        data = response.json()
        return data["accessToken"]
    except Exception as e:
        raise Exception(e)


def get_canvas_for_track(access_token, track_id):
    canvas_request = EntityCanvazRequest()
    canvas_request_entities = canvas_request.entities.add()
    canvas_request_entities.entity_uri = TRACK_URI_PREFIX + track_id

    try:
        resp = requests.post(
            API_HOST + CANVAS_ROUTE,
            headers={
                "Content-Type": "application/x-protobuf",
                "Authorization": "Bearer %s" % access_token
            },
            data=canvas_request.SerializeToString(),
        )
    except:
        raise ConnectionError

    canvas_response = EntityCanvazResponse()
    canvas_response.ParseFromString(resp.content)

    if(len(canvas_response.canvases) == 0):
        raise AttributeError

    canvas = random.choice(canvas_response.canvases)
    return canvas.url
