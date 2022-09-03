import pymysql.cursors

class DBConnection(object):
    def __init__(self, table_name):
        """
        コンストラクタ。自身のインスタンス生成時に実行される
        MySQLに接続する
        """
        self.connection = pymysql.connect(
            host='localhost',
            user='root',
            password='P@ssw0rd',
            database='minecraft_utility',
            cursorclass=pymysql.cursors.DictCursor)
        self.table = table_name
        return

    def __del__(self):
        """
        デストラクタ。自身のインスタンス破壊時に実行される
        MySQLの接続を切断する
        """
        self.connection.close()
    
    def run_query(self, sql, *args):
        """
        クエリを実行する。戻り値は無し
        対象: insert, update, delete
        """
        with self.connection:
            with self.connection.cursor() as cursor:
                cursor.executemany(sql, args)
            self.connection.commit()
        return
    
    def run_query_with_return(self, sql):
        """
        クエリを実行する。戻り値は有り
        対象: select
        """
        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql)
            results = cursor.fetchall()
        return results
        
    def run_query_with_return(self, sql, *args):
        """
        クエリを実行する。戻り値は有り
        対象: select
        """
        results = []
        with self.connection.cursor() as cursor:
            cursor.execute(sql, args)
            results = cursor.fetchall()
        return results
