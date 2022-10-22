import os, importlib
try:
    from termproject.hooks import hooks as _hooks
    from termproject.tabbyinput import Input
except ModuleNotFoundError:
    from hooks import hooks as _hooks
    from tabbyinput import Input

Hooks = _hooks()

class Terminal(object):
    def __init__(self):
        #Make a dictionary of hooks from the _hooks class
        self.hooks          = {f"builtin::{hook}":[] for hook in Hooks.__dict__}
        self.loaded_plugins = {}

        self.config = {'plugins_folder': 'termproject/plugins'}
        self.data   = {'debug_logs': []}

        self.input = Input()#Used for tab completion

        self.load_plugins()
    
    def call_hook(self, hook: str, data: dict) -> dict:
        if hook in self.hooks:
            for hook in self.hooks[hook]:
                hook: callable
                #Get the functio name
                if str(hook.__name__) == 'hookRequest_TerminalRefrence':
                    self.data['debug_logs'].append(f"[HookCaller::INFO] Hook {hook.__name__} is requesting terminal refrence")
                    data = hook(data, terminal=self)
                else: data = hook(data)
                
                if data is None:
                    print(f"[HookCaller::ERROR] Hook {hook} returned None")
        return data

    def load_plugin(self, plugin: str, spec):
        module = importlib.util.module_from_spec(spec)
        self.loaded_plugins[plugin] = module
        spec.loader.exec_module(module)

        #Plugin is now loaded, now we just gotta hook it into the terminal
        if not hasattr(self.loaded_plugins[plugin], 'EXPORTS'):
            print(f"[PluginLoader::ERROR] Plugin {plugin} has no EXPORTS")
            del self.loaded_plugins[plugin]

        for export in self.loaded_plugins[plugin].EXPORTS:
            if not hasattr(export, 'hooks'):
                continue
            for hook in export.hooks:
                self.data['debug_logs'].append(f"[PluginLoader::INFO] Hooking {export.name} to {hook}")
                if hook in self.hooks:
                    self.hooks[hook].append(export.hooks[hook])
                else:
                    print(f"[PluginLoader::ERROR] Plugin {export.name} is trying to hook to an invalid hook {hook}")

    def load_plugins(self) -> None:
        for plugin in os.listdir(self.config['plugins_folder']):
            if plugin.endswith('.py'):
                #Import the plugin from the file
                spec = importlib.util.spec_from_file_location(plugin, os.path.join(self.config['plugins_folder'], plugin))
                self.load_plugin(plugin, spec)


    def main(self, display_on_load: bool = False):
        if display_on_load: print("[Terminal::INFO] Terminal loaded")
        self.call_hook(Hooks.on_main, {})
        while not hasattr(self, 'stop'):
            if len(self.data['debug_logs']) > 100_000:
                self.data['debug_logs'] = self.data['debug_logs'][100:]
                
            prompt    = self.call_hook(Hooks.before_prompt, {'prompt': f'>>'})
            command   = self.input.get_input(prompt['prompt'])
            hook_resp = self.call_hook(Hooks.before_command, {'command': command})

            if 'abort' in hook_resp and hook_resp['abort']['value']:
                if hook_resp['abort']['callback'] is not None:
                    hook_resp['abort']['callback']()
                continue

            if hook_resp['command'].strip().startswith('cd'):
                try:
                    os.chdir(command.split(' ')[1])
                except IndexError:
                    print("cd: missing operand")
                except FileNotFoundError:
                    print("cd: no such file or directory")
                continue

            os.system(hook_resp['command'])
                
terminal = Terminal()
terminal.main()