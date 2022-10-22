class hooks(object):
    def __init__(self):
        self.on_load   = "builtin::on_load"
        self.on_main   = "builtin::on_main"

        self.before_prompt  = "builtin::before_prompt"
        self.before_command = "builtin::before_command"

    def register_hook(self, plugin_name: str, hook_name: str):
        """
        Registers a hook to the hooks class
        """
        #Clean up the hook name so it can be used as a variable name
        hook_name = hook_name.replace(' ', '_').replace('-', '_').lower()
        if not hasattr(self, hook_name):
            setattr(self, hook_name, hook_name)
            self.__dict__[hook_name] = []
        else:
            print(f"[Hooks::ERROR] Hook {hook_name} already exists")
        return hook_name

    def abort_action(self, data: dict, callback: callable = None) -> dict:
        """
        Attempts to abort the current action not always supported
        """
        data['abort'] = {
            'value': True,
            'callback': callback,
        }
        return data

    def cancel_abort(self, data: dict) -> dict:
        """
        Attempts to cancel the current abort action
        """
        data['abort'] = {
            'value': False,
            'callback': None,
        }
        return data

    def requestTerminalRefrence(self, func):
        def hookRequest_TerminalRefrence(*args, **kwargs):
            return func(*args, **kwargs)
        return hookRequest_TerminalRefrence