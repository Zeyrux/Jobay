class SocketIOBlueprint:

    funcs = []

    def add(self, func, *args, **kwargs):
        self.funcs.append((func, args, kwargs))

    def add_funcs_to_socket(self, socket):
        for func, args, kwargs in self.funcs:
            @socket(*args, **kwargs)
            func
        