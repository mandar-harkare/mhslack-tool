#!/bin/sh
dir='/usr/local/bin/.mhslack'
# Install python
sudo apt-get update
# sudo apt-get install software-properties-common
# sudo add-apt-repository ppa:deadsnakes/ppa
# sudo apt-get update
sudo apt-get install python3.8
sudo apt-get install python3-pip
pip3 --version
pip3 install -r requirements.txt
[ -d $dir ] || sudo mkdir $dir
sudo cp ./tool/mhslack* $dir/
sudo chmod 0744 $dir/mhslack.*
sudo chmod +x $dir/mhslack.*
# mhslack >/dev/null 2>&1 || 
echo "alias mhslack='/usr/local/bin/.mhslack/mhslack.py'" >> ~/.bashrc
. ~/.bashrc