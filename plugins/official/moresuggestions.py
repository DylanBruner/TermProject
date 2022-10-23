from hooks import hooks as _hooks
from terminal import Terminal

hooks = _hooks()

class MoreSuggestions(object):
    def __init__(self):
        self.name = "MoreSuggestions"
        self.version = "0.1"
        self.author = "Dylan Bruner"
        self.description = "Better suggestions for the terminal"
        self.hooks = {
            hooks.before_prompt: self.before_prompt,
        }

        self.suggestions = [
            'python',
            '!plugins',
            '!reload',
            '!poke',
            '!help'
        ]

    @hooks.requestTerminalRefrence
    def before_prompt(self, data: dict, terminal: Terminal):
        """
        We use a hook because we need to modify the terminal 
        and this is the only way to get a reference to it
        """
        for suggestion in self.suggestions:
            if suggestion not in terminal.input.added_suggestions:
                terminal.input.added_suggestions.append(suggestion)
        return data
    
EXPORTS = [MoreSuggestions()]