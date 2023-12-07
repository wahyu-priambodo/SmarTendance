#include <SPI.h>
#include <MFRC522.h>

#define RST_PIN 9  // Reset pin for RC522
#define SS_PIN 10 // SDA pin for RC522

MFRC522 rfid(SS_PIN, RST_PIN); // Create MFRC522 instance
MFRC522::MIFARE_Key key;

void setup() {
  Serial.begin(9600);
  SPI.begin();
  rfid.PCD_Init();
  Serial.println("Tempel RFID card/tag Anda...");
}

void loop() {
  if ( !rfid.PICC_IsNewCardPresent() )
    return;
  
  if ( !rfid.PICC_ReadCardSerial() )
    return;

  String uid = "";
  for (byte i = 0; i < 4; i++)
    uid += rfid.uid.uidByte[i];
  
  Serial.print(uid); // Jangan diganti! Karena valuenya akan dikirim ke ESP8266

  uid = ""; // Reset
  rfid.PICC_HaltA();
  rfid.PCD_StopCrypto1();
}