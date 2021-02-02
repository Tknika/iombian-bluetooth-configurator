# IoMBian Bluetooth Configurator

This service allows to configure the IoMBian device using Bluetooth Low Energy (BLE).


## Installation

- Clone the repo into a temp folder:

> ```git clone https://github.com/Tknika/iombian-bluetooth-configurator.git /tmp/iombian-bluetooth-configurator && cd /tmp/iombian-bluetooth-configurator```

- Create the installation folder and move the appropiate files (edit the user):

> ```sudo mkdir /opt/iombian-bluetooth-configurator```

> ```sudo cp requirements.txt /opt/iombian-bluetooth-configurator```

> ```sudo cp -r src/* /opt/iombian-bluetooth-configurator```

> ```sudo cp systemd/iombian-bluetooth-configurator.service /etc/systemd/system/```

> ```sudo chown -R iompi:iompi /opt/iombian-bluetooth-configurator```

- Create the virtual environment and install the dependencies:

> ```cd /opt/iombian-bluetooth-configurator```

> ```sudo apt install -y python3-venv python3-dev libbluetooth-dev libudev-dev```

> ```python3 -m venv venv```

> ```source venv/bin/activate```

> ```pip install --upgrade pip```

> ```pip install -r requirements.txt```

- Start the script

> ```sudo systemctl enable iombian-bluetooth-configurator.service && sudo systemctl start iombian-bluetooth-configurator.service```

## Author

(c) 2021 [Aitor Iturrioz Rodríguez](https://github.com/bodiroga)

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.