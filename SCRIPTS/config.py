import os
from dotenv import load_dotenv

class Config(object):
    load_dotenv()
    SECRET_KEY = os.urandom(24)
    SPOTIPY_CLIENT_ID = os.environ.get("SPOTIPY_CLIENT_ID")
    SPOTIPY_CLIENT_SECRET = os.environ.get("SPOTIPY_CLIENT_SECRET")
    SESSION_TYPE = 'filesystem'