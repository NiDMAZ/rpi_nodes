#!/usr/bin/python
import json
import Adafruit_DHT as dht
import datetime
import logging
import threading
import pickle
from rw_lock import RWLock

logger = logging.getLogger(__name__)

class TemperatureReader(object):
    def __init__(self):
        # TODO: PUT SOME CHECKS IN PLACE, RIGHT NOW I AM GOING TO ASSUME THIS FILE EXISTS
        with open('/etc/rpi_node/rpi_node.json', 'r') as f:
            js_conf = json.load(f)
        
        tmp_cfg = js_conf.get('temperature_reader')

        self.node_name = tmp_cfg.get('node_name', "UNKNOWN")
        self.node_number = tmp_cfg.get('node_number', 999)
        self.polling = tmp_cfg.get('polling_time', 30) # IN SECONDS
        self.gpio_pin = tmp_cfg.get('dht_gpio_port', 4) # GPIO pin the data feed is connected to
        self.dht_model = tmp_cfg.get('dht_model', 22) # Model number of DHT sensor
        self.next_runtime = datetime.datetime.now()
        self.cache = {}
        self._current = {}
        self.stop_event = threading.Event() # Will use this to shutdown the child threads
        self._thread_pool = []

        logger.info('Initialized Node: [{nm}], NodeNumber: [{nn}] PollingTime: [{pt}] DHTModel: [{md}] GPIOPin: [{gpin}]'.format(
                                                            nm=self.node_name,
                                                            nn=self.node_number,
                                                            pt=self.polling,
                                                            md=self.dht_model,
                                                            gpin=self.gpio_pin))

    def c2f(self, val):
        return (val * 9/5) + 32

    def check_temp(self):
        try:
            humidity, temperature = dht.read_retry(self.dht_model, self.gpio_pin)
            temperature = self.c2f(temperature)
            dt_now = datetime.datetime.now()
            self.cache[dt_now] = {'humidity': humidity, 'temperature': temperature}
            logger.info('Cached Updated complete')
        except Exception as e:
            logger.exception(e)
        finally:
            self._current = {'node_name': self.node_name,
                    'node_number': self.node_number,
                    'time': dt_now.strftime('%Y-%m-%d %H:%M:%S'),
                    'humidity': humidity,
                    'temperature': temperature,
                    'polling_time': self.polling}
            logger.info(self._current)

    def _update_cache(self):
        while True:
            if not self.stop_event.isSet() and datetime.datetime.now() >= self.next_runtime:
                logger.info('Updating Cache...')
                self.check_temp()
                self.next_runtime = datetime.datetime.now() + datetime.timedelta(seconds=self.polling)
                logger.info('Cache will update at: {}'.format(self.next_runtime))

    def run(self):
        try:
            update_cache_thread = threading.Thread(target=self._update_cache, name='Node_{}_UpdateThread'.format(self.node_name))
            update_cache_thread.setDaemon = True
            self._thread_pool.append(update_cache_thread)
            update_cache_thread.start()

        except KeyboardInterrupt:
            self._shutdown()

    def get_current(self):
        return self._current

    def get_historical(self, start_dt=None, end_dt=None):
        # TODO ADD THE ABILITY TO PASS A DATETIME RANGE
        if start_dt is None and end_dt is None:
            return self.cache

    def _shutdown(self):
        self._stop_event.set()
        for src in self._thread_pool:
            if src.isAlive():
                logger.info('Terminating thread: {}'.format(src))
                src.join(1)

TempReader = TemperatureReader()
TempReader.run()
