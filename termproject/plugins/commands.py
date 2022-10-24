from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu
hooks = _hooks()

class Commands(object):
    def __init__(self):
        self.name = "Commands"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Register commands"
        self.hooks = {
            hooks.before_command: self.before_command,
        }
        self.commands = {}

    def requestTerminalRefrence(self, func):
        def commandsRequest_TerminalRefrence(*args, **kwargs):
            return func(*args, **kwargs)
        return commandsRequest_TerminalRefrence

    def register_command(self, command: str, function, description: str):
        """
        Register a command
        """
        self.commands[command] = {
            'function': function,
            'description': description
        }

    def help(self):
        """
        Show help
        """
        menu = {"Commands": {}}
        for command in self.commands:
            menu['Commands'][command] = self.commands[command]['description']
        print(generateHelpMenu(menu))
    
    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to register custom commands
        """
        if str(data['command']).strip().startswith('!'):
            hooks.abort_action(data, lambda: self.run_command(terminal, data))
        return data
    
    def run_command(self, terminal: Terminal, data: dict):
        """
        Run a command
        """
        command = str(data['command']).strip().split(' ')[0]
        if command == '!help':
            self.help()
            return
        if command in self.commands:
            if self.commands[command]['function'].__name__ == 'commandsRequest_TerminalRefrence':
                self.commands[command]['function'](data=data, terminal=terminal)
            else: self.commands[command]['function'](data=data)
        else:
            print(f"Command {command} not found")

EXPORTS = [Commands()]