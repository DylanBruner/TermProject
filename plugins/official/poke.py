from hooks import hooks as _hooks
from terminal import Terminal
from utilites import generateHelpMenu

hooks = _hooks()

class Poke(object):
    def __init__(self):
        self.name = "Poke"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Allow for modifying the terminal's variables on the fly"
        self.hooks = {
            hooks.before_command: self.before_command,
        }

    @hooks.requestTerminalRefrence
    def before_command(self, data: dict, terminal: Terminal):
        """
        Used to register custom commands
        """
        if str(data['command']).strip().startswith('!poke'):
            hooks.abort_action(data, lambda: self.poke(terminal, data['command']))
        return data

    def help_menu(self):
        print(generateHelpMenu({
            "Poke Help": {
                "!poke get <variable>": "Get a variable",
                "!poke list": "List all variables",
                "!poke set <variable> <value>": "Set a variable",
                "!poke execute <code>": "Execute code",
                "!poke help": "Show this help menu"
            }
        }))

    def poke(self, terminal: Terminal, command: str):
        """
        Used to poke the terminal's variables
        """
        try:
            if command.startswith('!poke get'):
                if command.split(' ')[2] in terminal.__dict__:
                    print(f"{command.split(' ')[2]} = {terminal.__dict__[command.split(' ')[2]]}")
                else:
                    print(f"Variable {command.split(' ')[2]} does not exist")
            elif command.startswith('!poke list'):
                for attr in terminal.__dict__:
                    print(f"{attr} = {terminal.__dict__[attr]}",end="\n\n")
            elif command.startswith('!poke set'):
                terminal.__dict__[command.split(' ')[2]] = eval(command.split(' ')[3])
                print(f"Set {command.split(' ')[2]} to {eval(command.split(' ')[3])}")
            elif command.startswith('!poke execute'):
                exec(command.split(' ', 2)[2])
            elif command.startswith('!poke help'):
                self.help_menu()
            else: self.help_menu()
        except Exception as e:
            print(f"[Poke::Error] Failed to poke, {e}")

    
EXPORTS = [Poke()]