#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
icon_gen (https://github.com/aillieo/app-icon-generator)
Fast and easy way to generate icons for iOS and Android apps
Created by Aillieo on 2017-08-10
With Python 3.5
"""

from PIL import Image
import os

# output path and size config:
path_iOS = ['Icon-57', 'Icon-114']
size_iOS = [570, 1140]
path_Android = ['drawable-hdpi/icon', 'drawable-mdpi/icon']
size_Android = [72, 48]
path_custom = ['my_icon', 'your_icon']
size_custom = [60, 100]

# generate options and params:
auto_overwrite = True
gen_for_iOS = True
gen_for_Android = False
need_frame = False
frame_width_ratio = float(30) / 512
frame_radius_ratio = float(90) / 512
frame_color = (255, 255, 255)
need_rounded = True
rounded_radius_ratio = float(90) / 512


def tips_for_gen_options():
    tips = """(You can customize the generate options and parameters in the script)"""
    print(tips)


def get_ref_file():
    """get reference image by finding one image file in current directory or manually input"""
    file_ext = ['png', 'jpg', 'jpeg']
    files = os.listdir('.')
    ref_file = ''
    for filename in files:
        if filename.split('.')[-1].lower() in file_ext:
            ref_file = filename
            break
    if ref_file:
        print('Will use "%s" as reference image' % ref_file)
    else:
        print('Can not find property file, now please specific one')
        ref_file = input('input file name:')
    if not os.path.exists(ref_file):
        raise IOError('file not found: ' + ref_file)
    return ref_file


def gen_template_img(ref_file):
    """get template image for later resizing"""
    template_img = Image.open(ref_file)
    size = min(template_img.width, template_img.height)
    template_img = template_img.resize((size, size), Image.BILINEAR)
    if need_frame:
        template_img = add_frame(template_img)
    if need_rounded:
        template_img = round_corner(template_img)
    return template_img


def gen_icons(template_img, dict_path_size):
    """generate icons by resizing template image according to sizes defined in size list"""
    for name, size in dict_path_size:
        name = 'out/' + name + '.png'
        name = os.path.normpath(name)
        path, base = os.path.split(name)
        if path and not os.path.exists(path):
            os.makedirs(path)
        out_img = template_img.resize((size, size), Image.BILINEAR)
        if auto_overwrite or not os.path.exists(name):
            try:
                out_img.save(name, 'PNG')
            except IOError:
                print("IOError: save file failed: " + name)
        else:
            print('File already exists: %s , set "auto_overwrite" True to enable overwrite' % name)


def round_corner(img_in):
    """rounding corner for template"""
    if img_in.mode != 'RGBA':
        img_in = img_in.convert('RGBA')
    size = img_in.size[0]
    radius = size * rounded_radius_ratio
    if radius > 0 and rounded_radius_ratio < 0.5:
        img_in.load()
        for i in range(size):
            for j in range(size):
                if in_corner(size, radius, i, j):
                    img_in.putpixel((i, j), (0, 0, 0, 0))
        print("Round corner finished!")
    else:
        print('Round corner failed due to invalid parameters, please check "rounded_radius_ratio"')
    return img_in


def add_frame(img_in):
    """adding frame for template"""
    size = img_in.size[0]
    width = size * frame_width_ratio
    radius = size * frame_radius_ratio
    if radius > 0 and frame_radius_ratio < 0.5 and frame_width_ratio < 0.5:
        img_in.load()
        for i in range(size):
            for j in range(size):
                if in_frame(size, width, radius, i, j):
                    img_in.putpixel((i, j), frame_color)
        print("Add frame finished!")
    else:
        print('Add frame failed due to invalid parameters, please check "frame_width_ratio" and "frame_radius_ratio"')
    return img_in


def in_corner(size, radius, x, y, base_offset=0):
    """judge whether a point is corner of icon"""
    x -= base_offset
    y -= base_offset
    center = (0, 0)
    if x < radius and y < radius:
        center = (radius, radius)
    elif x < radius and y > size - radius:
        center = (radius, size - radius)
    elif x > size - radius and y < radius:
        center = (size - radius, radius)
    elif x > size - radius and y > size - radius:
        center = (size - radius, size - radius)

    if center != (0, 0):
        if (x - center[0]) ** 2 + (y - center[1]) ** 2 > radius ** 2:
            return True
    return False


def in_frame(size, width, radius, x, y):
    """judge whether a point should be set frame color"""
    inner_rect = width < x < size - width and width < y < size - width
    if not inner_rect:
        return True
    else:
        return in_corner(size - 2 * width, radius - width, x, y, width)


if __name__ == '__main__':
    file = get_ref_file()
    tips_for_gen_options()
    img = gen_template_img(file)

    if gen_for_iOS:
        print('Generating for iOS...')
        dict_iOS = zip(path_iOS, size_iOS)
        gen_icons(img, dict_iOS)
    if gen_for_Android:
        print('Generating for Android...')
        dict_Android = zip(path_Android, size_Android)
        gen_icons(img, dict_Android)
    if not gen_for_iOS and not gen_for_Android:
        print('Generating custom icons...')
        dict_custom = zip(path_custom, size_custom)
        gen_icons(img, dict_custom)
    print('Finished icon generation!')