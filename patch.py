BGM_REPLACE_DICT = \
    {'BGM_Sunshine': 'home_formation_factory',
     'BGM_Wake': 'GF_Emotional_Normal_loop',
     'GF_EV3_Bingocard_loop': 'GF_Bingocard_loop'}


def bgm_patcher(key):
    if key in BGM_REPLACE_DICT.keys():
        key = BGM_REPLACE_DICT[key]
    return key
