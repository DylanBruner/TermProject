import os
from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu

"""
Work in progress currently fails to detect the virtual environment, and the auto prompting has false positives
"""


hooks = _hooks()

class AutoDetectVenv(object):
    def __init__(self):
        self.name = "Auto Detect Venv"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Automatically detect and prompt to activate it"
        self.hooks = {
            hooks.before_command: self.before_command,
            'termtheme::on_theme_path': self.on_theme_path
        }

        self.prompted_directories = []

    def checkInVenv(self) -> bool:
        #If venv is activated return it's name
        if 'VIRTUAL_ENV' in os.environ:
            return os.environ['VIRTUAL_ENV'].split(os.path.sep)[-1]
        return False
    
    def venvExists(self, path: str) -> bool:
        return os.path.exists(os.path.join(path, 'Scripts', 'activate.bat'))

    def on_theme_path(self, data: dict) -> dict:
        #Split at the drive letter
        inVenv = self.checkInVenv()
        if inVenv:
            before_path = data['prompt'].split(':')[0][:-1]
            before_path += f'[{inVenv}] '
            data['prompt'] = before_path + f"{data['prompt'].split(':')[0][-1]}:{data['prompt'].split(':')[1]}"
            return data

    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        if self.venvExists(os.getcwd()) and os.getcwd() not in self.prompted_directories:
            print("Found a virtual environment in this directory, would you like to activate it? (y/n)", end=' ')
            if input().lower() == 'y':
                os.system('Scripts\\activate.bat')
            self.prompted_directories.append(os.getcwd())

        return data

EXPORTS = [AutoDetectVenv()]