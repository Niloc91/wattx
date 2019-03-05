#!/usr/bin/env python
import threading, logging, time
import multiprocessing
import json
from kafka import KafkaConsumer, KafkaProducer
import requests
import operator

kafka_host="kafka:9092"

def pullLatestRanking():
    consumer = KafkaConsumer(bootstrap_servers=kafka_host,
                             auto_offset_reset='latest',
                             enable_auto_commit=False,
                             value_deserializer=lambda m: json.loads(m.decode('utf-8')))
    consumer.subscribe(['ranking'])

    #Pull prices
    response = requests.get("https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest?start=1&limit=1000&convert=USD&CMC_PRO_API_KEY=06e6d783-bec5-4cff-9da7-9fb99d977a0c")
    priceData = response.json()['data']
    priceTable = {}

    for x in priceData:
        priceTable[x['symbol']] = x['quote']['USD']['price']

    #Setup ranking table
    RankingTable = {}
    for message in consumer:
        for x in message.value:
            RankingTable[x] =  priceTable.get(x,-1)

        RankingTable =  sorted(RankingTable.items(), key=lambda kv: kv[1], reverse=True)
        #Send to kafka
        print(json.dumps(RankingTable))
        producer = KafkaProducer(bootstrap_servers=kafka_host)
        producer.send('rankingwithprice', json.dumps(RankingTable).encode('utf-8'))
        producer.close()




def main():
    while True:
        pullLatestRanking()
        time.sleep(100)
        print("sending....")


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()