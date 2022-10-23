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
        self.hooks = {
            hooks.before_command: self.before_command,
        }

        self.plugins = ['devutils', 'termtheme', 'moresuggestions', 'poke']

        print(f"[CorePackage] run '!installcore' to install")

    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        if data['command'].split(' ')[0].lower() == '!installcore':
            hooks.abort_action(data, lambda: None)
            print(f"[CorePackage] Installing core plugins")
            pluginStore: PluginStore = terminal.get_plugin('pluginstore.py')
            for plugin in pluginStore.manifest_cache['plugins']:
                if plugin['name'] in self.plugins:
                    pluginStore.installPluginFromUrl(plugin, terminal)
        
        try:    os.rename('termproject/plugins/corepackage.py', 'termproject/plugins/corepackage.py.dis')
        except: print("[CorePackage] Failed to disable self")
        return data
    
EXPORTS = [CorePackage()]