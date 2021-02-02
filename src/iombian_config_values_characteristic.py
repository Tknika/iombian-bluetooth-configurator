#!/usr/bin/env python3

from pybleno import Characteristic
import json
import logging
import threading

logger = logging.getLogger(__name__)


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
        self.num_params = 0
        self.processed_num_params = 0
        self.config = {}
        self.config_timeout_timer = None

    def on_start(self):
        logger.debug("on_start has been called")
        self.num_params = self.iombian_config.num_params

    def on_error(self):
        logger.debug("on_error has been called")
        self.num_params = 0
        self.processed_num_params = 0
        self.config = {}
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
            self.config_timeout_timer = None

    def on_done(self):
        logger.debug("on_done has been called")
        self.num_params = 0
        self.processed_num_params = 0
        self.config = {}
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
            self.config_timeout_timer = None

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        if self.num_params == 0:
            logger.error("The configuration process has not been started, please, check the protocol")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            return
        if self.config_timeout_timer:
            self.config_timeout_timer.cancel()
        self.config_timeout_timer = threading.Timer(4.0, self.iombian_config.cancel_config_process)
        self.config_timeout_timer.start()
        try:
            data_string = str(data, 'utf-8')
            config = json.loads(data_string)
        except (UnicodeDecodeError, json.decoder.JSONDecodeError) as e:
            logger.error(f"A non valid JSON string has been received: {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            self.iombian_config.cancel_config_process()
            return
        self.config.update(config)
        self.processed_num_params += 1
        if int(self.processed_num_params) == int(self.num_params):
            logger.debug("All expected parameters has been received")
            if self.config_timeout_timer:
                self.config_timeout_timer.cancel()
            self.iombian_config.finish_config_process(self.config)
        callback(Characteristic.RESULT_SUCCESS)