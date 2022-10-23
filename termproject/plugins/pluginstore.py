import requests
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu

hooks = _hooks()

class PluginStore(object):
    def __init__(self):
        self.name = "Plugin Store"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Get plugins from github"
        self.hooks = {
            hooks.before_command: self.before_command,
        }

        self.manifest_cache = requests.get()

    def searchForPlugin(self, q: str) -> list:
        pass

    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to register custom commands
        """
        if str(data['command']).strip().startswith('!pluginstore'):
            hooks.abort_action(data, lambda: self.pluginstore(terminal, data['command']))
        return data
    
    def pluginstore(self, terminal: Terminal, command: str):
        """
        Get plugins from github
        """
        print("Plugin Store v"+self.version)
        print("1. Search for plugins")
        print("2. Manage plugins")
        print("3. Exit")

EXPORTS = [PluginStore()]