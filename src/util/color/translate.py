import math

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
