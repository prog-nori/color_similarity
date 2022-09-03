import pymysql.cursors

from src.db.DBConnection import DBConnection

class DBImagesTable(DBConnection):
    def __init__(self):
        """
        MySQLに接続する
        """
        super('images')
        return

    def find(self):
        """
        全件参照
        """
        print('DBImagesTable.find()の実装予定はありません')
        return

    def get(self, id):
        """
        idで一件参照
        """
        return self.run_query_with_return(f'SELECT * FROM {self.table} WHERE id={id}')

    def add(self, filename):
        """
        追加
        """
        return self.run_query(f'INSERT INTO {self.table} (id, filename) VALUES (LEFT(UUID(), 8), %s)', filename)

    def update(self):
        """
        更新
        """
        print('DBImagesTable.update()の実装予定はありません')
        return

    def remove(self):
        """
        削除
        """
        print('DBImagesTable.remove()の実装予定はありません')
        return
