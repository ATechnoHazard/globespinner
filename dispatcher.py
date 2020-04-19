class Dispatcher(object):
    handlers = {}

    def add_handler(self, handler_str, handler_func):
        self.handlers[handler_str] = handler_func

    def dispatch(self, command, args, bot, message):
        if command in self.handlers:
            self.handlers[command](bot, message, args)
        else:
            pass
