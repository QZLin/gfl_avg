import keyword
import re
from re import search, match

import patch
import tool.bgm_path_resolver
from profiles import IMG  # !!!Run profiles_gen.py once to generate profiles.py
import ast_rpy as ast


def is_codename(name):  # TODO
    if len(name) == 0:
        return False
    if name[0] != '_' or match('', name[0]) is None:
        return False
    if name in ['+', '-', '*', '/', '\\']:
        return False


codename_map = str.maketrans(m := r'\\ ~#%&*.{}/:;()<>?|"\-\[\]\'', '_' * len(m))


def to_codename(origin_name: str):
    if origin_name.isspace():
        origin_name = f'SPACE_{origin_name.count(" ")}'
    # name = re.sub(r'[\\ ~#%&*.{}/:;()<>?|"\-\[\]\']', "_", origin_name)
    name = origin_name.translate(codename_map)
    if keyword.iskeyword(name) or name in dir(__builtins__):
        name = f'{name}_{str(hash(origin_name)).replace("-", "_")}'
    return name


debug_sound_fx = []
debug_bgm = []
debug_names = []
debug_chars = []


def s_apd(value, list_: list):
    """
    Append value to list when not exist
    :param value:
    :param list_:
    :return:
    """
    if value not in list_:
        list_.append(value)


def parser(source, label=None, names=None, debug_mode=False):
    lines = source.splitlines()
    if '' in lines:
        lines.remove('')
    if names is None:
        names = {}
    speaker_status = {}

    ast_map = [ast.Statement(['stop', 'sound'])]
    ast_top = []
    for line in lines:
        # NPC-Kalin(1)<Speaker>格琳</Speaker>||:“选择我们，加入我们！格里芬私人军事承包商，更新世界的锋芒！”+没错，从今天开始，您就是格里芬旗下的战术指挥官啦！
        name = None

        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]
        tag_head = head[head.find('||') + 2:]
        # Parse All tag by regex match
        full_tags = re.finditer('<(\\S+?)>(.+?)</\\1>', head)
        half_head = re.sub('<(\\S+?)>(.+?)</\\1>', "", head)
        half_tags = re.finditer('<(\\S+?)>', half_head)

        tags = [{'key': x.groups()[0], 'value': x.groups()[1], 'close': True} for x in full_tags]
        tags.extend([{'key': x.groups()[0], 'value': None, 'close': False} for x in half_tags])

        for tag in tags:
            speakers = []
            match tag['key']:
                case 'BGM':
                    bgm = patch.bgm_patcher(tag['value'])
                    if (path := tool.bgm_path_resolver.pl.fpath(bgm + '.wav')) is None:
                        path = 'musiclost.flac'
                        s_apd(f'LOST: {bgm}', debug_bgm)
                    else:
                        path = path.replace('\\', '/')
                        s_apd(path, debug_bgm)
                    ast_map.append(ast.Statement(['play', 'music'], ast.Str(path)))
                case 'SE1', 'SE2':
                    sound_fx = tag['value']
                    s_apd(sound_fx, debug_sound_fx)
                    path = f'audio/{sound_fx}.wav'
                    ast_map.append(ast.Statement(['play', 'sound'], ast.Str(path)))
                case 'BIN':
                    bg_result = tag['value']
                    bg_img = IMG[int(bg_result.replace(' ', ''))]
                    bg_code_name = f'i_{to_codename(bg_img)}'

                    ast_map.append(ast.Assign(f'i_{to_codename(bg_img)}', 'image', f'images/{bg_img}.png'))
                    ast_map.append(ast.Statement(['scene'], bg_code_name))
                case 'Speaker':
                    name = tag['value']
                    if name.isspace():
                        name = None
                    elif name is None:
                        pass
                    elif name not in names.keys():
                        code_name = to_codename(name)
                        names[name] = code_name
                        s_apd(name, debug_names)
                        speakers.append(code_name)
                        ast_top.append(ast.Assign(code_name, 'define', ast.Func('Character', name)))
                # TODO
                case '通讯框':
                    pass
                case 'Grey':
                    pass
                case 'Shake':
                    pass
                case 'Position':
                    pass
                case '回忆':
                    pass
                case '关闭蒙版':
                    pass
                case '名单', '名单2':
                    pass

        # TODO Character Portrait

        # Convert color tag
        for r in re.finditer('<color=#(\\S+?)>', text):
            text = text.replace(r.group(), f'{{color=#{r.groups()[0]}}}')
            text = text.replace('</color>', '{/color}')

        # Text
        last_chars = ''
        for text_unit in text.split('+'):
            # if len(chars.keys()) != 0:
            #     current_chars = ';'.join([f'{k}:{v}' for k, v in chars.items()])
            #     if current_chars != last_chars:
            #         for char in chars:
            #             ast_map.append(ast.Statement(['show', f'{to_codename(char)}_{chars[char]}']))
            #             avg_text += f'show {to_codename(char)}_{chars[char]}\n'
            #         last_chars = current_chars
            # else:
            #     last_chars = ''
            if name is None or text_unit == '':
                ast_map.append(ast.Text(text_unit))
                # avg_text += f"play sound '{tool.bgm_path_resolver.UI_ObjDown}'\n"
            elif text_unit != '':
                ast_map.append(ast.Text(text_unit, character=names[name]))
    ast_top.append(ast.Block('label', label, ast_map))
    result = ast.ast2rpy(ast_top)
    return result
    # return char_define(names) + '\n' + add_indentation(avg_text, label=label)


if __name__ == '__main__':
    # import time
    # t = time.time()
    mp = ast.Block('label', 'start', calls := [])
    debug = True


    def generate_avg_level(chapter, level, part):
        file_name = f'{chapter}-{level}-{part}'
        with open(f'avgtxt_main/{file_name}.bytes', 'r', encoding='utf-8') as file:
            s = file.read()

        label_name = 's' + file_name.replace('-', '_')
        avg_rpy_text = parser(s, label_name, debug_mode=True)
        with open(f'rpy/{label_name}.rpy', 'w', encoding='utf-8') as file:
            file.write(avg_rpy_text)
        print(avg_rpy_text)
        calls.append(ast.Statement('call', label_name))


    # Chapter 1~12, level 1~6, part 1~2
    chapter_, level_, part_ = 1, 1, 1
    while True:
        generate_avg_level(chapter_, level_, part_)
        if (part_ := part_ + 1) > 2:
            part_ = 1
            if (level_ := level_ + 1) > 6:
                level_ = 1
                if (chapter_ := chapter_ + 1) > 12:
                    break
    with open('rpy/script.rpy', 'w') as f:
        f.write(ast.ast2rpy(mp))

    if debug:
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
