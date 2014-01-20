#!/usr/bin/env python

# eye from:
# http://www.flickr.com/photos/vernhart/910778661/
# face from:
# http://www.flickr.com/photos/ale_era/3512379377/
# god:
# <div xmlns:cc="http://creativecommons.org/ns#" about="http://www.flickr.com/photos/cobalt/2251980733/"><a rel="cc:attributionURL" href="http://www.flickr.com/photos/cobalt/">http://www.flickr.com/photos/cobalt/</a> / <a rel="license" href="http://creativecommons.org/licenses/by-nc-sa/2.0/">CC BY-NC-SA 2.0</a></div>
# baby:
# http://www.flickr.com/photos/jkunz/3285097079/
# portrait:
# http://www.flickr.com/photos/loxleyimages/2536542728/
import subprocess
import math
from numpy import array
from PIL import Image

GAMMA = 1.0
width = 50
vary_color_limit = .1
slant = .2;


if True:
    image_file = 'portrait.jpg'
    height = 20
    GAMMA = .5
    slant = .1;

image = Image.open(image_file)
aspect = float(image.size[0]) / image.size[1]

image = image.resize((width, height), Image.BICUBIC)
max_color = float(max(v[1] for v in image.getextrema()))

def float_range(fr, to, step=1.0):
    steps = (to - fr) / step
    for s in range(steps + 1):
        yield fr + float(to - fr) * s / steps

def int_and_remainder(v):
    return int(v), v % 1.0

def get_pixel(column, row):
    try:
        r, g, b = image.getpixel((column, row))
    except IndexError:
        r, g, b = 0, 0, 0
    return array([
        (r / max_color) ** GAMMA,
        (g / max_color) ** GAMMA,
        (b / max_color) ** GAMMA,
    ])

def rgb(x, y):
    column, col_blend = int_and_remainder(x * (image.size[0] - 1))
    row, row_blend = int_and_remainder((1.0 - y) * (image.size[1] - 1))

    topleft = get_pixel(column, row)
    topright = get_pixel(column + 1, row)
    bottomleft = get_pixel(column, row + 1)
    bottomright = get_pixel(column + 1, row + 1)

    return sum([
        topleft * (1.0 - col_blend) * (1.0 - row_blend),
        topright * (col_blend) * (1.0 - row_blend),
        bottomleft * (1.0 - col_blend) * (row_blend),
        bottomright * (col_blend) * (row_blend),
    ])

def color(x, y):
    r, g, b = rgb(x, y)
    m = max(r, g, b, vary_color_limit)
    return '%f %f %f' % (r / m, g / m, b / m)

def intensity(x, y):
    #return max(rgb(x, y))
    r, g, b = rgb(x, y)
    return 0.299 * r + 0.587 * g + 0.114 * b

from genshi.template import NewTextTemplate
template = NewTextTemplate(open('pipes.rib').read())

data = str(template.generate(sin=math.sin, rng=float_range, **locals()))
print data
#with open('out.rib', 'w') as stream:
#    stream.write(data)
#subprocess.check_call(['rndr', 'out.rib'])

