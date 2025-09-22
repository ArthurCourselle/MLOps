from kafka import KafkaConsumer, KafkaProducer
import json
import numpy as np

consumer = KafkaConsumer("courselle", bootstrap_servers=["nowledgeable.com:9092"])
producer = KafkaProducer(bootstrap_servers="nowledgeable.com:9092")

for message in consumer:

    json_data = json.loads(message.value.decode("utf-8"))
    data_array = np.array(json_data["data"])

    sum_result = np.sum(data_array)

    result_message = {
        "original_data": json_data["data"],
        "sum_result": float(sum_result),
    }

    json_result = json.dumps(result_message).encode("utf-8")
    producer.send("processed", json_result)
    producer.flush()

    print(f"Sum : {sum_result}")

producer.close()
