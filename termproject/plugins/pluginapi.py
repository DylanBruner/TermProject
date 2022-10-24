import importlib
from hooks import hooks as _hooks
from terminal import Terminal

hooks = _hooks()

class PluginApi(object):
    def __init__(self):
        self.name = "Plugin API"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Plugin API, provides useful functions for plugins"
        self.hooks = {}

    def load_plugin(self, plugin_file: str, terminal: Terminal) -> None:
        try:
            spec = importlib.util.spec_from_file_location(plugin_file, f"{terminal.install_path}/plugins/{plugin_file}")
            terminal.load_plugin(plugin_file.split('.')[0], spec)
        except Exception as e:
            pass

    def unload_plugin(self, plugin_name: str, terminal: Terminal) -> None:
        try:
            if '.py' not in plugin_name:
                plugin_name += '.py'
            for loaded_plugin in terminal.loaded_plugins:
                if loaded_plugin == plugin_name:
                    del terminal.loaded_plugins[loaded_plugin]
                    for hook_type in terminal.hooks:
                        for hook in terminal.hooks[hook_type]:
                            #Get the parent class of the hook
                            parent_class = str(hook.__self__.__class__.__name__)
                            if parent_class.lower().strip() == plugin_name.lower().strip().replace('.py',''):
                                terminal.hooks[hook_type].remove(hook)
                    return True
        except Exception as e:
            pass
        return False
    
EXPORTS = [PluginApi()]