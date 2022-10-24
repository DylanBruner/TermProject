import json

class Config(object):
    def __init__(self, config_file: str):
        self.config_file = config_file
        self.config      = {}

        with open(self.config_file, 'r') as f:
            self.config = json.load(f)

    def __getitem__(self, key):
        with open(self.config_file, 'r') as f:
            self.config = json.load(f)
        return self.config[key]