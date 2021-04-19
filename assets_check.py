from os import walk


def check_bgm(path):
    with open('debug/bgm.txt', 'r', encoding='utf-8') as file:
        bgm = file.read().split('\n')
    exist_bgm = []
    for root, dirs, files in walk(path):
        for name in files:
            # print(name)
            exist_bgm.append(name)
    print('ERROR-LOST-FILE:')
    for x in bgm:
        if x + '.wav' not in exist_bgm:
            print(x)


check_bgm(r'D:\renprj\girlsfrontline\game\bgm')
