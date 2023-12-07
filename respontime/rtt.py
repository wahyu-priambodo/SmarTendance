import paho.mqtt.client as mqtt
import mysql.connector
from datetime import datetime

# Fungsi untuk menghandle pesan MQTT
def on_message(client, userdata, msg):
    # Mendapatkan payload dari pesan MQTT
    payload = msg.payload.decode('utf-8')
    print(f"Received message: {payload}")

    # Mengunggah data ke database MySQL
    upload_to_database(payload)

# Fungsi untuk mengunggah data ke database MySQL
def upload_to_database(payload):
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
    current_time = datetime.now().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3]

    # Menjalankan query untuk menyimpan data ke tabel test_absen
    query = f"INSERT INTO test_absen (uid, waktu) VALUES ('{payload}', '{current_time}')"
    cursor.execute(query)

    # Melakukan commit untuk menyimpan perubahan
    connection.commit()

    # Menutup kursor dan koneksi
    cursor.close()
    connection.close()

    print(f"Data uploaded to database at {current_time}")

# Membuat koneksi ke broker MQTT
client = mqtt.Client()
client.on_message = on_message
client.connect("free.mqtt.iyoti.id", 1883, 60)

# Subscribing ke topik tertentu
client.subscribe("SmarTendance/ESP8266")

# Loop forever untuk mendengarkan pesan
client.loop_forever()
