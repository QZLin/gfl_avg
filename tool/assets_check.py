from os import walk

import tool.config as config


def check_bgm(path):
    with open('../debug/bgm.txt', 'r', encoding='utf-8') as file:
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


def check_background(path):
    pass


if __name__ == '__main__':
    check_bgm(config.RENPY_BGM)
