import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

# Fungsi untuk mengunggah data ke database MySQL
def upload_to_database():
    # Membuat koneksi ke database
    connection = mysql.connector.connect(
        host='localhost',
        user='root',
        password='',
        database='smartendance'
    )

    # Membuat kursor untuk eksekusi query
    cursor = connection.cursor()

    # Mendapatkan waktu saat ini
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')

    # Menjalankan query untuk menyimpan data ke tabel test_absen
    query = f"INSERT INTO test_absen (uid, waktu) VALUES ('{14045}', '{current_time}')"
    cursor.execute(query)

    # Melakukan commit untuk menyimpan perubahan
    connection.commit()

    # Menutup kursor dan koneksi
    cursor.close()
    connection.close()

    print(f"Data uploaded to database at {current_time}")
    print(f"Current time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')}")

if __name__ == '__main__':
    upload_to_database()
