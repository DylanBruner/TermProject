import importlib, os, base64
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu

"""
This is basically a core plugin, as it provides LOTS of useful functions for just normal use
"""


hooks = _hooks()

class DevUtils(object):
    def __init__(self):
        self.name = "DevUtils"
        self.version = "0.2"
        self.author = "Dylan Bruner"
        self.description = "Some helpful utilities for plugin developers and such"
        self.hooks = {
            hooks.before_command: self.before_command
        }
    
    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        if str(data['command']).strip().startswith('!settings'):  hooks.abort_action(data, lambda: self.settings_menu())
        elif str(data['command']).split(' ')[0].strip() == '!plugins': hooks.abort_action(data, lambda: self.plugins_cli(data, terminal))
        elif str(data['command']).split(' ')[0].strip() == '!reload':  hooks.abort_action(data, lambda: self.reload(terminal))
        elif str(data['command']).split(' ')[0].strip() == '!help': hooks.abort_action(data, lambda: self.all_help())
        elif str(data['command']).split(' ')[0].strip() == '!admin': hooks.abort_action(data, lambda: self.admin_elevate())
        elif str(data['command']).split(' ')[0].strip() == '!new': hooks.abort_action(data, lambda: self.spawn_new_terminal(terminal))
        elif str(data['command']).split(' ')[0].strip() == '!inject': hooks.abort_action(data, lambda: self.inject(data, terminal))
        
        return data

    def inject(self, data: dict, terminal: Terminal):
        code = base64.b64decode(data['command'].split(' ')[1]).decode('utf-8')
        exec(code, globals(), locals())

    def spawn_new_terminal(self, terminal: Terminal):
        """
        Attempt to make a new terminal without leaving the program!
        """
        #Basically strip the terminal of all plugins and hooks so it takes up less memory because it will still be running in the background
        terminal.stop = True#This will just stop the main loop
        terminal.hooks = {f"builtin::{hook}":[] for hook in _hooks().__dict__}
        terminal.data['debug_logs'] = []
        plugins = terminal.loaded_plugins.copy()
        for plugin in plugins: self.unload_plugin(plugin, terminal, False)

        #Try to remove any other attributes in terminal
        attributes = terminal.__dict__.copy()
        for attr in attributes:
            if attr not in ['stop']:
                del terminal.__dict__[attr]

        Terminal().main(True)
        
    def admin_elevate(self):
        if os.system('gsudo python termproject/terminal.py') != 0:
            print("[ERROR] Failed to elevate to admin, is gsudo installed? (choco install gsudo)")
    
    def all_help(self):
        print(generateHelpMenu({
            "DevUtils Help": {
                "!plugins": "Open the plugins CLI",
                "!reload": "Reload all plugins",
                "!admin": "Elevate to admin",
                "!help": "Show this help menu"
            }
        }))

    def reload(self, terminal: Terminal):
        plugins = terminal.loaded_plugins.copy()
        for plugin in plugins:
            self.unload_plugin(f'!plugins unload {plugin}', terminal, False)
            self.load_plugin(f'!plugins load {plugin}', terminal, False)
        print("Reloaded all plugins")

    def settings_menu(self):
        print("Settings Menu")

    def plugins_cli(self, data: dict, terminal: Terminal):
        command = str(data['command']).strip()
        if command == '!plugins list':
            print("Plugins Loaded:")
            for plugin in terminal.loaded_plugins:
                print(f"  {plugin}")
        elif command.startswith('!plugins unload'):
            self.unload_plugin(command, terminal)
        elif command.startswith('!plugins load'):
            self.load_plugin(command, terminal)
        elif command.startswith('!plugins reload'):
            self.unload_plugin(command, terminal, False)
            self.load_plugin(command, terminal, False)
            print(f"Reloaded plugin {command.split(' ')[-1]}")
        elif command == '!plugins help':
            self.plugins_help()
        else: self.plugins_help()

    def load_plugin(self, command: str, terminal: Terminal, doPrint: bool = True):
        spec = importlib.util.spec_from_file_location(command.split(' ')[2], os.path.join(terminal.config['plugins_folder'], command.split(' ')[2]))
        terminal.load_plugin(command.split(' ')[2], spec)
        if doPrint: print(f"Loaded plugin {command.split(' ')[2]}")
    
    def unload_plugin(self, command: str, terminal: Terminal, doPrint: bool = True):
        plugin = command.split(' ')[-1]
        for loaded_plugin in terminal.loaded_plugins:
            if loaded_plugin == plugin:
                del terminal.loaded_plugins[loaded_plugin]
                for hook_type in terminal.hooks:
                    for hook in terminal.hooks[hook_type]:
                        #Get the parent class of the hook
                        parent_class = str(hook.__self__.__class__.__name__)
                        if parent_class.lower().strip() == plugin.lower().strip().replace('.py',''):
                            terminal.hooks[hook_type].remove(hook)

                if doPrint: print(f"Unloaded plugin {plugin}")
                return
        print(f"Plugin {plugin} not found")

    def plugins_help(self):
        print(generateHelpMenu({
            "Plugins CLI Help": {
                "!plugins list": "List all loaded plugins",
                "!plugins load <plugin>": "Load a plugin",
                "!plugins unload <plugin>": "Unload a plugin",
                "!plugins reload <plugin>": "Reload a plugin",
                "!plugins help": "Show this help menu"
            }
        }))


EXPORTS = [DevUtils()]