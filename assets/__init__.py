# Assets package for game resources
import os

ASSETS_DIR = os.path.dirname(__file__)

def get_asset_path(filename):
    return os.path.join(ASSETS_DIR, filename)