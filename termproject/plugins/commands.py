from hooks import hooks as _hooks
from terminal import Terminal

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
    
    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to register custom commands
        """
        if str(data['command']).strip().startswith('!'):
            hooks.abort_action(data, lambda: self.run_command(terminal, data['command']))
        return data
    
    def run_command(self, terminal: Terminal, command: str):
        """
        Run a command
        """
        command = command.strip()[1:]
        if command in self.commands:
            self.commands[command](terminal)
        else:
            print(f"Command {command} not found")

EXPORTS = [Commands()]