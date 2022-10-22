from hooks import hooks as _hooks
from terminal import Terminal

hooks = _hooks()

class MoreSuggestions(object):
    def __init__(self):
        self.name = "Example Plugin"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Example plugin"
        self.hooks = {}

        print("Hello, world!")
    
EXPORTS = [MoreSuggestions()]