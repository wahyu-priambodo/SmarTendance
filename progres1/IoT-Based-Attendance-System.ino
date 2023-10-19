#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN D1
#define SDA_PIN D2
#define BUZZER D8 // Set pin buzzer ke pin D8

MFRC522 mfrc522(SDA_PIN, RST_PIN);

void setup() {
  Serial.begin(9600); // Mengatur baud rate di 9600
  pinMode(BUZZER, OUTPUT); // Mengatur pin buzzer sebagai output
  SPI.begin();
  mfrc522.PCD_Init();
  Serial.println("Tempel RFID card/tag Anda...");
}

void loop() {
  if (mfrc522.PICC_IsNewCardPresent() && mfrc522.PICC_ReadCardSerial()) {
    Serial.print("UID Kartu: ");
    String uidStr = "";
    for (byte i = 0; i < mfrc522.uid.size; i++) {
      Serial.print(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " ");
      Serial.print(mfrc522.uid.uidByte[i], HEX);
      uidStr.concat(String(mfrc522.uid.uidByte[i] < 0x10 ? " 0" : " "));
      uidStr.concat(String(mfrc522.uid.uidByte[i], HEX));
    }
    Serial.println();
    mfrc522.PICC_HaltA();
    mfrc522.PCD_StopCrypto1();

    // Memeriksa UID dan menampilkan pesan "login berhasil" jika UID kartu/tag benar
    uidStr.toUpperCase();
    if (uidStr.substring(1) == "A7 5A 46 62" || uidStr.substring(1) == "09 8D 53 A3") {
      Serial.println("Kartu cocok... login berhasil!\n");
      tone(BUZZER, 500, 500); // Mengaktifkan buzzer
      delay(1000);
      noTone(BUZZER); // Menonaktifkan buzzer setelah 1 detik
    }
    else {
      Serial.println("Kartu tidak cocok... login gagal!\n");
      delay(1000);
    }
  }
}