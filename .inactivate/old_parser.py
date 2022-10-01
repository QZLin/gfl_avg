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
