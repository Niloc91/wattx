from flask import Flask, Response
from kafka import KafkaConsumer
import threading
import time
import json
import logging
import os
app = Flask(__name__)


kafka_host="kafka:9092"

@app.route('/test')
def test():
    return "HELLO"



@app.route('/')
def pricelist():
    consumer = KafkaConsumer(bootstrap_servers=kafka_host,
                             auto_offset_reset='earliest',
                             enable_auto_commit=False,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe(['rankingwithprice'])
    consumer.poll()
    for message in consumer:
        print (message.value)
        return json.dumps(message.value)





if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )

    app.run(host='0.0.0.0')




