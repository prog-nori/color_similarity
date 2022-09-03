
class Block:
    def __init__(
        self, file=None, name=None,
        red=None, green=None, blue=None,
        hue=None, saturation=None, value=None,
        rgb=None, hsv=None):
        self.file = file
        self.name = name
        self.red = red
        self.green = green
        self.blue = blue
        # self.hue = hue
        # self.saturation = saturation
        # self.value = value

        if rgb is None and all([red, green, blue]):
            self.rgb = Block.setRGB(red, blue, green)

        # if hsv is None and all([hue, saturation, value]):
        #     self.hsv = Block.setHSL(hue, saturation, value)

    @staticmethod
    def setRGB(r, g, b):
        return Block.colorFormat('rgb', r, g, b)

    # @staticmethod
    # def setHSL(h, s, v):
    #     return Block.colorFormat('hsl', h, s, v)

    # @staticmethod
    # def setHSV(h, s, v):
    #     return Block.colorFormat('hsv', h, s, v)

    @staticmethod
    def colorFormat(label, a, b, c):
        return '{}({}, {}, {})'.format(label, a, b, c)
