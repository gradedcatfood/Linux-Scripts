#!/bin/bash -e
# IMPORTANT. My phpstom installation exists on /opt/phpstorm.
# Early Access program: https://confluence.jetbrains.com/display/PhpStorm/PhpStorm+Early+Access+Program
# For stable releases try: https://data.services.jetbrains.com/products/download?code=PS&platform=linux

if [ "$(whoami)" != "root" ]
then
  echo "Sorry, you are not root."
  exit 1
fi

echo -n "Please enter the PhpStorm download url (eg http://download.jetbrains.com/webide/PhpStorm-EAP-141.690.tar.gz): "
read url
 
# Download file from url
echo "Downloading PhpStorm to ~/Desktop"
cd /home/mmillis/Downloads
wget ${url} --no-check-certificate
tar -xzf /home/mmillis/Downloads/PhpStorm* -C /opt
# tar -xzf /home/mmillis/Downloads/PhpStorm*
rm /home/mmillis/Downloads/PhpStorm*.tar.gz

# Remove old Phpstorm
echo "Removing old PhpStorm"
sudo rm -rf /usr/local/bin/phpstorm

# Copy new Phpstorm
echo "Copying new PhpStorm"
mv ~/Desktop/PhpStorm* /opt/phpstorm

# Finish
echo "New PhpStorm has been installed!"