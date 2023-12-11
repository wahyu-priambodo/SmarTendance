import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime
import random
import time


# Fungsi untuk mengunggah data ke database MySQL
def upload_to_database(payload):
    # Membuat koneksi ke database
    connection = mysql.connector.connect(
        host="sql12.freemysqlhosting.net",
        database="sql12669534",
        user="sql12669534",
        password="IDgkU64Rsf",
    )

    # Membuat kursor untuk eksekusi query
    cursor = connection.cursor()

    # Mendapatkan waktu saat ini
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S.%f")

    # Menjalankan query untuk menyimpan data ke tabel test_absen
    query = (
        f"INSERT INTO test_absen (uid, waktu) VALUES ('{payload}', '{current_time}')"
    )
    cursor.execute(query)

    # Melakukan commit untuk menyimpan perubahan
    connection.commit()

    # Menutup kursor dan koneksi
    cursor.close()
    connection.close()

    print(
        f"{payload} - {current_time} - {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}"
    )


if __name__ == "__main__":
    print("Payload   -    Waktu saat ini    -    Waktu saat fungsi dijalankan")
    while True:
        # Create random number with 8 digits
        payload = random.randint(10000000, 99999999)
        upload_to_database(payload)
        time.sleep(10)
