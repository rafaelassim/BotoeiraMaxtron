#!/bin/bash

cp botoeira.service /etc/systemd/system

apt-get install -y python3-pyudev
apt-get install -y python3-serial

systemctl enable botoeira.service
systemctl start botoeira.service