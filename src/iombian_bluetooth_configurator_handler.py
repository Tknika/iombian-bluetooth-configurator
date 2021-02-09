#!/usr/bin/env python3

import logging
import pybleno
import threading

from iombian_config import IoMBianConfig
from iombian_config_service import IoMBianConfigService

logger = logging.getLogger(__name__)


class IoMBianBluetoothConfiguratorHandler():

    DEFAULT_NAME = "iom2040"
    SAVE_CONFIG_DELAY = 2

    def __init__(self, file_config_handler, name=DEFAULT_NAME):
        self.file_config_handler = file_config_handler
        self.ble_config_handler = IoMBianConfig(self.on_config_complete)
        self.config_service = IoMBianConfigService(self.ble_config_handler)
        self.ble = None
        self.name = name

    def start(self):
        if self.file_config_handler.execute_command("is_configured"):
            logger.info("Device already configured, Bluetooth Configurator Handler will not be started")
            self.stop()
            return
        logger.debug("Starting Bluetooth Configurator Handler")
        self.name = self.file_config_handler.execute_command("get_device_id")
        self.ble = pybleno.Bleno()
        self.ble.on('stateChange', self.on_state_change)
        self.ble.on('advertisingStart', self.on_advertising_start)
        self.ble.start()

    def stop(self):
        logger.debug("Stopping Bluetooth Configurator Handler")
        if self.ble:
            self.ble.stopAdvertising()
            self.ble.disconnect()

    def on_config_complete(self, config):
        logger.info("Bluetooth Configuration Received!")
        threading.Timer(self.SAVE_CONFIG_DELAY, self.file_config_handler.execute_command, ["save_config", config]).start()

    def on_state_change(self, state):
        if (state == 'poweredOn'):
            self.ble.startAdvertising(self.name, [self.config_service.uuid])
        else:
            self.ble.stopAdvertising()

    def on_advertising_start(self, error):
        if error:
            logger.error(f"Advertising process could not be started: {error}")
        else:
            self.ble.setServices([self.config_service])