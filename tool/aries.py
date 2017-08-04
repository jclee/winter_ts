#!/usr/bin/env python

def getChild(node, name):
    for child in node[1:]:
        if isinstance(child, list) and child[0] == name:
            return child
    return None

def parseDocument(content):
    toks = _tokens(content)
    if next(toks) != '(':
        raise Exception("expected opening paren at start of document")
    node = _parseNode(toks)
    try:
        next(toks)
        raise Exception("extra stuff after document closing paren")
    except StopIteration:
        pass
    return node

def _parseNode(tokens):
    tok = next(tokens)
    node = []
    while tok != ')':
        if tok == '(':
            node.append(_parseNode(tokens))
        else:
            node.append(tok)
        tok = next(tokens)
    return node

def _tokens(content):
    tok = []
    for ch in content:
        if ch in '()':
            if tok:
                yield ''.join(tok)
                tok = []
            yield ch
        elif ch in ' \t\n\r':
            if tok:
                yield ''.join(tok)
                tok = []
        else:
            tok.append(ch)
    if tok:
        yield ''.join(tok)
