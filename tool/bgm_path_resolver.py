import cvtool

import patch
import tool.config as config

pl = cvtool.pla.PLAsset(config.RENPY_PROJECT, rel_root=config.RENPY_GAME, path_sep='/')
pl.build_library()

UI_ObjDown = pl.fpath('UI_ObjDown.wav')


def get_bgm(key):
    bgm = patch.bgm_patcher(key)
    if (path := pl.fpath(bgm + '.wav')) is None:
        path = 'musiclost.flac'
        with open('debug/bgm.txt', 'a') as f:
            f.write('LOST: {bgm}\n')
    else:
        path = path.replace('\\', '/')
        with open('debug/bgm.txt', 'a') as f:
            f.write(' {bgm}\n')
    return path


if __name__ == "__main__":
    print(pl.library)
    print(UI_ObjDown)
