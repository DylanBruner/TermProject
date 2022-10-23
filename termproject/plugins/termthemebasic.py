import colorama, os, ctypes, sys, subprocess
from hooks import hooks as _hooks
from terminal import Terminal

hooks = _hooks()

blackCyan = f"{colorama.Back.BLACK}{colorama.Fore.CYAN}"

class TerminalTheme(object):
    def __init__(self):
        self.name = "TermTheme"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Some themeing functions for the terminal"
        self.hooks = {
            hooks.before_prompt: self.before_prompt
        }

    def isAdmin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def strip_styling(self, text: str) -> str:
        return text.replace(colorama.Fore.RESET, '').replace(colorama.Back.RESET, '').replace(colorama.Style.RESET_ALL, '')

    @hooks.requestTerminalRefrence
    def before_prompt(self, data: dict, terminal: Terminal) -> dict:
        data['prompt'] = f"{os.getcwd()}{colorama.Fore.GREEN}$ {colorama.Style.RESET_ALL}"

        return data

EXPORTS = [TerminalTheme()]