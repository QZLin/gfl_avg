import enum


class Element:
    child = None
    name = None
    value = None
    intend = 0

    # def __init__(self, name, value, child, intend):
    #     self.name = name
    #     self.value = value
    #     self.child = child
    #     self.intend = intend


class Text(Element):
    def __init__(self, text, name=None):
        self.value = text
        self.arg0 = name


class Statement(Element):
    def __init__(self, names, value=None):
        self.name = names
        self.value = value


class Assign(Element):
    def __init__(self, name, type_, child):
        self.name = name
        self.type = type_
        if isinstance(child, Element):
            self.child = [child]
        else:
            self.child = child


class Block(Element):
    pass


class Func(Element):
    def __init__(self, name, child):
        self.name = name
        if isinstance(child, Element):
            self.child = [child]
        else:
            self.child = child


def raw_str(string):
    return f"'{string}'"


def ast2rpy(ast_map: list):
    if type(ast_map) == str:
        return raw_str(ast_map)
    if ast_map is None:
        return ''
    content = ''
    for e in ast_map:
        tp = type(e)
        if tp == str:
            return raw_str(e)
        intend = e.intend * ' '
        if tp == Statement:
            content += intend + f"{' '.join(e.name)} {e.value}\n"
        elif tp == Text:
            content += (f'{e.arg0} ' if e.arg0 else '') + intend + raw_str(e.value) + '\n'
        elif tp == Func:
            content += e.intend * ' ' + f"{e.name}({ast2rpy(e.child)})\n"
        elif tp == Assign:
            content += e.intend * ' ' + f"{e.type} {e.name} = {ast2rpy(e.child)}\n"

    return content
