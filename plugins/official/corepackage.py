import os
from hooks import hooks as _hooks
from terminal import Terminal
try:
    from plugins.pluginstore import PluginStore
except: pass

hooks = _hooks()

class CorePackage(object):
    def __init__(self):
        self.name = "Core Package"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Install the most commonly used plugins with one command"
        self.hooks = {}

        self.plugins = ['devutils', 'termtheme', 'moresuggestions', 'poke']

    def _on_load(self, terminal: Terminal):
        print(f"[CorePackage] Installing core plugins")
        pluginStore: PluginStore = terminal.get_plugin('pluginstore.py')
        for plugin in pluginStore.manifest_cache['plugins']:
            if plugin['name'] in self.plugins:
                pluginStore.installPluginFromUrl(plugin, terminal)
    

        terminal.get_plugin('pluginapi.py').unload_plugin('corepackage.py', terminal)
        try:    os.remove(f'{terminal.install_path}/plugins/corepackage.py')
        except: print("[CorePackage] Failed to disable self")
    
EXPORTS = [CorePackage()]