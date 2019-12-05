#!/bin/bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y
sudo apt install -y python3-pip
pip3 install awscli --upgrade --user
export PATH=$PATH:/home/ubuntu/.local/bin >> ~/.profile
source ~/.profile
pip3 install networkx
pip3 install matplotlib
ssh-keygen -t rsa -b 4096 -q -N "" -f /home/ubuntu/.ssh/id_rsa
aws s3 cp s3://comp-596-graph/github.gml /home/ubuntu/comp596/project/github.gml
#cat .ssh/id_rsa.pub
sudo reboot
