import logging
from threading import Thread
import time

__author__ = 'Ruslan'
from Queue import Queue


class Timer(Thread):
    def __init__(self, list_callbacks):
        super(Timer, self).__init__()
        self.list_events = list_callbacks
        self.activated_events = Queue()
        self.daemon = True

    def run(self):
        while 1:
            for event in self.list_events:
                if event.get('time', None) is None:
                    if __debug__:
                        raise ValueError("Time is None rly?")
                    else:
                        logging.warning("Event w'll never use: " + event.get('callback'))
                        continue

                if event['time'] <= time.time():
                    self.activated_events.put(event.get('callback'), timeout=1)
                    self.list_events.remove(event)
            time.sleep(1)