
bots = {}


def register(name):
    def wrap(func):
        assert name.startswith('/')
        bots[name] = func
        return func
    return wrap


async def notify_bots(message):
    try:
        name, message = message.split(' ', maxsplit=2)
        await bots[name](message)
    except (ValueError, KeyError):
        pass


@register('/stock')
async def stock_bot(message):
    # TODO: Implement this bot
    pass
