import os

import UnityPy

path = r'D:\qproject\com.sunborn.girlsfrontline.cn\files\Android\New'
os.chdir(path)

e = UnityPy.load('asset_textavg.ab')
print(e)
