from confluent_kafka import Producer

kafka_producer_config = {
    'bootstrap.servers': 'localhost:9092',
    'group.id': 'mygroup',
    'auto.offset.reset': 'earliest'
}
producer = Producer(kafka_producer_config)
