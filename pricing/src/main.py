#!/usr/bin/env python
import threading, logging, time
import multiprocessing

from kafka import KafkaConsumer, KafkaProducer


class Producer(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.stop_event = threading.Event()

    def stop(self):
        self.stop_event.set()

    def run(self):
        producer = KafkaProducer(bootstrap_servers='localhost:9092')

        while not self.stop_event.is_set():
            print "sending...."
            producer.send('Topic1', b"test")
            producer.send('Topic1', b"\xc2Hola, mundo!")
            time.sleep(1)


        producer.close()


def scapePrice():
    producer = KafkaProducer(bootstrap_servers='localhost:9092')

    producer.send('Topic1', b"test")

    producer.close()



def main():
    tasks = [
        Producer()
    ]

    for t in tasks:
        t.start()

    time.sleep(10)

    for task in tasks:
        task.stop()

    for task in tasks:
        task.join()


if __name__ == "__main__":
    logging.basicConfig(
        format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
        level=logging.INFO
    )
    main()