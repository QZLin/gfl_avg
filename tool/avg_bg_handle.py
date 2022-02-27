from os import fdopen

import argparse
import cv2.cv2 as cv
from sys import stdout

import cvtool

parser = argparse.ArgumentParser()
parser.add_argument('image')
parser.add_argument('-f', '--file', action='store_true')
parser.add_argument('-o', '--output', type=str)
args = parser.parse_args()
# print(args.image)

img = cvtool.im.sim_screen_crop((1280, 720), cvtool.im.uimread(args.image))
# cvtool.im.test_img(img)
out = cv.imencode('.png', img)[1]

if args.file:
    cvtool.im.uimwrite(args.output, '.png', img)
else:
    with fdopen(stdout.fileno(), "wb", ) as stdout:
        stdout.write(out)
        stdout.flush()
