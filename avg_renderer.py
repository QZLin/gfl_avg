from re import search, sub
from profiles import IMG

CHAR_DEF = 'define %s = Character("%s")'
# SHOW_BG = 'scene %s'
SHOW_BG = 'image %s = im.Scale(im.Crop("images/%s",(0,218,1024,578)),1280,720)\nscene %s\n'


def add_front(texts, sep_count=4, sep=' ', label=None):
    # string = ''
    # for x in texts.split('\n'):
    #     string += sep * sep_count + x + '\n'
    # return string
    if label is not None:
        texts += 'return\n'
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
    try:
        lines.remove('')
    except ValueError:
        pass
    for line in lines:
        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]

        tag_head = head[head.find('||') + 2:]

        char_head = head[:head.find('||')]
        # char_head = sub(r'<\S+?>.+?</\S+?>', '', head)
        img = r'\S+?\(\d+?\)'

        bg_m = search(r'(?<=<BIN>).+?(?=</BIN>)', head)
        if bg_m is not None:
            bg_t = IMG[int(bg_m.group().replace(' ', ''))]
            bg_code_name = 'i_' + bg_t.replace('-', '_').replace('.', '_').replace(' ', '_')
            bg_code = SHOW_BG % (bg_code_name, bg_t + '.png', bg_code_name)
            avg_text += bg_code
            # avg_text += SHOW_BG % IMG[int(bg_m.group().replace(' ', ''))] + '\n'

        name_r = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
        name = name_r.group() if name_r is not None else None

        if name is not None and name != '':
            if name not in names.keys():
                code_name = name.replace('-', '_').replace(' ', '_')
                names[name] = code_name

            # names.add(name.group())
        # name = name.group() if name is not None else None

        for ltxt in text.split('+'):
            if name is None or name == '':
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
    with open('rpy/main.rpy', 'w') as f:
        pass
    for x in range(1, 13):
        for y in range(1, 7):
            for z in range(1, 3):
                level = '%d-%d-%d' % (x, y, z)
                with open('avgtxt_main/%s.bytes' % level, 'r', encoding='utf-8') as file:
                    s = file.read()

                avg = render(s, label='s' + level.replace('-', '_'))
                with open('rpy/%s.rpy' % level.replace('-', '_'), 'w', encoding='utf-8') as file:
                    file.write(avg)
                print(avg)
                with open('rpy/main.rpy', 'a+') as f:
                    f.write('    call s' + level.replace('-', '_') + '\n')
# if __name__ == '__main__':
#     level = '1-4-1'
#     with open('avgtxt_main/%s.bytes' % level, 'r', encoding='utf-8') as file:
#         s = file.read()
#
#     avg = render(s, label='s' + level.replace('-', '_'))
#     with open('rpy/%s.rpy' % level.replace('-', '_'), 'w', encoding='utf-8') as file:
#         file.write(avg)
#     print(avg)
