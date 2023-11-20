#include <ESP8266WiFi.h>
#include <PubSubClient.h>
#include <MFRC522.h> // for RC522 sensor
#include <LiquidCrystal_I2C.h> // for LCD 16x2 I2C
#include <ArduinoJson.h> // for parsing JSON message/data

// RC522 settings
#define RST_PIN D0 // Reset pin for RC522
#define SS_PIN  D8 // SDA pin for RC522

// Buzzer pin
#define BUZZER D4

MFRC522 mfrc522(SS_PIN, RST_PIN); // Instansiasi objek mfrc522 sebagai sensor rfid 
// MFRC522::MIFARE_Key key;

// LCD settings
LiquidCrystal_I2C lcd(0x27, 16, 2); // Address 0x27, 16 columns, 2 rows

// WiFi settings
const char* wifi_ssid = "gaz";
const char* wifi_pass = "12345678";
WiFiClient esp8266_client;

// MQTT configurations
//const char* mqtt_broker = "587dd96c589c4f5b8f049f2d78f8f801.s1.eu.hivemq.cloud";
const char* mqtt_broker = "free.mqtt.iyoti.id"; // or "broker.hivemq.com"
const int mqtt_port = 1883;
const char* client_id = "esp8266-mqtt-client";
//const char* username = "SmarTendance";
//const char* password = "SmarTendance-MQTT123";
const char* sub_topic = "SmarTendance/SERVER"; // get message from the PHP Server
const char* pub_topic = "SmarTendance/ESP8266"; // send message to the server
PubSubClient mqtt_client(esp8266_client); // client id

/* DEKLARASI PROTOTIPE FUNGSI */
void reconnect_mqtt_broker();
void connect_wifi();
void callback(char* topic, byte* payload, unsigned int length);

void setup() {
  Serial.begin(115200);
  SPI.begin();
  mfrc522.PCD_Init();

  // Set connection settings
  mqtt_client.setServer(mqtt_broker, mqtt_port); // using tls port (8883)
  mqtt_client.setCallback(callback);

  // Initiate LCD and buzzer as an outputs
  lcd.init();
  lcd.backlight();
  lcd.print("# SmarTendance #");
  lcd.setCursor(0, 1);
  lcd.print("Tempel kartu....");
  pinMode(BUZZER, OUTPUT);
}

// unsigned long curr_time = millis();
// unsigned long prev_time = 0;
// const long delay_time = 1000;

void loop() {
  // Pengecekan untuk koneksi WiFi
  if (WiFi.status() != WL_CONNECTED) { connect_wifi(); }
  
  // Pengecekan untuk koneksi Mqtt Client
  if (!mqtt_client.connected()) {
    reconnect_mqtt_broker(); // menghubungkan ulang ke Mqtt broker
  }
  // Jika sudah terhubung dgn Mqtt broker
  else {
    mqtt_client.loop(); // lakukan looping terus untuk mendapatkan message dari publisher (SmarTendance/SERVER)
  }

  // Pengecekan untuk baca kartu
  if (!mfrc522.PICC_IsNewCardPresent()) { return; }
  if (!mfrc522.PICC_ReadCardSerial()) { return; }

  // Looping untuk membaca uid kartu/tag
  String uid = "";
  for (byte i = 0; i < mfrc522.uid.size; i++) { 
    uid += String(mfrc522.uid.uidByte[i]);
    // uid += String(mfrc522.uid.uidByte[i], HEX);
  }

  // Menampilkan hasil uid kartu/tag ke serial mon.
  Serial.print("Student UID: ");
  Serial.println(uid);

  // Pengecekan untuk publish
  if (mqtt_client.publish(pub_topic, uid.c_str())) {
    Serial.print("Student UID has successfully published on topic [");
    Serial.print(pub_topic);
    Serial.println("]");
  }
  // Tampilkan pesan error jika gagal publish
  else {
    Serial.println("Failed to publish student UID");
  }

  delay(1000); // Delay setiap 1s untuk mendapatkan pesan atau publish pesan baru
}

void callback(char* topic, byte* payload, unsigned int length) {
  Serial.print("Message received on topic [");
  Serial.print(sub_topic);
  Serial.println("]: ");

  // Parsing JSON message
  StaticJsonDocument<200> jsonDoc;
  DeserializationError error = deserializeJson(jsonDoc, payload, length);

  // Handle error parsing JSON
  if (error) {
    Serial.print("Failed to parse JSON: ");
    Serial.println(error.c_str());
    return;
  }

  // Mendapatkan nilai dari kunci "keterangan" dan "status"
  const char* keterangan = jsonDoc["keterangan"];
  const char* status = jsonDoc["status"];
  
  Serial.print("Keterangan: ");
  Serial.println(keterangan);
  Serial.print("Status: ");
  Serial.println(status);

  // kirim data ke Arduino lewat serial comm.
  lcd.clear();
  if (strcmp(keterangan, "Student UID is registered") == 0 && strcmp(status, "Unavailable course for now") != 0) {
    lcd.print("Absensi Berhasil");
    lcd.setCursor(0, 1);
    lcd.print("Status:");
    lcd.print(status);

    // Bunyikan buzzer
    if (strcmp(status, "Hadir") == 0) { // status kehadiran: hadir
      tone(BUZZER, 500, 200);
      delay(500);
      noTone(BUZZER);
    }
    else if (strcmp(status, "Terlambat") == 0 || strcmp(status, "Alpa") == 0) { // status kehadiran: terlambat / alpa
      for (int i=1; i<=2; i++) {
        tone(BUZZER, 500, 200);
        delay(100);
        noTone(BUZZER);
        delay(100);
      }
    }
    else {
      // bunyi 3 kali selama 0,2 dtk
      for (int i=1; i<=3; i++) {
        tone(BUZZER, 500, 200);
        delay(100);
        noTone(BUZZER);
        delay(100);
      }
    }

    delay(5000);
  }
  else if (strcmp(keterangan, "Student UID is not registered") == 0) {
    lcd.print("Student UID is-");
    lcd.setCursor(0, 1);
    lcd.print("not registered!");

    // bunyi 3 kali selama 0,2 dtk
    for (int i=1; i<=3; i++) {
      tone(BUZZER, 500, 200);
      delay(100);
      noTone(BUZZER);
      delay(100);
    }
    
    delay(5000);
  }
  // tampilkan pesan ke awal setelah 3 dtk
  lcd.clear();
  lcd.print("# SmarTendance #");
  lcd.setCursor(0, 1);
  lcd.print("Tempel kartu....");
}

void reconnect_mqtt_broker() {
  while (!mqtt_client.connected()) {
    Serial.println("Connecting to MQTT broker: " + String(mqtt_broker));
    
    /* USING USERNAME AND PASSWORD
    if (mqtt_client.connect(client_id, username, password)) {
      Serial.println("Connected to MQTT broker");
      mqtt_client.subscribe(sub_topic);
    }
    */
    if (mqtt_client.connect(client_id)) {
      Serial.print("Connected to : ");
      Serial.println(mqtt_broker);
      mqtt_client.subscribe(sub_topic);
    }
    else {
      Serial.print("failed, rc=");
      Serial.print(mqtt_client.state());
      Serial.println(": Connection to MQTT broker failed!");
    }
  }
}

void connect_wifi() {
  Serial.print("Connecting to WiFi");
  WiFi.begin(wifi_ssid, wifi_pass);

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println();
  Serial.print("Connected to: ");
  Serial.println(wifi_ssid);

  Serial.print("IP Address: ");
  Serial.println(WiFi.localIP());
}