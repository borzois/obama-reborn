import json
from pathlib import Path


class Repository:
    def __init__(self):
        self.__keys = {}

        self.mod_path = Path(__file__).parent
        keys_filename = 'keys.json'
        keys_file_path = (self.mod_path / keys_filename).resolve()
        with open(keys_file_path, 'r') as key_file:
            self.__keys.update(json.load(key_file))

    def get_token(self):
        return self.__keys['token']

    def get_admins(self):
        return self.__keys['admins']

    def get_llkey(self):
        return self.__keys['llkey']
