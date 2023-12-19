import mysql.connector
import hashlib

class Database(object):
    def __init__(self, host: str, user: str, password: str, database: str):
        try:
            self.database = mysql.connector.connect(
                host=host,
                user=user,
                passwd=password,
                database=database
            )
            self.name = database
            self.cursor = self.database.cursor()
        except:
            print('Cannot connect to DataBase with current prompts')

    def get_table(self):
        self.cursor.execute('select user_name, user_results from users')
        return self.cursor

    def connection_status(self):
        return self.database.is_connected()

    def encryptSHA256(self, password):
        password = hashlib.sha256(password.encode())
        hex_dig = password.hexdigest()
        return hex_dig

    def remove_user(self, name):
        self.cursor.execute(f'delete from users where user_name = {name};')

    def get_name_table(self):
        self.cursor.execute('select user_name from users')
        return self.cursor
    def validation(self,email,password):


    def insert_user(self, name: str, login: str, password: str, results: float):
        if self.connection_status():
            try:
                '''add_user = ("insert into users"
                            "(user_name, user_login, user_password, user_results)"
                           "values (%s, %s, %s, %s)")
                user = (name, login, self.encryptSHA256(password), results)
                self.cursor.execute(add_user, user)
                #self.database.commit()'''
            except:
                print('values error')
    def edit_user(self):

mydb1 = Database('localhost', 'root', '7568853Ar', 'testdb123')
mydb2 = Database('localhost', 'root', '7568853Ar', 'testdb123')

