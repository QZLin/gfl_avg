from re import search, sub, match
from profiles import IMG

CHAR_DEF = 'define %s = Character("%s")'
SOUND_FX = 'play sound \'audio/%s\''
BGM = 'play music \'bgm/%s\''


# SHOW_BG = 'image %s = im.Scale(im.Crop("images/%s",(0,218,1024,578)),1280,720)\nscene %s\n'

def is_codename(name):
    if len(name) == 0:
        return False
    if name[0] != '_' or match('', name[0]) is None:
        return False
    if name in ['+', '-', '*', '/', '\\']:
        return False


def to_code(origin):
    illegal = [' ', '-', '.']
    for x in illegal:
        origin = origin.replace(x, '_')
    return origin


def show_bg(file_name, codename):
    return 'image %s = im.Scale(im.Crop("images/%s",(0,218,1024,578)),1280,720)\n' \
           'scene %s\n' % \
           (codename, file_name, codename)


def add_front(texts, sep_count=4, sep=' ', label=None):
    if label is not None:
        texts += 'return\n'
    string = sep * sep_count + ('\n' + sep * sep_count).join(texts.split('\n'))
    if label is not None:
        string = 'label %s:\n' % label + string
    return string


def render_chars(name_dict):
    return '\n'.join([CHAR_DEF % (name_dict[x], x) for x in name_dict.keys()])


debug_bgm = set()
debug_chars = set()


def render(source, label=None, names=None):
    avg_text = ''
    # debug
    if label is not None:
        avg_text += "'" + label + "'\n"

    if names is None:
        # names = set()
        names = {}

    lines = source.split('\n')
    if '' in lines:
        lines.remove('')
    for line in lines:
        # NPC-Kalin(1)<Speaker>格琳</Speaker>||:“选择我们，加入我们！格里芬私人军事承包商，更新世界的锋芒！”+没错，从今天开始，您就是格里芬旗下的战术指挥官啦！

        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]

        tag_head = head[head.find('||') + 2:]
        char_head = head[:head.find('||')]

        # BGM
        bgm_result = search(r'(?<=<BGM>).+?(?=</BGM>)', tag_head)
        if bgm_result is not None:
            bgm = bgm_result.group()
            debug_bgm.add(bgm)
            # avg_text += BGM % (bgm + '.wav') + '\n'

        # Sound FX
        sound_fx_result = search(r'(?<=<SE1>).+?(?=</SE1>)', tag_head)
        if sound_fx_result is not None:
            sound_fx = sound_fx_result.group()
            avg_text += SOUND_FX % (sound_fx + '.wav') + '\n'

        # Character
        # char_head = sub(r'<\S+?>.+?</\S+?>', '', head)
        img = r'\S+?\(\d+?\)'

        # Background
        bg_result = search(r'(?<=<BIN>).+?(?=</BIN>)', head)
        if bg_result is not None:
            bg_img = IMG[int(bg_result.group().replace(' ', ''))]
            bg_code_name = 'i_' + to_code(bg_img)
            # bg_render = SHOW_BG % (bg_code_name, bg_img + '.png', bg_code_name)
            avg_text += show_bg(bg_img + '.png', bg_code_name)

        # Name
        name_result = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
        name = name_result.group() if name_result is not None else None

        if name is not None:
            name = name.replace(' ', '')
            if name == '':
                name = None
            elif name not in names.keys():
                code_name = to_code(name)
                names[name] = code_name

        # text
        for text_unit in text.split('+'):
            if name is None:
                avg_text += '\'' + text_unit + '\'\n'
            elif text_unit != '':
                avg_text += "%s '%s'\n" % (names[name], text_unit)
            elif text_unit == '':
                avg_text += '\'\'\n'
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
    with open('rpy/script.rpy', 'w') as f:
        f.write('label start:\n')


    def render_level(chapter, lv, part):
        level = '%d-%d-%d' % (chapter, lv, part)
        with open('avgtxt_main/%s.bytes' % level, 'r', encoding='utf-8') as file:
            s = file.read()

        code_level = level.replace('-', '_')
        avg = render(s, label='s' + code_level)
        with open('rpy/%s.rpy' % code_level, 'w', encoding='utf-8') as file:
            file.write(avg)
        print(avg)
        with open('rpy/script.rpy', 'a+') as file:
            file.write('    call s' + code_level + '\n')


    for i in range(1, 13):
        for ii in range(1, 7):
            for iii in range(1, 3):
                render_level(i, ii, iii)

    with open('debug/bgm.txt', 'w') as f:
        f.write('\n'.join(debug_bgm))
# if __name__ == '__main__':
#     level = '1-4-1'
#     with open('avgtxt_main/%s.bytes' % level, 'r', encoding='utf-8') as file:
#         s = file.read()
#
#     avg = render(s, label='s' + level.replace('-', '_'))
#     with open('rpy/%s.rpy' % level.replace('-', '_'), 'w', encoding='utf-8') as file:
#         file.write(avg)
#     print(avg)
