from re import search, sub

CHAR_DEF = 'define %s = Character("%s")'

s = '''()||<BGM>BGM_Sunshine</BGM><BIN>8</BIN>:格里芬S09区战术指挥室……
NPC-Kalin(1)<Speaker>活泼的少女</Speaker>||:早啊，指挥官。+这是您第一次来格里芬的指挥室吧，感觉怎么样？
NPC-Kalin(0)<Speaker>活泼的少女</Speaker>||:您最终决定来格里芬就职，真是太好了。
NPC-Kalin(0)<Speaker>格琳</Speaker>||:先自我介绍一下，我叫格琳娜（Kalina），未来将担任您的后勤官。+今后叫我格琳就可以了，而您呢……
NPC-Kalin(1)<Speaker>格琳</Speaker>||:“选择我们，加入我们！格里芬私人军事承包商，更新世界的锋芒！”+没错，从今天开始，您就是格里芬旗下的战术指挥官啦！
NPC-Kalin(2)<Speaker>格琳</Speaker>||:……诶，直到现在，您还担心自己能否胜任吗？
NPC-Kalin(1)<Speaker>格琳</Speaker>||:放心吧，格里芬的选拔是出了名的严格呢。+连那样的考验都能通过，您的身上一定有着值得信赖的才能。
NPC-Kalin(0)<Speaker>格琳</Speaker>||<黑点1>:+而接下来的训练，我会帮您认清这份才能……究竟是什么。+现在，请先切换到战术地图吧。
NPC-Kalin(1)<Speaker>格琳</Speaker><通讯框>||<黑点2><BIN>10</BIN>:指挥官，您听得到吗？+您的战术人形已准备就绪了，随时可以行动。+请部署她们，然后开始训练吧！
'''

with open('avg.txt', 'w') as f:
    f.write('')

txt_file = ''


def printf(*args, sep=' ', end='\n', file=None):
    global txt_file
    txt = ''
    for x in args:
        txt += str(x) + ' '
    txt = txt[:-1]

    # with open('avg.txt', 'a+') as f:
    #     f.write(txt + '\n')
    txt_file += (txt + '\n')
    print(*args, sep=sep, end=end, file=file)


chars = set()

for line in s.split('\n'):
    head = line[:line.find(':')]
    text = line[line.find(':') + 1:]

    img_head = sub(r'<\S+?>.+?</\S+?>', '', head)
    img = r'\S+?\(\d+?\)'

    char = search(r'(?<=<Speaker>).*(?=</Speaker>)', line)
    char = char.group() if char is not None else ''
    chars.add(char)

    for t in text.split('+'):
        if char == '':
            printf('\'%s\'' % t)
        else:
            printf(char, '\'%s\'' % t)

chars.remove('')
for c in chars:
    txt_file = CHAR_DEF % (c, c) + '\n' + txt_file

with open('avg.txt', 'w') as f:
    f.write(txt_file)
