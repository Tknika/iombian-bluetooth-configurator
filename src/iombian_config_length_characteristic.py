#!/usr/bin/env python3

from pybleno import Characteristic
import logging

logger = logging.getLogger(__name__)


class IoMBianConfigLengthCharacteristic(Characteristic):

    def __init__(self, iombian_config):
        Characteristic.__init__(self, {
            'uuid': 'ec0D',
            'properties': ['write'],
            'value': None
          })
        self.iombian_config = iombian_config

    def onWriteRequest(self, data, offset, withoutResponse, callback):
        try:
            data_string = str(data, 'utf-8')
            data_int = int(data_string)
        except (ValueError, UnicodeDecodeError) as e:
            logger.error(f"A non valid value has been received (it should be an integer): {e}")
            callback(Characteristic.RESULT_UNLIKELY_ERROR)
            return
        callback(Characteristic.RESULT_SUCCESS)
        self.iombian_config.start_config_process(data_int)