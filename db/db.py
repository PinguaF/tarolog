import sqlite3

def get_user_from_db(id):
    with sqlite3.connect("main.db") as db:
        cursor = db.cursor()
        cursor.execute(f"""SELECT * FROM Users WHERE Id = {id}""")
        user = cursor.fetchall()
        if not user:
            return 0
    db.close()
    return user


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