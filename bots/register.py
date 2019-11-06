__all__ = (
    'active_bots',
)


active_bots = {}


def add(name):
    def wrap(func):
        assert name.startswith('/')
        active_bots[name] = func
        return func
    return wrap
