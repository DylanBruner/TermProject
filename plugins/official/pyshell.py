import os
from hooks import hooks as _hooks
from terminal import Terminal
from plugins.commands import Commands

hooks    = _hooks()
commands = Commands()

class PyShell(object):
    def __init__(self):
        self.name = "PyShell"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Drop into a python interpreter that has access to the terminal's variables"
        self.hooks = {
        }
    
    def _on_load(self, terminal: Terminal) -> None:
        commands: Commands = terminal.get_plugin('commands.py')
        commands.register_command('!pyshell', self.termpreter, 'Drop into a python interpreter that has access to the terminal\'s variables')
    
    def modifyVar(self, values: dict, newDefenition: tuple):
        values = values.copy()
        values[newDefenition[0]] = newDefenition[1]
        return values
    
    @commands.requestTerminalRefrence
    def termpreter(self, data: dict, terminal: Terminal):
        try:
            import code
            code.interact(local=self.modifyVar(locals(), ('clear', lambda: os.system('cls' if os.name == 'nt' else 'clear'))))
        except Exception as e:
            print(f"[ERROR] Failed to enter interpreter: {e}")

EXPORTS = [PyShell()]