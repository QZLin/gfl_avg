import cvtool.no_path_asset as npa

import tool.config as config

np = npa.NPAssets(config.RENPY_PROJECT, relpath=True,
                  relroot=config.RENPY_GAME)
np.build_library()

UI_ObjDown = np.fpath('UI_ObjDown.wav').replace('\\', '/')
print(np.library)
