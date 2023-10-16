#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>
#include "secrets.h"

unsigned long lastMillis = 0;
unsigned long previousMillis = 0;
const long interval = 5000;
bool isNTPConnect = false;

#define AWS_IOT_PUBLISH_TOPIC "awsiot/pub"
#define AWS_IOT_SUBSCRIBE_TOPIC "awsiot/sub"

WiFiClientSecure net;

// Credentials for AWS IoT
BearSSL::X509List cert(root_ca);
BearSSL::X509List client_crt(client_cert);
BearSSL::PrivateKey key(private_key);

PubSubClient client(net);

time_t now;
time_t nowish = 1510592825;

void NTPConnect(void)
{
  Serial.print("Setting time using SNTP");
  configTime(TIME_ZONE * 3600, 0, "pool.ntp.org", "time.nist.gov");
  now = time(nullptr);
  while (now < nowish)
  {
    delay(500);
    Serial.print(".");
    now = time(nullptr);
  }
  Serial.println("done!");
  struct tm timeinfo;
  if (!getLocalTime(&timeinfo))
  {
    Serial.print("Failed to obtain time");
  }
  Serial.print("Current time: ");
  Serial.print(asctime(&timeinfo));

  isNTPConnect = true;
}

void messageReceived(char *topic, byte *payload, unsigned int length)
{
  Serial.print("Received [");
  Serial.print(topic);
  Serial.print("]: ");
  for (int i = 0; i < length; i++)
  {
    Serial.print((char)payload[i]);
  }
  Serial.println();
}

void connectAWS()
{
  delay(3000);

  // Setting up WiFi connection
  WiFi.mode(WIFI_STA);
  WiFi.begin(WIFI_SSID, WIFI_PASSWORD);

  Serial.print(String("Attempting to connect to SSID: ") + String(WIFI_SSID));

  while (WiFi.status() != WL_CONNECTED)
  {
    Serial.print(".");
    delay(1000);
  }

  Serial.println("Connected");

  // Set time via NTP, as required for x.509 validation
  if (!isNTPConnect)
    NTPConnect();

  // Setting up certification key
  net.setTrustAnchors(&cert);
  net.setClientRSACert(&client_crt, &key);

  // Setting up connection to AWS MQTT
  client.setServer(MQTT_endpoint, 8883);
  client.setCallback(messageReceived);

  // Connecting to AWS MQTT
  Serial.println("Connecting to AWS IOT");

  while (!client.connect(THINGNAME))
  {
    Serial.print(".");
    delay(1000);
  }

  if (!client.connected())
  {
    Serial.println("AWS IoT Timeout!");
    return;
  }

  // Subscribe to a topic
  client.subscribe(AWS_IOT_SUBSCRIBE_TOPIC);

  Serial.println("AWS IoT Connected!");
}

void publishMessage(const char rfid_number[])
{
  StaticJsonDocument<200> doc;
  doc["time"] = millis();
  doc["rfid"] = rfid_number;
  char jsonBuffer[512];
  serializeJson(doc, jsonBuffer); // print to client

  client.publish(AWS_IOT_PUBLISH_TOPIC, jsonBuffer);
}

void setup()
{
  Serial.begin(115200);
  connectAWS();
}

void loop()
{
  {
    const char rfid_number[] = "1234567890";
    struct tm timeinfo;
    if (!getLocalTime(&timeinfo))
    {
      Serial.print("Failed to obtain time");
    }
    Serial.print("Current time: ");
    Serial.print(asctime(&timeinfo));

    char h[] = "Hello from ESP8266";

    Serial.print(F("Humidity: "));
    Serial.println(h);
    delay(3000);

    if (!client.connected())
    {
      connectAWS();
    }
    else
    {
      client.loop();
      if (millis() - lastMillis > 5000)
      {
        lastMillis = millis();
        publishMessage(rfid_number);
        exit(0);
      }
    }
  }
}