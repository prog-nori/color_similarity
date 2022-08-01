from operator import ne
import cv2
import os
import csv
import math
import numpy as np

from datetime import datetime
from src.util.color.translate import get_cielab1976, rgb2lab
from src.models.block import Block

CSV_FILE = 'output-2022-07-22-19-18-13.csv'


def get_formatted_datetime():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')


def get_mean_colors(an_img_file):
    """
    与えられた画像のRGB,HSV平均色を返す
    """
    rgb_img = cv2.imread(an_img_file, cv2.IMREAD_COLOR)

    if rgb_img is None:
        return -1, -1, -1, -1, -1, -1
    h, w, _ = rgb_img.shape
    search_range = rgb_img[0:h, 0:w]

    img = cv2.imread(an_img_file)
    if img is not None:
        avg_color_per_row = np.average(cv2.imread(an_img_file), axis=0)
        avg_color = np.average(avg_color_per_row, axis=0)
        # print(avg_color)
        blue = round(avg_color[0])
        green = round(avg_color[1])
        red = round(avg_color[2])
    else:
        blue = round(search_range.T[0].flatten().mean())
        green = round(search_range.T[1].flatten().mean())
        red = round(search_range.T[2].flatten().mean())

    hsv_img = cv2.cvtColor(search_range, cv2.COLOR_BGR2HSV)

    if hsv_img is None:
        return -1, -1, -1, -1, -1, -1

    hue = round(hsv_img.T[0].flatten().mean())
    salute = round(hsv_img.T[1].flatten().mean())
    value = round(hsv_img.T[2].flatten().mean())

    return red, green, blue, hue, salute, value


def find_all_files(directory):
    """
    指定されたディレクトリ内のすべてのファイルを再帰的に検索
    yieldでリストとして返す
    """
    for root, dirs, files in os.walk(directory):
        yield root
        for file in files:
            yield os.path.join(root, file)


def csv_row_2_dict(a_line):
    """
    カンマ区切りのcsvを辞書に変換（指定フォーマットを想定）
    """
    block = Block(
        file=a_line[0],
        name=a_line[1],
        red=int(a_line[2]),
        green=int(a_line[3]),
        blue=int(a_line[4]),
        hue=int(a_line[5]),
        saturation=int(a_line[6]),
        value=int(a_line[7]))
    return block


def csv_row_2_dict_all(a_list):
    """
    リストとして与えられた全てのデータを、カンマ区切りのcsvを辞書に変換（指定フォーマットを想定）
    """
    result = []
    for an_element in a_list:
        result.append(csv_row_2_dict(an_element))
    return result


def read_csv_as_nested_list(filename):
    """
    CSVファイルをネストされたリストとして読み込む
    """
    csv_file = open(filename, 'r', encoding='utf-8', errors='', newline='')
    csv_lines = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    return csv_lines


def pythagorean_proposition(a, b):
    """
    三平方の定理
    :param a: a
    :param b: b
    :return: c
    """
    return math.sqrt(a**2 + b**2)


def find_similar_colors(an_image, limit=20):
    """
    CSVのリストから、与えられた画像と近似色のものを探す
    """
    # 対象のファイルの色番号
    r, g, b, h, s, v = get_mean_colors(an_image)

    a_list = []
    nested_list = read_csv_as_nested_list(CSV_FILE)
    for el in csv_row_2_dict_all(nested_list):
        # CIELAB1976で2つのRGBを評価する
        a_dict = dict()
        a_dict['diff'] = get_cielab1976(rgb2lab(r, g, b), rgb2lab(el.red, el.green, el.blue))
        a_dict['info'] = el
        a_list.append(a_dict)
    return sorted(a_list, key=lambda x: x['diff'])[:limit]
