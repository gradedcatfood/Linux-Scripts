#!/usr/bin/python3

import subprocess
import urllib.request
import tarfile
import os
import sys

def main():

    name = sys.argv[1].lower()
    code = get_code(name)

    file_name = 'upgrade-' + name + '.tar.gz'
   
    print('Downloading ' + name + '....')

    url = 'https://data.services.jetbrains.com/products/download?code=' + code + '&platform=linux'
    path = '/home/mmillis/Downloads/' + file_name
    urllib.request.urlretrieve(url, path)

    proc = subprocess.Popen('sudo tar -xzf "/home/mmillis/Downloads/' + file_name + '" -C "/opt"')

    print('Unzipping File....')
    archive = tarfile.open('/home/mmillis/Downloads/' + file_name)

    dir_name = os.path.commonprefix(archive.getnames())[:-1]

    archive.extractall('/opt')
    archive.close()


    print("Linking to /usr/local/bin")
    subprocess.run('rm -rf /usr/local/bin/' + name, stdout=subprocess.PIPE, shell=True)
    subprocess.run('ln -s /opt/' + dir_name + '/bin/' + name + '.sh /usr/local/bin/' + name, stdout=subprocess.PIPE, shell=True)


    print('Cleaning Downloads Dir')
    subprocess.run('rm -f ' + path, stdout=subprocess.PIPE, shell=True)

def get_code(name):
    if name == 'phpstorm':
        code = 'PS'
    elif name == 'datagrip':
        code = 'DG'
    else:
        exit('unkown app name')

    return code

if __name__ == '__main__':
    if(os.geteuid() != 0):
        exit('Need to be root')

    if len(sys.argv) < 2:
        exit('Need to pass in app name')

    main()

