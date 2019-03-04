from flask import Flask
from kafka import KafkaConsumer
import threading
import time
import json
import logging
import os
app = Flask(__name__)

def latestPrices():
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                             auto_offset_reset='latest',
                             enable_auto_commit=False,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe(['rankingwithprice'])

    data = []
    for message in consumer:
        print (message.value)
        data = message.value

    return data

pricing = threading.Thread(target=latestPrices)
pricing.start()
latestData = pricing.join()


@app.route('/')
def pricelist():
    return latestData

if __name__ == '__main__':

    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:' +
               '%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    app.run()
