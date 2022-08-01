#! /usr/bin/env python3
#  -*- coding: utf-8 -*-

import this
import cv2
import numpy as np
import os
from pprint import pprint

OUTPUT_DIR = os.path.join('templates', 'images', 'svg')


def find_all_files(directory):
    """
    指定ディレクトリ配下のファイル名を再帰的に取得する
    .png, .jpg, .jpegで終わらないものは除外する。
    """
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            if file[-4:] == '.png' or file[-4:] == '.jpg' or file[-5:] == '.jpeg':
                yield os.path.abspath(os.path.join(root, file))


def get_rgb_data_from_file(file):
    """
    各画素のカラーコードを取得、2次元リストで返す
    """
    SIZE = 10
    an_image = cv2.imread(file, -1)
    if an_image is None:
        return None
    height, width, _ = an_image.shape
    a_list = list()
    for h in range(height):
        for w in range(width):
            this_cell = an_image[h, w].tolist()
            # BGRA
            # print(an_image[h, w])
            print(type(this_cell))
            if len(this_cell) == 3:
                this_cell.append(255)
                # an_image[h, w].append(255) = 255
            # print(len(an_image[h, w]), '|', an_image[h, w])
            rgba = 'rgba({}, {}, {}, {})'.format(this_cell[2], this_cell[1], this_cell[0], this_cell[3] / 255)
            a_list.append('\t<rect x="{}" y="{}" width="{}" height="{}" fill="{}" />'.format(w * SIZE, h * SIZE, SIZE, SIZE, rgba))
    return a_list


def main(args):
    """
    argsで指定されたディレクトリを再帰的に読み込み、ディレクトリ構造を維持したままpng, jpgをsvgへと変換する
    """
    for file in find_all_files(args[0]):
        svg_elements_list = ['<svg xmlns="http://www.w3.org/2000/svg" xmlns:xlink="http://www.w3.org/1999/xlink">']
        grid = get_rgb_data_from_file(file)
        if grid is None:
            continue
        else:
            svg_elements_list.extend(grid)
        svg_elements_list.append('</svg>')
        svg_str = '\n'.join(map(str, svg_elements_list))
        head = os.path.join('templates', 'images')
        output_base_file_name = file.split(head)[1]
        new_path_png = os.path.join(OUTPUT_DIR, output_base_file_name[1:])
        output_file_name = new_path_png.rsplit('.', 1)[0] + '.svg'
        dir_name, file_name = output_file_name.rsplit(os.sep, 1)
        if not os.path.exists(dir_name):
            os.makedirs(dir_name)
        with open(output_file_name, mode='w') as f:
            f.write(svg_str)
        print(os.path.abspath(output_file_name))
    #     return
        
    #     output_base_file_name = file.split(os.path.join('templates', 'images', os.sep))[1]
    #     output_file_name = os.path.join(OUTPUT_DIR, output_base_file_name.split('.')[0] + '.svg')
    #     print(file)
    # print('fin')
    return


if __name__ == '__main__':
    from sys import exit, argv
    exit(main(argv[1:]))