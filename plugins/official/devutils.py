import importlib, os, base64, colorama, requests, shutil
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu
from plugins.commands import Commands
from plugins.pluginstore import PluginStore
"""
This is basically a core plugin, as it provides LOTS of useful functions for just normal use
"""


hooks    = _hooks()
commands = Commands()

class DevUtils(object):
    def __init__(self):
        self.name = "DevUtils"
        self.version = "0.2"
        self.author = "Dylan Bruner"
        self.description = "Some helpful utilities for plugin developers and such"
        self.hooks = {
        }

    def _on_load(self, terminal: Terminal):
        commands: Commands = terminal.get_plugin('commands.py')
        commands.register_command('!inject', self.inject, "Inject code into the terminal")
        commands.register_command('!plugins', self.plugins_cli, "Open the plugins CLI")
        commands.register_command('!reload', self.reload, "Reload all plugins")
        commands.register_command('!admin', self.admin_elevate, "Elevate to admin")
        commands.register_command('!update', self.update, "Update the terminal")

    @commands.requestTerminalRefrence
    def update(self, data: str, terminal: Terminal):
        print(('='*10)+'[Updating Plugins]'+('='*10))
        plugin_store: PluginStore = terminal.get_plugin('pluginstore.py')
        plugin_names = [plugin_name['name'] for plugin_name in plugin_store.manifest_cache['plugins'] if plugin_name != '']
        
        for plugin in terminal.loaded_plugins.copy().keys():
            if plugin.split('.py')[0] in plugin_names:
                for plugin_data in plugin_store.manifest_cache['plugins']:
                    if plugin_data['name'] == plugin.split('.py')[0]:
                        try:
                            #plugin_store.installPluginFromUrl(plugin_data, terminal, False)
                            print(f"{colorama.Fore.GREEN}Updated {plugin_data['name']}{colorama.Fore.RESET}")
                        except Exception as e:
                            print(f"{colorama.Fore.RED}Failed to update {plugin_data['name']}: {e}{colorama.Fore.RESET}")
        self.reload(data, terminal, False)

        print(('='*10)+'[Updating Core]'+('='*10))
        if not os.path.exists(terminal.install_path+'/tmp'):
            os.mkdir(terminal.install_path+'/tmp')
            print('Downloading update...')
            r = requests.get('https://github.com/DylanBruner/TermProject/archive/refs/heads/master.zip')
            with open(terminal.install_path+'/tmp/update.zip', 'wb') as f:
                f.write(r.content)
            print('Extracting update...')
            shutil.unpack_archive(terminal.install_path+'/tmp/update.zip', terminal.install_path+'/tmp')
            print('Copying files...')
            for file in os.listdir(terminal.install_path+'/tmp/TermProject-master/termproject/plugins'):
                shutil.copyfile(terminal.install_path+'/tmp/TermProject-master/termproject/plugins/'+file, terminal.install_path+'/termproject/plugins/'+file)
            #Copy all .py files in tmp/TermProject-master/termproject to termproject
            for file in os.listdir(terminal.install_path+'/tmp/TermProject-master/termproject'):
                if file.endswith('.py'):
                    shutil.copyfile(terminal.install_path+'/tmp/TermProject-master/termproject/'+file, terminal.install_path+'/termproject/'+file)
            print("Cleaning up...")
            shutil.rmtree(terminal.install_path+'/tmp')
            print("Update complete!")

    @commands.requestTerminalRefrence
    def inject(self, data: dict, terminal: Terminal):
        code = base64.b64decode(data['command'].split(' ')[1]).decode('utf-8')
        exec(code, globals(), locals())

    @commands.requestTerminalRefrence
    def admin_elevate(self, data: dict, terminal: Terminal):
        if os.system(f'gsudo python "{terminal.install_path}/terminal.py"') != 0:
            print("[ERROR] Failed to elevate to admin, is gsudo installed? (choco install gsudo)")
    
    @commands.requestTerminalRefrence
    def reload(self, data: dict, terminal: Terminal, do_print: bool = True):
        for hook in terminal.hooks: terminal.hooks[hook] = []
        terminal.get_plugin('commands.py').commands = {}
        plugins = terminal.loaded_plugins.copy()
        for plugin in plugins:
            self.unload_plugin(f'!plugins unload {plugin}', terminal, False)
        terminal.load_plugins()
        if do_print: print("Reloaded all plugins")

    @commands.requestTerminalRefrence
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