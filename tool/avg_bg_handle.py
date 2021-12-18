import cv2
from numpy import flipud
from sys import argv

if len(argv) < 2:
    print('File Name needed...')
    exit()
img = cv2.imread(argv[1])
# img = cv2.imread(r'3X.png')
cv2.imshow('', img)
h, w, z = img.shape
if h != 1024 or w != 1024:
    print('Not 1024x1024 img')
    exit()


def get_edge(corner, end=0, reverse=False):
    i = 0 if not reverse else end
    add = 1
    if reverse:
        corner = flipud(corner)
        add = -1
    for p in corner:
        x, y, z_ = p
        if x + y + z_ != 0:
            return i
        i += add
    return None


edge_u = get_edge(img[0:512, 512])
edge_d = get_edge(img[512:1024, 512], 1024, True)
print(edge_u, edge_d)

cv2.imwrite(argv[1], img[edge_u:edge_d])
# cv2.imshow('cut', img[edge_u:edge_d])
# cv2.waitKey()
