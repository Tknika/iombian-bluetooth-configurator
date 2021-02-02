#!/usr/bin/env python3

from pybleno.hci_socket import Emit
import logging

logger = logging.getLogger(__name__)


class IoMBianConfig():

    def __init__(self, callback):
        self.callback = callback
        self.num_params = 0

    def start_config_process(self, num_params):
        logger.info(f"Configuration process has started ({num_params} parameters)")
        self.num_params = num_params
        self.emit("start", [])

    def finish_config_process(self, config):
        # Check if config contains 'num_params' keys
        num_keys = len(config.keys())
        if num_keys != self.num_params:
            logger.error(f"The received 'config' doesn't match the expected number of parameters ({num_keys}/{self.num_params})")
            return
        logger.info("Configuration process has finished")
        self.num_params = 0
        self.emit("done", [])
        self.callback(config)

    def cancel_config_process(self):
        logger.warn("Configuration process has been cancelled")
        self.num_params = 0
        self.emit("error", [])

Emit.Patch(IoMBianConfig)