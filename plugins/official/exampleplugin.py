from hooks import hooks as _hooks
from terminal import Terminal

hooks = _hooks()

class ExamplePlugin(object):
    def __init__(self):
        self.name = "Example Plugin"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Example plugin"
        self.hooks = {}

        print("Hello, world! from example plugin")
    
EXPORTS = [ExamplePlugin()]