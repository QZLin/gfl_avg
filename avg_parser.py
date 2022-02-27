import keyword
import re
from re import search, match

import patch
import tool.bgm_path_resolver
from profiles import IMG  # !!!Run profiles_gen.py once to generate profiles.py


def is_codename(name):  # TODO
    if len(name) == 0:
        return False
    if name[0] != '_' or match('', name[0]) is None:
        return False
    if name in ['+', '-', '*', '/', '\\']:
        return False


def to_codename(origin_name):
    name = re.sub(r'[\\ ~#%&*.{}/:;()<>?|"\-\[\]\']', "_", origin_name)
    if keyword.iskeyword(name) or name in dir(__builtins__):
        name = f'{name}_{abs(hash(origin_name))}'
    return name


def show_bg(file_name, codename):
    return f'image {codename} = "images/{file_name}"\n' \
           f'scene {codename}\n'
    # return f'image {codename} = im.Scale(im.Crop("images/{file_name}",(0,218,1024,578)),1280,720)\n' \
    #        f'scene {codename}\n'
    # if file_name[-4:] == '.png':
    #     file_name = file_name[:-4]
    # return f'scene {file_name}\n'


def add_indentation(texts, sep_count=4, sep=' ', label=None):
    if label is not None:
        texts += 'return\n'
    string = sep * sep_count + ('\n' + sep * sep_count).join(texts.split('\n'))
    if label is not None:
        string = 'label %s:\n' % label + string
    return string


def char_define(name_dict):
    # return '\n'.join([CHAR_DEF % (name_dict[x], x) for x in name_dict.keys()])
    return '\n'.join([f'define {name_dict[x]} = Character("{x}")' for x in name_dict.keys()]) + '\n'


debug_sound_fx = []
debug_bgm = []
debug_names = []
debug_chars = []


def set_append(value, list_: list):
    if value not in list_:
        list_.append(value)


def parser(source, label=None, names=None, debug=False):
    avg_text = 'stop sound\n'
    if label is not None and debug:
        avg_text += f"'{label.replace('s', '').replace('_', '-')}'\n"

    if names is None:
        names = {}

    lines = source.split('\n')
    if '' in lines:
        lines.remove('')

    for line in lines:
        # NPC-Kalin(1)<Speaker>格琳</Speaker>||:“选择我们，加入我们！格里芬私人军事承包商，更新世界的锋芒！”+没错，从今天开始，您就是格里芬旗下的战术指挥官啦！

        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]

        tag_head = head[head.find('||') + 2:]

        tags = {x.groups()[0]: x.group() for x in re.finditer('<(\\S+?)>.+?</\\1>', head)}
        # BGM
        if 'BGM' in tags.keys():
            bgm = search(r'(?<=<BGM>).+?(?=</BGM>)', tags['BGM']).group()
            bgm = patch.bgm_patcher(bgm)
            if (path := tool.bgm_path_resolver.pl.fpath(bgm + '.wav')) is None:
                path = 'musiclost.flac'
                set_append(f'LOST: {bgm}', debug_bgm)
            else:
                path = path.replace('\\', '/')
                set_append(path, debug_bgm)
            avg_text += f'play music \'{path}\'\n'

        # Sound FX
        if 'SE1' in tags.keys():
            sound_fx = search(r'(?<=<SE1>).+?(?=</SE1>)', tags['SE1']).group()
            avg_text += f"play sound 'audio/{sound_fx}.wav'\n"
            set_append(sound_fx, debug_sound_fx)

        # Character # TODO
        char_head = head[:head.find('||')]
        char_head = re.sub('<(\\S+?)>.+?</\\1>', '', char_head)
        char_head = re.sub('<\\S+?>', '', char_head)
        char_list = [x.strip() for x in char_head.split(';')]
        chars = {}
        for x in char_list:
            if re.match('\\(\\S*\\)', x):
                continue
            r = re.search('(.*?)\\((\\d*?)\\)', x)
            chars[r.groups()[0]] = r.groups()[1]
        for char in char_list:
            set_append(char, debug_chars)
        # img = r'\S+?\(\d+?\)'

        # Background
        if 'BIN' in tags.keys():
            bg_result = search(r'(?<=<BIN>).+?(?=</BIN>)', tags['BIN'])
            bg_img = IMG[int(bg_result.group().replace(' ', ''))]
            bg_code_name = f'i_{to_codename(bg_img)}'
            # bg_render = SHOW_BG % (bg_code_name, bg_img + '.png', bg_code_name)
            avg_text += show_bg(bg_img + '.png', bg_code_name)

        # Name
        # name_result = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
        # name = name_result.group() if name_result is not None else None
        if 'Speaker' in tags.keys():
            name_result = tags['Speaker']
            name = search(r'<Speaker>(.*)</Speaker>', name_result).groups()[0]
            name = name.replace(' ', '')
            if name == '':
                name = None
            elif name not in names.keys():
                code_name = to_codename(name)
                names[name] = code_name
                set_append(name, debug_names)
        else:
            name = None

        # Convert color tag
        if re.search('<(color)=#\\S+?>(.*?)</\\1>', text):
            for r in re.finditer('<color=#(\\S+?)>', text):
                text = text.replace(r.group(), f'{{color=#{r.groups()[0]}}}')
            text = text.replace('</color>', '{/color}')

        # Text
        last_chars = ''
        for text_unit in text.split('+'):
            if len(chars.keys()) != 0:
                current_chars = ';'.join([f'{k}:{chars[k]}' for k in chars.keys()])
                if current_chars != last_chars:
                    for char in chars:
                        avg_text += f'show {to_codename(char)}_{chars[char]}\n'
                    last_chars = current_chars
            else:
                last_chars = ''
            if name is None:
                avg_text += f"'{text_unit}'\n"
                avg_text += f"play sound '{tool.bgm_path_resolver.UI_ObjDown}'\n"
            elif text_unit != '':
                avg_text += f"{names[name]} '{text_unit}'\n"
                avg_text += f"play sound '{tool.bgm_path_resolver.UI_ObjDown}'\n"
            elif text_unit == '':
                avg_text += "''\n"
    return char_define(names) + '\n' + add_indentation(avg_text, label=label)


if __name__ == '__main__':
    # import time
    # t = time.time()
    with open('rpy/script.rpy', 'w') as f:
        f.write('label start:\n')


    def generate_avg_level(chapter, level, part):
        file_name = f'{chapter}-{level}-{part}'
        with open(f'avgtxt_main/{file_name}.bytes', 'r', encoding='utf-8') as file:
            s = file.read()

        label_name = 's' + file_name.replace('-', '_')
        avg = parser(s, label=label_name, debug=True)
        with open(f'rpy/{label_name}.rpy', 'w', encoding='utf-8') as file:
            file.write(avg)
        print(avg)
        with open('rpy/script.rpy', 'a+') as file:
            file.write(' ' * 4 + f'call {label_name}\n')


    # Chapter 1~12, level 1~6, part 1~2
    i, ii, iii = 1, 1, 1
    while True:
        generate_avg_level(i, ii, iii)
        if (iii := iii + 1) > 2:
            iii = 1
            if (ii := ii + 1) > 6:
                ii = 1
                if (i := i + 1) > 12:
                    break

    # Write debug info
    with open('debug/bgm.txt', 'w') as f:
        f.write('\n'.join(debug_bgm))
    with open('debug/sound_fx.txt', 'w') as f:
        f.write('\n'.join(debug_sound_fx))
    with open('debug/names.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_names))
    with open('debug/chars.txt', 'w', encoding='utf-8') as f:
        f.write('\n'.join(debug_chars))
    # print(time.time() - t)
