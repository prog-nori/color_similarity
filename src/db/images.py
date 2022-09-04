import pymysql.cursors

from src.db.DBConnection import DBConnection

class DBImagesTable(DBConnection):
    def __init__(self):
        """
        MySQLに接続する
        """
        super().__init__('images')
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
        return self.run_query_with_return(f'SELECT * FROM {self.table} WHERE id=%s', id)

    def add(self, filename):
        """
        追加
        """
        uuid = self.run_query_with_return('SELECT LEFT(UUID(), %s) as uuid', 8)[0]['uuid']
        sql = f'INSERT INTO {self.table} (id, filename) VALUES (%s, %s)'
        self.run_query(sql, uuid, filename)
        return uuid

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
