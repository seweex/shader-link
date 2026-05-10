
import json

from pathlib import Path

class Cacher:
    CACHE_FILENAME = "shader-link.cache.json"
    SRC_CODE_CHECKSUM_KEY = "source-code-checksum"

    def __init__(self, path : str):
        file = Path (path + '/' + self.CACHE_FILENAME)

        if file.is_file ():
            with open (file, 'r') as json_file:
                self.cache = json.load (json_file)
        else:
            self.cache = dict()

        self.path = str (file)

    def update (self, file, checksum : str):
        self.cache [file] = { self.SRC_CODE_CHECKSUM_KEY : checksum }

    def checksum (self, file):
        return self.cache.setdefault (file, dict ()).get (self.SRC_CODE_CHECKSUM_KEY)

    def save (self):
        with open (self.path, 'w') as file:
            json.dump (self.cache, file, indent=4)
