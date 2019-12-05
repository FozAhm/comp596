#!/bin/bash
git clone https://github.com/FozAhm/comp596.git /home/ubuntu/comp596
sudo chown -R ubuntu:ubuntu /home/ubuntu/comp596/
chmod u+x /home/ubuntu/comp596/project/update_script.sh
sudo -u ubuntu /bin/bash /home/ubuntu/comp596/project/update_script.sh