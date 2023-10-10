#include <ESP8266WiFi.h>
#include <WiFiClientSecure.h>
#include <PubSubClient.h>
#include <ArduinoJson.h>
#include <time.h>

#include "secrets.h"

#define AWS_IOT_PUBLISH_TOPIC "awsiot/test"
#define AWS_IOT_SUBSCRIBE_TOPIC "awsiot/test"
