# TODO: Hook up to browser local cache

_CONTENT = {}

_READ_HANDLES = {}
_WRITE_HANDLES = {}

class _ReadHandle(object):
    def __init__(self, path):
        self.path = path

class _WriteHandle(object):
    def __init__(self, path):
        self.path = path
        self.content = []

    def write(self, s):
        self.content.append(s)

def open(path, mode):
    if path in _WRITE_HANDLES or path in _READ_HANDLES:
        raise IOError("Simultaneous file access not supported")
    if mode == 'rt':
        if path not in _CONTENT:
            raise IOError("File does not exist")
        handle = _ReadHandle(path)
        _READ_HANDLES[path] = handle
        return handle
    elif mode == 'wt':
        handle = _WriteHandle(path)
        _WRITE_HANDLES[path] = handle
        return handle
    else:
        raise IOError("Unsupported access mode: " + repr(mode))
