INTEND_TYPE = ' '
INTEND_COUNT = 4


class Element:
    name = None
    value = None
    type = None
    child = None
    arg0 = None
    arg1 = None
    indent = 0


class Str(Element):
    def __init__(self, value):
        self.value = value if value is not None else ''

    def __str__(self):
        return raw_str(self.value)


class Text(Element):
    def __init__(self, text, name=None):
        self.value = text
        self.arg0 = name


def stmt(*e):
    return ' '.join([str(x) for x in e if x is not None])


class Statement(Element):
    def __init__(self, names, value=None):
        self.name = names
        self.value = value


class Assign(Element):
    def __init__(self, name, type_, child):
        self.name = name
        self.type = type_
        self.child = [child] if isinstance(child, Element) else child


class Block(Element):
    def __init__(self, type_, name, child, indent=0):
        self.type = type_
        self.name = name
        self.child = child
        self.intend = indent


class Func(Element):
    def __init__(self, name, child):
        self.name = name
        self.child = [child] if isinstance(child, Element) else child


def raw_str(string):
    return f"'{string}'"


def idt(level):
    """
    Spawn indent
    :param level:
    :return:
    """
    if level is None:
        return ''
    return INTEND_TYPE * INTEND_COUNT * level


def ast2rpy(ast_map):
    """
    Normal AST parser
    :param ast_map:
    :return:
    """
    if type(ast_map) == Block:
        return rpy_block(ast_map)
    else:
        return '\n'.join(_ast2rpy(x) for x in ast_map)


def rpy_block(block):
    """
    Block parser
    :param block:
    :return:
    """
    rpy_script = ''
    rpy_script += f'{idt(block.indent)}{block.type} {block.name}:\n'
    if block.child is not None:
        for x in block.child:
            x.indent += 1
    rpy_script += ast2rpy(block.child)
    return rpy_script


def _ast2rpy(ast_map: list):
    """
    AST parser for non newline elements
    :param ast_map:
    :return:
    """
    if isinstance(ast_map, Element):
        ast_map = [ast_map]
    elif ast_map is None:
        return ''
    elif type(ast_map) == str:
        return raw_str(ast_map)
    rpy_script = ''
    for e in ast_map:
        tp = type(e)
        if tp == Statement:
            rpy_script += stmt(f"{idt(e.indent)}{' '.join(e.name)}", e.value)
            # rpy_script += f"{idt(e.indent)}{' '.join(e.name)}" + (f' {e.value}' if e.value else '')
        elif tp == Str:
            rpy_script += Str.value
        elif tp == Block:
            if e.child:
                rpy_script += rpy_block(e)
        elif tp == Text:
            rpy_script += idt(e.indent) + stmt(e.arg0, raw_str(e.value))
        elif tp == Func:
            rpy_script += f"{idt(e.indent)}{e.name}({_ast2rpy(e.child)})"
        elif tp == Assign:
            rpy_script += f"{idt(e.indent)}{e.type} {e.name} = {_ast2rpy(e.child)}"

    return rpy_script
