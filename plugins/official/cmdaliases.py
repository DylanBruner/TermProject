import json
from hooks import hooks as _hooks
from terminal import Terminal
from plugins.commands import Commands

hooks    = _hooks()
commands = Commands()

class CmdAliases(object):
    def __init__(self):
        self.name = "CmdAliases"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Allows you to create aliases for commands"
        self.hooks = {
            hooks.before_command: self.before_command
        }
    
    def _on_load(self, terminal: Terminal):
        commands: Commands = terminal.get_plugin('commands.py')
        commands.register_command('!alias', self.alias, 'Create an alias for a command')

    @commands.requestTerminalRefrence
    def alias(self, terminal: Terminal, data: dict):
        """
        Create an alias for a command
        """
        command = data['command'].split(' ')
        args    = command[1:]

        if len(args) < 2:
            print('Usage: alias <alias> <command>')
            return

        alias   = args[0]
        command = ' '.join(args[1:])

        with open(terminal.install_path+'/userconfig.json') as f:
            config = json.load(f)
            if 'aliases' not in config: config['aliases'] = {}

        config['aliases'][alias] = command
        with open(terminal.install_path+'/userconfig.json', 'w') as f:
            json.dump(config, f, indent=4)
    
    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to handle aliases
        """
        command = data['command'].split(' ')
        with open(terminal.install_path+'/userconfig.json') as f:
            config = json.load(f)
            if 'aliases' not in config: config['aliases'] = {}

        if command[0] in config['aliases']:
            data['command'] = config['aliases'][command[0]] + ' ' + ' '.join(command[1:])
            return data
        return data
        
    
EXPORTS = [CmdAliases()]