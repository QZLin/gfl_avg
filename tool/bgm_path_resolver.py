import cvtool

import tool.config as config

pl = cvtool.pla.PLAsset(config.RENPY_PROJECT, rel_root=config.RENPY_GAME, path_sep='/')
pl.build_library()

UI_ObjDown = pl.fpath('UI_ObjDown.wav')

if __name__ == "__main__":
    print(pl.library)
    print(UI_ObjDown)
