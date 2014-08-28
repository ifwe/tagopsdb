import model.meta.base as base
from .model import *

class LazySession(object):
    def __init__(self, module, attr):
        self.module = module
        self.attr = attr
    def __getattr__(self, attr):
        return getattr(getattr(self.module, self.attr), (attr))


Session = LazySession(base, 'Session')
