#!/usr/bin/env python3

from pybleno import Characteristic
import gzip
import json
import logging
import threading

logger = logging.getLogger(__name__)


def deep_update(source, overrides):
    for key, value in overrides.items():
        if isinstance(value, dict) and value:
            returned = deep_update(source.get(key, {}), value)
            source[key] = returned
        else:
            source[key] = overrides[key]
    return source


class IoMBianConfigValuesCharacteristic(Characteristic):

    def __init__(self, iombian_config):
        Characteristic.__init__(self, {
            'uuid': 'ec0F',
            'properties': ['write'],
            'value': None
          })

        self.iombian_config = iombian_config
        self.iombian_config.on("start", self.on_start)
        self.iombian_config.on("error", self.on_error)
        self.iombian_config.on("done", self.on_done)
        self.num_messages = 0
        self.processed_num_messages = 0
        self.config = {}
        self.config_timeout_timer = None

    def on_start(self):
        logger.debug("on_start has been called")
        self.num_messages = self.iombian_config.num_messages

    def on_error(self):
        logger.debug("on_error has been called")
        self.num_messages = 0
        self.processed_num_messages = 0
        self.config = {}
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
            self.config_timeout_timer = None

    def on_done(self):
        logger.debug("on_done has been called")
        self.num_messages = 0
        self.processed_num_messages = 0
        self.config = {}
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
            self.config_timeout_timer = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if self.num_messages == 0:
            logger.error("The configuration process has not been started, please, check the protocol")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            return
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
        self.config_timeout_timer = threading.Timer(4.0, self.iombian_config.cancel_config_process)
        self.config_timeout_timer.start()
        try:
            data_decompressed = gzip.decompress(data)
            data_string = data_decompressed.decode()
            config = json.loads(data_string)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError, OSError) as e:
            logger.error(f"A non valid compressed JSON string has been received: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            self.iombian_config.cancel_config_process()
            return
        self.config = deep_update(self.config, config)
        self.processed_num_messages += 1
        if int(self.processed_num_messages) == int(self.num_messages):
            logger.debug("All expected messages has been received")
            if self.config_timeout_timer:
                self.config_timeout_timer.cancel()
            self.iombian_config.finish_config_process(self.config)
        callback(Characteristic.RESULT_SUCCESS)