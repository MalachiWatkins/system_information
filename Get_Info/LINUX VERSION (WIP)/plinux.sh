#!/bin/bash
echo "Alias sourced"
echo "Run Install In terminal to install all pakages and update"
alias install="
sudo bash -c 'apt-get update' ;
sudo bash -c 'apt install software-properties-common'  ;
sudo bash -c  'add-apt-repository ppa:deadsnakes/ppa' ;
sudo bash -c 'apt install python3.9' ;
sudo bash -c 'dpkg --add-architecture i386' ;
sudo bash -c 'apt install python3-pip';
sudo bash -c 'python3 getinfo.py';
"
