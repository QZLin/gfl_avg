import cv2
from numpy import flipud
from sys import argv

if len(argv) < 2:
    print('File Name needed...')
    exit()
img = cv2.imread(argv[1])


def get_edge(corner, end=0, reverse=False):
    i = 0 if not reverse else end
    if reverse:
        corner = flipud(corner)
    for p in corner:
        x, y, z = p
        if x + y + z != 0:
            return i
        i += 1 if not reverse else -1
    return None


edge_u = get_edge(img[0:512, 512])
edge_d = get_edge(img[512:1024, 512], 1024, True)
print(edge_u, edge_d)

cv2.imwrite(argv[1], img[edge_u:edge_d])
# cv2.imshow('cut', img[edge_u:edge_d])
# cv2.waitKey()
