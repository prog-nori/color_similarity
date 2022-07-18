from re import L
import cv2
import os
import csv
import math

from datetime import datetime

CSV_FILE = 'output-2022-07-18-21-52-53.csv'

def get_formatted_datetime():
    return datetime.now().strftime('%Y-%m-%d-%H-%M-%S')

def get_mean_colors(an_img_file):
    """
    与えられた画像のRGB, HSV平均色を返す
    """
    rgb_img = cv2.imread(an_img_file, cv2.IMREAD_COLOR)
    
    if rgb_img is None:
        return -1, -1, -1, -1, -1, -1
    h, w, _ = rgb_img.shape
    search_range = rgb_img[0:h, 0:w]

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
    a_dict = dict()
    try:
        a_dict['file'] = a_line[0]
        a_dict['red'] = int(a_line[1])
        a_dict['green'] = int(a_line[2])
        a_dict['blue'] = int(a_line[3])
        a_dict['hue'] = int(a_line[4])
        a_dict['saturation'] = int(a_line[5])
        a_dict['value'] = int(a_line[6])
        a_dict['rgb'] = 'rgb({}, {}, {})'.format(a_line[1], a_line[2], a_line[3])
        a_dict['hsv'] = 'hsv({}, {}, {})'.format(a_line[4], a_line[5], a_line[6])
    except ValueError as e:
        print(e)
        print(type(e))
    return a_dict

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
    csv_file = open(filename, 'r', encoding='ms932', errors='', newline='')
    csv_lines = csv.reader(csv_file, delimiter=",", doublequote=True, lineterminator="\r\n", quotechar='"', skipinitialspace=True)
    return csv_lines

# 三平方の定理
pythagorean_proposition = lambda a, b: math.sqrt(a**2 + b**2)

def find_similar_colors(an_image, limit=20):
    """
    CSVのリストから、与えられた画像と近似色のものを探す
    """
    # 対象のファイルの色番号
    r, g, b, h, s, v = get_mean_colors(an_image)

    a_list = []
    for el in csv_row_2_dict_all(read_csv_as_nested_list(CSV_FILE)):
        r2, g2, b2 = el['red'], el['green'], el['blue']
        # CIELAB1976で2つのRGBを評価する
        a_dict = dict()
        a_dict['diff'] = get_cielab1976(rgb2lab(r, g, b), rgb2lab(r2, g2, b2))
        a_dict['info'] = el
        a_list.append(a_dict)
    return sorted(a_list, key=lambda x: x['diff'])[:limit]


def rgb2xyz(r, g, b):
    """
    RGB色空間をXYZ色空間へと変換する
    """
    r /= 255
    g /= 255
    b /= 255

    func = lambda c: ((c + 0.055) / 1.055) ** 2.4 if c > 0.04045 else c / 12.92

    r = func(r) * 100
    g = func(g) * 100
    b = func(b) * 100
    
    xyz = dict({'z': 0, 'y': 0, 'z': 0})
    xyz['x'] = r * 0.4124 + g * 0.3576 + b * 0.1805
    xyz['y'] = r * 0.2126 + g * 0.7152 + b * 0.0722
    xyz['z'] = r * 0.0193 + g * 0.1192 + b * 0.9505

    return xyz

def xyz2lab(x, y, z):
    """
    XYZ色空間をLab色空間へと変換する
    """
    x = x / 95.047
    y = y / 100.000
    z = z / 108.883

    func = lambda c: c ** (1 / 3) if c > 0.008856 else (7.787 * c) + (16 / 116)

    x = func(x)
    y = func(y)
    z = func(z)

    lab = Lab()
    lab.l = (116 * y) - 16
    lab.a = 500 * (x - y)
    lab.b = 200 * (y - z)

    return lab

def rgb2lab(r, g, b):
    """
    RGB色空間をLab色空間へと変換する
    """
    xyz = rgb2xyz(r, g, b)
    return xyz2lab(xyz['x'], xyz['y'], xyz['z'])

def get_cielab1976(lab1, lab2):
    """
    CIELABの値を取得する。
    引数にLab型の変数を2つとる
    """
    get = lambda x, y: (x - y) ** 2

    l = get(lab1.l, lab2.l)
    a = get(lab1.a, lab2.a)
    b = get(lab1.b, lab2.b)

    return math.sqrt(l + a + b)

class Lab:
    """
    Lab色空間を表すクラス
    """
    def __init__(self, l=0, a=0, b=0):
        """
        コンストラクタ
        """
        self.l = l
        self.a = a
        self.b = b
