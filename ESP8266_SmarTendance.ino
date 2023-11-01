#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <SoftwareSerial.h>

// Wifi settings
const char* ssid = "POCO M3";
const char* password = "Awikwok123456";

// Server settings
const char* serverIP = "192.168.4.127";
const int serverPort = 80;
const String serverPath = "handle-uid.php";

// Serial comm to Arduino
SoftwareSerial Arduino(D1, D2);  // RX, TX

void sendUIDToServer(String uid) {
  WiFiClient client;
  if ( !client.connect(serverIP, serverPort) ) {
    Serial.println("Connection Failed!");
    return;
  }

  HTTPClient http;
  String endpoint = "http://"+String(serverIP)+"/"+serverPath;

  http.begin(client, endpoint);
  http.addHeader("Content-Type", "application/x-www-form-urlencoded");  

  String postData = "uid=" + uid;
  int httpResponseCode = http.POST(postData);

  if ( httpResponseCode > 0 ) {
    String response = http.getString();
    Serial.println("HTTP Response code: " + String(httpResponseCode));
    Serial.println(response);
  } else {
    Serial.print("Error in sending POST request. Error code: ");
    Serial.println(httpResponseCode);
  }

  http.end();
}

void setup() {
  Serial.begin(115200);
  Arduino.begin(9600);
  WiFi.begin(ssid, password);

  while ( WiFi.status() != WL_CONNECTED ) {
    delay(1000);
    Serial.println("Connecting to WiFi...");
  }
  
  Serial.print("IP address: ");
  Serial.println(WiFi.localIP());
}

void loop() {
  String uid = "";
  if ( Arduino.available() > 0 ) {
    uid = Arduino.readStringUntil('\n');
    if (uid != "") {
      // Kirim UID ke halaman PHP
      sendUIDToServer(uid);
    }
  }
}
