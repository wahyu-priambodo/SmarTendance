import paho.mqtt.client as mqtt
import time

# Set your MQTT broker details
broker_url = "broker.emqx.io"  # Replace with your broker URL
broker_port = 1883  # Replace with your broker port
publish_topic = "SmarTendance/ESP32/AttendanceTest1"  # Replace with the topic you want to publish to
subscribe_topic = "SmarTendance/ESP32/AttendanceTest1/Response"  # Replace with the topic you want to subscribe for the reply
message_received = False

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT Broker")
    else:
        print(f"Connection failed with result code {rc}")

def on_message(client, userdata, msg):
    print(f"Received message on topic '{msg.topic}': {msg.payload.decode('utf-8')}")
    global message_received
    message_received = True

if __name__ == "__main__":
    # Create an MQTT client
    client = mqtt.Client()

    # Set callback functions
    client.on_connect = on_connect
    client.on_message = on_message

    # Connect to the broker
    client.connect(broker_url, broker_port, keepalive=60)

    # Start the MQTT loop in a non-blocking way
    client.loop_start()

    while True:
        # Publish a message to the specified topic
        message_to_publish = "11112222"
        client.publish(publish_topic, message_to_publish, qos=0)
        print(f"Published message '{message_to_publish}' to topic '{publish_topic}'")

        # Subscribe to the response topic
        client.subscribe(subscribe_topic, qos=0)
        print(f"Subscribed to topic '{subscribe_topic}' for reply")

        # Wait for a reply for up to 3 seconds
        timeout = time.time() + 10
        while time.time() < timeout: # and message_received == False
            time.sleep(1)  # Sleep for 1 second
            # Check if a subscribe message has been received in this PC

        if message_received == False:
            print("No response received within 10 seconds")
        else:
            message_received = False
            
        # Unsubscribe from the response topic
        client.unsubscribe(subscribe_topic)
        print(f"Unsubscribed from topic '{subscribe_topic}'")
