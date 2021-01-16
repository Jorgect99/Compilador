
class Nodo:
    def __init__(self, lexema=None, token=None, renglon=None):
        self.sig = None
        self.lexema = lexema
        self.token = token
        self.renglon = renglon

    def __repr__(self):
        return self.lexema