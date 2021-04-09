from re import search, sub

CHAR_DEF = 'define %s = Character("%s")'


def add_front(texts, sep_count=4, sep=' ', label_name=None):
    # string = ''
    # for x in texts.split('\n'):
    #     string += sep * sep_count + x + '\n'
    # return string
    string = sep * sep_count + ('\n' + sep * sep_count).join(texts.split('\n'))
    if label_name is not None:
        string = 'label %s:\n' % label_name + string
    return string


def render_chars(name_set):
    return '\n'.join([CHAR_DEF % (x, x) for x in name_set])


def render(source, names=None):
    avg_text = ''

    if names is None:
        names = set()

    for line in source.split('\n'):
        head = line[:line.find(':')]
        text = line[line.find(':') + 1:]

        img_head = sub(r'<\S+?>.+?</\S+?>', '', head)
        img = r'\S+?\(\d+?\)'

        name = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
        if name is not None:
            names.add(name.group())
        name = name.group() if name is not None else None

        for ltxt in text.split('+'):
            if name is None:
                avg_text += "'%s'\n" % ltxt
            elif ltxt != '':
                avg_text += "%s '%s'\n" % (name, ltxt)
    return render_chars(names) + '\n' + add_front(avg_text, label_name='start')


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
    s = '''()||<BGM>BGM_Sunshine</BGM><BIN>8</BIN>:格里芬S09区战术指挥室……
NPC-Kalin(1)<Speaker>活泼的少女</Speaker>||:早啊，指挥官。+这是您第一次来格里芬的指挥室吧，感觉怎么样？
NPC-Kalin(0)<Speaker>活泼的少女</Speaker>||:您最终决定来格里芬就职，真是太好了。
NPC-Kalin(0)<Speaker>格琳</Speaker>||:先自我介绍一下，我叫格琳娜（Kalina），未来将担任您的后勤官。+今后叫我格琳就可以了，而您呢……
NPC-Kalin(1)<Speaker>格琳</Speaker>||:“选择我们，加入我们！格里芬私人军事承包商，更新世界的锋芒！”+没错，从今天开始，您就是格里芬旗下的战术指挥官啦！
NPC-Kalin(2)<Speaker>格琳</Speaker>||:……诶，直到现在，您还担心自己能否胜任吗？
NPC-Kalin(1)<Speaker>格琳</Speaker>||:放心吧，格里芬的选拔是出了名的严格呢。+连那样的考验都能通过，您的身上一定有着值得信赖的才能。
NPC-Kalin(0)<Speaker>格琳</Speaker>||<黑点1>:+而接下来的训练，我会帮您认清这份才能……究竟是什么。+现在，请先切换到战术地图吧。
NPC-Kalin(1)<Speaker>格琳</Speaker><通讯框>||<黑点2><BIN>10</BIN>:指挥官，您听得到吗？+您的战术人形已准备就绪了，随时可以行动。+请部署她们，然后开始训练吧！'''
    print(render(s))
