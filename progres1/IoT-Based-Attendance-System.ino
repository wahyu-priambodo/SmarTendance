#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN D1 // Set pin reset rc522 di pin D1 esp8266
#define SDA_PIN D2 // Set pin SDA rc522 di pin D2 esp8266
#define BUZZER D8 // Set pin buzzer di pin D8 esp8266

MFRC522 rfid(SDA_PIN, RST_PIN);
MFRC522::MIFARE_Key key;

String uid = ""; // Untuk menyimpan data UID kartu/tag
String lastUID = ""; // Untuk menampung UID kartu/tag yang sebelumnya telah digunakan
bool userLoggedIn = false; // Variabel penanda apakah user sudah login

void setup() {
  Serial.begin(9600); // Mengatur baud rate di 9600
  pinMode(BUZZER, OUTPUT); // Mengatur pin buzzer sebagai output
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Tempel RFID card/tag Anda...");
}

void loop() {
  if (rfid.PICC_IsNewCardPresent() && rfid.PICC_ReadCardSerial()) {
    for (byte i = 0; i < 4; i++) {
      uid += rfid.uid.uidByte[i];
    }
    Serial.print("UID Kartu: ");
    Serial.println(uid);

    // User belum login
    if (!userLoggedIn) {
      // Memeriksa kartu/tag apakah UIDnya sesuai atau tidak. Jika iya, maka login berhasil.
      if (uid == "167907098" || uid == "914183163") {
        Serial.println("Kartu cocok... login berhasil!\n");
        tone(BUZZER, 500, 500); // Membunyikan buzzer selama 5s ketika user pertama kali login
        userLoggedIn = true; // Set variabel penanda menjadi true.
        lastUID = uid;
        Serial.print("lastUID:");
        Serial.println(lastUID);
        Serial.print("uid:");
        Serial.println(uid);
        delay(500);
        noTone(BUZZER); // Menonaktifkan buzzer setelah user login.
      }
      // Jika UID kartu/tag tidak sesuai, maka login gagal.
      else {
        Serial.println("Kartu tidak cocok... Login gagal!\n");
        delay(1000);
      }
    }
    // User sudah login
    else {
      if (lastUID == uid) {
        Serial.println("Anda sudah login!\n");
        // Membunyikan buzzer 2 kali selama 2s
        for (int i=1; i<=2; i++) {
          tone(BUZZER, 500, 200);
          delay(100);
          noTone(BUZZER);
          delay(100);
        }
      }
    }
    uid = ""; // Reset uid value
    rfid.PICC_HaltA();
    rfid.PCD_StopCrypto1();
  }
}