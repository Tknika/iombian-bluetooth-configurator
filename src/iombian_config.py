#!/usr/bin/env python3

from pybleno.hci_socket import Emit
import logging

logger = logging.getLogger(__name__)


class IoMBianConfig():

    def __init__(self, callback):
        self.callback = callback
        self.num_messages = 0

    def start_config_process(self, num_messages):
        logger.info(f"Configuration process has started ({num_messages} messages)")
        self.num_messages = num_messages
        self.emit("start", [])

    def finish_config_process(self, config):
        logger.info("Configuration process has finished")
        self.num_messages = 0
        self.emit("done", [])
        self.callback(config)

    def cancel_config_process(self):
        logger.warn("Configuration process has been cancelled")
        self.num_messages = 0
        self.emit("error", [])

Emit.Patch(IoMBianConfig)