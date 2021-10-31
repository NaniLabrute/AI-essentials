import mysql.connector
import csv

class Database:
    db_instance = None
    csv_instance = None

    def __init__(self):
        #mysql
        if self.db_instance is None:
            self.db_instance = mysql.connector.connect(
                host="localhost",
                user="root",
                password="p@ssw0rd1",
                database="Game",
                auth_plugin="mysql_native_password")
            self.db_cursor = self.db_instance.cursor()

    def init_database(self):
        try:
            self.db_cursor.execute("CREATE TABLE players ("
                                   "name VARCHAR(255),"
                                   "mail VARCHAR(255) PRIMARY KEY,"
                                   "password VARCHAR(255),"
                                   "coins int,"
                                   "level int)")
        except Exception:
            print("table already existe")

    def add_player_account(self, name, mail, password, coins, level):
        try:
            sql = "INSERT INTO players (name, mail, password, coins, level) VALUES (%s, %s, %s, %s, %s)"
            val = (f'{name}', f'{mail}', f'{password}', f'{coins}', f'{level}')
            self.db_cursor.execute(sql, val)
            self.db_instance.commit()
        except:
            print("email already exist")

    def get_player_account(self, mail, password):
        try:
            sql = "SELECT mail FROM players WHERE mail = %s AND password = %s"
            val = (f'{mail}', f'{password}')
            self.db_cursor.execute(sql, val)
            return self.db_cursor.fetchall().__getitem__(0).__getitem__(0)
        except:
            print("you mail or you password is wrong")
            return ""

    def update_player_coins(self, coins, mail):
        sql = "UPDATE players SET coins = %s WHERE mail = %s"
        val = (f'{coins}', f'{mail}')
        self.db_cursor.execute(sql, val)
        self.db_instance.commit()

    def update_player_level(self, level, mail):
        sql = "UPDATE players SET level = %s WHERE mail = %s"
        val = (f'{level}', f'{mail}')
        self.db_cursor.execute(sql, val)
        self.db_instance.commit()

    def add_player_score(self, coins, mail):
        sql = "SELECT coins FROM players WHERE mail = %s"
        val = (f'{coins}',)
        self.db_cursor.execute(sql, val)
        result = [mail, coins]
        with open('leaderboard.csv','w') as f:
            writer = csv.writer(f)
            writer.writerow(result)