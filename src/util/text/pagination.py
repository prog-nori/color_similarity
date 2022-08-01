

import math


class Pagination(object):

    def __init__(self, offset=0, limit=20, items=[]):
        """
        コンストラクタ
        
        offsetもlimitも0インデックス
        """
        print(len(items))
        self.offset=offset
        self.limit=limit
        self.items=items[offset:limit]
        self.isActive=False
        self.max = math.ceil(len(items) / 20)
        super()
    
    def get_pagination_content(self, current_page_number):
        """
        Paginationのコンテンツ(list)を取得する
        current_page_numberは0インデックス
        """
        # n = len(self.items)
        n = self.max
        print(self.offset, self.limit, n, current_page_number)
        pagination = list()
        pagination.append(Page(label=1))
        index = lambda: list(set([pg.num for pg in pagination]))

        unit = [current_page_number - 1, current_page_number, current_page_number + 1]

        def put(el):
            actv = True if el == current_page_number else False
            pagination.append(Page(num=el, active=actv))
        for u in unit:
            if u in index() or u < 0 or u < n:
                continue
            if pagination[-1].label != '...':
                if u - pagination[-1].num == 2:
                    put(pagination[-1].num + 1)
                elif u - pagination[-1].num > 1:
                    pagination.append(Page())
            put(u)
        if n not in index():
            if n - pagination[-1].num > 1:
                pagination.append(Page())
            put(n)
        return pagination

class Page:
    def __init__(self, num=None, label=None, active=False):
        """
        num...ページ番号（0インデックス）
        label...ページ番号（1インデックス）
        """
        self.active = active

        if [num, label].count(None) == len([num, label]):
            # 両方空白なら...を入れる
            self.label = '...'
            self.num = None
            return

        if num is not None and label is None:
            self.label = num + 1
        else:
            self.label = label

        if num is None and label is not None:
            self.num = label - 1
        else:
            self.num = num
