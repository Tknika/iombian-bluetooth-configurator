#!/usr/bin/env python3

from pybleno import BlenoPrimaryService
from iombian_config_length_characteristic import IoMBianConfigLengthCharacteristic
from iombian_config_values_characteristic import IoMBianConfigValuesCharacteristic


class IoMBianConfigService(BlenoPrimaryService):
    def __init__(self, iombian_config):
        BlenoPrimaryService.__init__(self, {
          'uuid': 'ec00',
          'characteristics': [
            IoMBianConfigLengthCharacteristic(iombian_config),
            IoMBianConfigValuesCharacteristic(iombian_config)
          ]})