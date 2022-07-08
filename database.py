import sqlite3


def connect_database():
    connection = sqlite3.connect("active_abonents.sqlite")
    cursor = connection.cursor()
    return connection, cursor


def create_abonents_table():
    connection, cursor = connect_database()
    cursor.execute("""CREATE TABLE IF NOT EXISTS abonents(
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        server_key VARCHAR(10) NOT NULL UNIQUE,
        ip_address VARCHAR(20) NOT NULL UNIQUE
    )""")
    connection.commit()
    connection.close()


def drop_abonents_table():
    connection, cursor = connect_database()
    cursor.execute("""DROP TABLE IF EXISTS abonents""")
    connection.commit()
    connection.close()
