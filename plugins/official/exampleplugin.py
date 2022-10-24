from hooks import hooks as _hooks
from terminal import Terminal
from plugins.commands import Commands

hooks    = _hooks()
commands = Commands()

class ExamplePlugin(object):
    def __init__(self):
        self.name = "Example Plugin"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Example plugin"
        self.hooks = {}

        print("Hello, world! from example plugin")
    
    def _on_load(self, terminal: Terminal) -> None:
        """
        This is called after all plugins are loaded
        this is where you will want to register commands
        """

        #To register a command, first you need to get the commands plugin
        commands: Commands = terminal.get_plugin('commands.py')
        #This variable can be given a type to make it easier to use but it is not required
        
        #Now you can register a command
        commands.register_command('!myFirstCommand', self.myFirstCommand, 'This is a command that will be registered')

        #But if you want a command to be able to access the terminal, you need to use the requestTerminalRefrence decorator
        commands.register_command('!mySecondCommand', self.mySecondCommand, 'This is a command that will be registered')

    @commands.requestTerminalRefrence
    def mySecondCommand(self, data: dict, terminal: Terminal) -> None:
        """
        This command will unload it's self after it is executed
        Note: Unloading is not a great way to disable a plugin, it's better to disable it and fully restart
        the terminal
        """
        terminal.get_plugin('pluginapi.py').unload_plugin('exampleplugin.py', terminal)

    def myFirstCommand(self, data: dict) -> None:
        """
        This is a command that will be registered
        the data parameter is a dictionary that contains most of the data you will need
        like the executed command
        """
        print("Hello, world! from myFirstCommand", data['command'])
    
EXPORTS = [ExamplePlugin()]