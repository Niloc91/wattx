#!/usr/bin/env python
import threading, logging, time
import json
from kafka import KafkaConsumer, KafkaProducer
import requests
import math

#Scrape ranking
def scapeRanking():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    limit = 100
    num_pages = math.ceil(limit/100)
    rankingTable = []
    for i in range(0, num_pages):

        response = requests.get('https://min-api.cryptocompare.com/data/top/mktcapfull?limit=100&tsym=USD&page='+str(i)+'&api_key=81ac4735d8ae77744d5f68b89aad0df9925188443819bd529f3e160c8ac75f74')
        rankingData = response.json()['Data']


        for x in rankingData:
            rankingTable.append(x['CoinInfo']['Name'])

    print("Entries added:"+str(len(rankingTable)))
    print(json.dumps(rankingTable))

    producer.send('ranking', json.dumps(rankingTable).encode('utf-8'))
    producer.close()



def main():
    while True:
        scapeRanking()
        time.sleep(10)
        print("sending....")


enable_logging=False
if __name__ == "__main__":

    if enable_logging :
        logging.basicConfig(
            format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
            level=logging.INFO
        )

    main()