#!/bin/bash
set -e


# How to use 
# sudo ./update-phpstorm.sh /home/mmillis/Downloads/PhpStorm-2020.3.tar.gz PhpStorm-203.5981.175

if [ "$EUID" -ne 0 ]
  then echo "Please run as root"
  exit
fi

if [ $# -eq 0 ]
  then
    echo "No arguments supplied"
    exit
fi

# url = "https://data.services.jetbrains.com/products/download?code=PS&platform=linux"
# cd /home/mmillis/Downloads
# wget ${url} --no-check-certificate

path=$1
path_without_extension=${1::-7}
inner_tar_name=$2

echo "Extracting $1"
tar -xzf "$path" -C /opt

# echo "Running phpstorm.sh"
# /opt/"$inner_tar_name"/bin/phpstorm.sh

echo "Linking to /usr/local/bin"
sudo rm -rf /usr/local/bin/phpstorm
sudo ln -s /opt/"$inner_tar_name"/bin/phpstorm.sh /usr/local/bin/phpstorm

echo 'Done!'