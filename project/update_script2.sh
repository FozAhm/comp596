#!/bin/bash
/bin/su -c "git clone https://github.com/FozAhm/comp596.git /home/ubuntu/comp596" - ubutnu
/bin/su -c "chmod +x /home/ubuntu/comp596/project/update_script.sh" - ubuntu
/bin/su -c "/home/ubuntu/comp596/project/update_script.sh" - ubuntu