import re
from database import connect_database, create_abonents_table, drop_abonents_table
import csv
from datetime import datetime
import os


date = datetime.now().strftime("%d_%m_%Y")
time = datetime.now().strftime("%H%M")

drop_abonents_table()

create_abonents_table()



def read_file(file: str):
    with open(file, mode="r", encoding="utf-8") as file:
        for line in file:
            match = re.search(
                r'\w+ \w+  \d+ \d\d:\d\d:\d\d \d+ \w+-\w+/\d+.\d+.\d+.\d+:\d+ Control Channel: TLSv1, cipher TLSv1/SSLv3 DHE-RSA-AES256-SHA, 1024 bit RSA',
                line)
            try:
                match1 = match.group()
                server_key = re.search(r'\d+-\d+', match1).group()
                ip_address = re.search(r'\d+\.\d+\.\d+\.\d+', match1).group()
                connection, cursor = connect_database()
                cursor.execute("""INSERT INTO abonents (server_key, ip_address)
                    VALUES (?, ?)
                """, (server_key, ip_address))
                connection.commit()
                connection.close()
            except:
                pass


def export_to_csv():
    # folder = os.makedirs(f"active_abonents{date}_{time}", mode=0o777)
    connection, cursor = connect_database()
    print("Exporting data into CSV..........")
    cursor.execute("""SELECT * FROM abonents""")
    with open(f"abonents/active_abonents{date}_{time}.csv", mode="w") as file:
        csv_writer = csv.writer(file, delimiter=";")
        csv_writer.writerow([i[0] for i in cursor.description])
        csv_writer.writerows(cursor)


for i in range(10000):
    try:
        read_file(f"openvpn/srv{i}.log")
    except:
        pass

read_file("openvpn/srvsrv122.log")
read_file("openvpn/srvsrv220.log")

export_to_csv()
