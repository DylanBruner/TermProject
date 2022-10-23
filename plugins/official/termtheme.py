import colorama, os, ctypes, subprocess
from hooks import hooks as _hooks

hooks = _hooks()

chars = {
    'semiCircleLeft': '\ue0b6',
    'forwardArrow': '\ue0b0'
}
blackCyan = f"{colorama.Back.BLACK}{colorama.Fore.CYAN}"

class TerminalTheme(object):
    def __init__(self):
        self.name = "TermTheme"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Some themeing functions for the terminal"
        self.hooks = {
            hooks.before_prompt: self.before_prompt,
            hooks.before_command: self.before_command
        }

    def isAdmin(self) -> bool:
        try:
            return ctypes.windll.shell32.IsUserAnAdmin()
        except:
            return False

    def strip_styling(self, text: str) -> str:
        return text.replace(colorama.Fore.RESET, '').replace(colorama.Back.RESET, '').replace(colorama.Style.RESET_ALL, '')

    def before_prompt(self, data: dict):
        data['prompt'] = f"{blackCyan}{chars['semiCircleLeft']}{colorama.Back.CYAN}{colorama.Fore.BLACK}"
        if self.isAdmin():
            data['prompt'] += f"{colorama.Style.DIM}{colorama.Fore.MAGENTA}(Admin){colorama.Fore.BLACK}{colorama.Style.NORMAL} "
        data['prompt'] += os.getcwd()+f"{colorama.Back.RESET}{colorama.Fore.RESET}"
        data['prompt'] += f'{colorama.Back.BLACK}{colorama.Fore.CYAN}{chars["forwardArrow"]}{colorama.Fore.RESET}{colorama.Back.RESET}'

        return data
    
    def before_command(self, data: dict) -> dict:
        if data['command'].startswith('ls'):
            hooks.abort_action(data, lambda: self.better_listdir(data))
        return data
    
    def better_listdir(self, data: dict):
        proc = subprocess.Popen(data['command'], shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.PIPE)
        stdout, stderr = proc.communicate()
        stdout = stdout.decode('utf-8')
        stderr = stderr.decode('utf-8')
        if stderr:
            print(stderr)
        else:
            for file in stdout.split('\n'):
                if os.path.isdir(file):
                    print(f"{colorama.Fore.CYAN}{file}{colorama.Fore.RESET}")
                elif os.path.isfile(file):
                    print(f"{colorama.Fore.GREEN}{file}{colorama.Fore.RESET}")
                else:
                    print(f"{colorama.Fore.RED}{file}{colorama.Fore.RESET}")

EXPORTS = [TerminalTheme()]