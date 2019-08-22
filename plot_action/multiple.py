from iter_helper import DuplicateLast


def multiple(*arg, these=None):
    if these is not None:
        return DuplicateLast(*these)
    return DuplicateLast(*arg)


m = multiple
