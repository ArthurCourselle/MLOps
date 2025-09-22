from kafka import KafkaProducer
import json

message = {"data": [[1, 2], [3, 4]]}

producer = KafkaProducer(bootstrap_servers="nowledgeable.com:9092")
json_message = json.dumps(message).encode("utf-8")
producer.send("courselle", json_message)
producer.flush()
producer.close()
