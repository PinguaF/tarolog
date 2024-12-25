import sqlite3

class User:
    def __init__(self, id):
        print(f"200 Redirect to class User(-> db/db.py) via {id}")
        self.Id = id
        with sqlite3.connect("main.db") as db:
                cursor = db.cursor()
                cursor.execute(f"""SELECT * FROM Users WHERE Id = {self.Id}""")
                db_user_data = cursor.fetchall()
                print(db_user_data)
                self.Username = db_user_data[0][1]
                self.CountCard = db_user_data[0][2]
                self.Subscription = db_user_data[0][3]
                self.TypeAstrolog = db_user_data[0][4]
                self.Zodiak = db_user_data[0][5]
                self.Role = db_user_data[0][6]
                self.Claimed = db_user_data[0][7]

    def __del__(self):
        print("delete class User")    

def insert_user_into_db(message):
        with sqlite3.connect("main.db") as db:
            cursor = db.cursor()
            cursor.execute(f"""SELECT Id FROM Users WHERE Id = {message.chat.id}""")
            user = cursor.fetchall()
            if not user:
                cursor.execute(f""" INSERT INTO Users (Id, Username, CountCard, Subscription, TypeAstrolog, Zodiak, Role, Claimed) VALUES ({message.chat.id}, '{(message.from_user.first_name)}', {2}, {False}, {0}, {0}, 'user', {False} ) """)
                db.commit()
        db.close()
        return
    
    
