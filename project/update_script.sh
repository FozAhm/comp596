#!/bin/bash
sudo apt update
sudo DEBIAN_FRONTEND=noninteractive apt upgrade -y
sudo apt install -y python3-pip
pip3 install awscli --upgrade --user
export PATH=$PATH:/home/ubuntu/.local/bin >> ~/.profile
source ~/.profile
pip3 install networkx
pip3 install matplotlib
pip3 install numpy
pip3 install scipy
pip3 install powerlaw
ssh-keygen -t rsa -b 4096 -q -N "" -f /home/ubuntu/.ssh/id_rsa
aws s3 cp s3://comp-596-graph/github.gpickle /home/ubuntu/comp596/project/github.gpickle
aws s3 cp s3://comp-596-graph/github_gcp.gpickle /home/ubuntu/comp596/project/github_gcp.gpickle
#cat .ssh/id_rsa.pub
sudo reboot
