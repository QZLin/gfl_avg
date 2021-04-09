from re import search, sub
from profiles import IMG

CHAR_DEF = 'define %s = Character("%s")'
SHOW_BG = 'scene %s'


def add_front(texts, sep_count=4, sep=' ', label=None):
    # string = ''
    # for x in texts.split('\n'):
    #     string += sep * sep_count + x + '\n'
    # return string
    string = sep * sep_count + ('\n' + sep * sep_count).join(texts.split('\n'))
    if label is not None:
        string = 'label %s:\n' % label + string
    return string


# def render_chars(name_set):
#     return '\n'.join([CHAR_DEF % (x, x) for x in name_set])

def render_chars(name_dict):
    return '\n'.join([CHAR_DEF % (name_dict[x], x) for x in name_dict.keys()])


def render(source, label=None, names=None):
    avg_text = ''

    if names is None:
        # names = set()
        names = {}

    lines = source.split('\n')
    lines.remove('')
    for line in lines:
        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]

        img_head = sub(r'<\S+?>.+?</\S+?>', '', head)
        img = r'\S+?\(\d+?\)'

        bg_m = search(r'(?<=<BIN>).+?(?=</BIN>)', head)
        if bg_m is not None:
            avg_text += SHOW_BG % IMG[int(bg_m.group().replace(' ', ''))] + '\n'

        name_r = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
        name = name_r.group() if name_r is not None else None

        if name is not None:
            if name not in names.keys():
                code_name = name.replace('-', '_').replace(' ', '_')
                names[name] = code_name

            # names.add(name.group())
        # name = name.group() if name is not None else None

        for ltxt in text.split('+'):
            if name is None:
                avg_text += "'%s'\n" % ltxt
            elif ltxt != '':
                avg_text += "%s '%s'\n" % (names[name], ltxt)
    return render_chars(names) + '\n' + add_front(avg_text, label=label)


# class Renderer:
#     def __init__(self, source=''):
#         self.source = source
#
#     def set_source(self, source):
#         self.source = source
#
#     def render(self):
#         pass
#
#
if __name__ == '__main__':
    with open('avgtxt_main/1-2-2.bytes', 'r', encoding='utf-8') as file:
        s = file.read()

    print(render(s, label='start'))
