#!/usr/bin/env python3

import logging
import os
import signal

from communication_module import CommunicationModule
from iombian_bluetooth_configurator_handler import IoMBianBluetoothConfiguratorHandler

LOG_LEVEL = os.environ.get("LOG_LEVEL", logging.INFO)
CONFIG_HOST = os.environ.get("CONFIG_HOST", "127.0.0.1")
CONFIG_PORT = int(os.environ.get("CONFIG_PORT", 5555))

logging.basicConfig(
    format='%(asctime)s %(levelname)-8s - %(name)-16s - %(message)s', level=LOG_LEVEL)
logger = logging.getLogger(__name__)


def signal_handler(sig, frame):
    logger.info("Stopping IoMBian Bluetooth Configurator Service")
    bluetooth_configurator_handler.stop()
    comm_module.stop()


if __name__ == "__main__":
    logger.info("Starting IoMBian Bluetooth Configurator Service")

    comm_module = CommunicationModule(host=CONFIG_HOST, port=CONFIG_PORT)
    comm_module.start()

    bluetooth_configurator_handler = IoMBianBluetoothConfiguratorHandler(
        comm_module)
    bluetooth_configurator_handler.start()

    signal.signal(signal.SIGINT, signal_handler)
    signal.signal(signal.SIGTERM, signal_handler)
    signal.pause()
