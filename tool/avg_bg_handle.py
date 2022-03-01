from os import fdopen

import argparse
import cv2.cv2 as cv
from sys import stdout

import cvtool

parser = argparse.ArgumentParser()
parser.add_argument('image')
parser.add_argument('-f', '--file', type=str)
parser.add_argument('-c', '--compress', type=int, choices=range(0, 11), default=0)
# parser.add_argument('-o', '--output', type=str)
args = parser.parse_args()
# print(args.image)

img = cvtool.im.sim_screen_crop((1280, 720), cvtool.im.uimread(args.image))
img = cv.resize(img, (1280, 720), interpolation=cv.INTER_CUBIC)  # cv.INTER_LINEAR
# cvtool.im.test_img(img)
out = cv.imencode('.png', img)[1]

if args.file:
    cvtool.im.uimwrite(args.file, '.png', img, [cv.IMWRITE_PNG_COMPRESSION, args.compress])
else:
    with fdopen(stdout.fileno(), "wb", ) as stdout:
        stdout.write(out)
        stdout.flush()
