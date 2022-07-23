import json
import os

INFO = 'static/481c1390987f2432f8385d08f219728060e2144b'

class BlockName:
    """
    ブロック名に関するクラス
    """
    def __init__(self, hash='481c1390987f2432f8385d08f219728060e2144b'):
        """
        コンストラクタ。八種からファイルを読み込み、JSONをダンプして対応表をセットする
        """
        path = os.path.join('static', hash)
        json_dict = json.load(open(path, 'r'))
        self._dict = dict()
        for key, v in json_dict.items():
            if key[:6] == 'block.':
                if key == 'block.minecraft.diamond_ore':
                self._dict[key] = v

    def find(self, path):
        """
        与えられた画像のパスから対応するブロック名を返却する
        """
        if path[-4:] == '.png':
            path = path[:-4]

        target = path.split('textures/')[-1].replace('/', '.')
        target = 'block.minecraft.{}'.format(target.split('block.')[-1])
        return self._dict.get(target)

    def get(self):
        """
        ゲッタ
        """
        return self._dict


def main():
    a_dict = BlockName()
    print(a_dict.get())
    print(len(a_dict.get().keys()))

if __name__ == '__main__':
    main()
