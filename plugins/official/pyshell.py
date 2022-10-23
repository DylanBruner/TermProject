import os
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu

hooks = _hooks()

class PyShell(object):
    def __init__(self):
        self.name = "PyShell"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Drop into a python interpreter that has access to the terminal's variables"
        self.hooks = {
            hooks.before_command: self.before_command,
        }
    
    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        if data['command'].split(' ')[0].lower() == '!pyshell':
            hooks.abort_action(data, lambda: self.termpreter(terminal))
        return data

    def modifyVar(self, values: dict, newDefenition: tuple):
        values = values.copy()
        values[newDefenition[0]] = newDefenition[1]
        return values
    
    def termpreter(self, terminal: Terminal):
        try:
            import code
            code.interact(local=self.modifyVar(locals(), ('clear', lambda: os.system('cls' if os.name == 'nt' else 'clear'))))
        except Exception as e:
            print(f"[ERROR] Failed to enter interpreter: {e}")

EXPORTS = [PyShell()]