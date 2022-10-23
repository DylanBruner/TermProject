import requests, importlib
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu
from search import Search

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

        self.manifest_cache = requests.get("https://raw.githubusercontent.com/DylanBruner/TermProject/master/plugins/manifest.json").json()

    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to register custom commands
        """
        if str(data['command']).strip().startswith('!pluginstore'):
            hooks.abort_action(data, lambda: self.pluginstore(terminal, data['command']))
        return data

    def installPluginFromUrl(self, plugin: dict, terminal: Terminal):
        print(f"Downloading {plugin['name']}...")
        data = requests.get(plugin['url']).text
        with open(f"termproject/plugins/{plugin['name']}.py", "w") as f:
            f.write(data)
        print(f"Downloaded {plugin['name']}, installing it into the terminal...")

        spec = importlib.util.spec_from_file_location(plugin['name'], f"termproject/plugins/{plugin['name']}.py")
        terminal.load_plugin(plugin['name'], spec)


    def pluginstore(self, terminal: Terminal, command: str):
        """
        Get plugins from github
        """
        print("Plugin Store v"+self.version)
        print("1. Search for plugins")
        print("2. Manage plugins")
        print("3. Exit")

        choice = input("Option: ")
        if choice == "1":
            self.search(terminal)

    def search(self, terminal: Terminal):
        selection   = Search([plugin['name'] for plugin in self.manifest_cache['plugins']]).search()
        try:
            plugin_data = [plugin for plugin in self.manifest_cache['plugins'] if plugin['name'] == selection][0]
        except Exception as e:
            print("Failed to find plugin", e)

        self.installPluginFromUrl(plugin_data, terminal)
        
EXPORTS = [PluginStore()]