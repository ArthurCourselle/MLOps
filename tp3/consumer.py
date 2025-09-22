from kafka import KafkaConsumer

consumer = KafkaConsumer("processed", bootstrap_servers=["nowledgeable.com:9092"])

for message in consumer:
    print(message.value.decode("utf-8"))
