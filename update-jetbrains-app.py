#!/usr/bin/python3

import subprocess
import urllib.request
import tarfile
import os
import sys

def main():

    name = sys.argv[1].lower()

    try:
        eap = sys.argv[2]
    except IndexError:
        eap = None

    code = get_code(name)

    if eap:
        print('!!!FETCHING EAP!!!')
        name = name + '-eap'


    file_name = 'upgrade-' + name + '.tar.gz'
   
    print('Downloading ' + name + '....')

    if eap:
        url = 'https://data.services.jetbrains.com/products/download?code=' + code + '&platform=linux&type=eap'
    else:
        url = 'https://data.services.jetbrains.com/products/download?code=' + code + '&platform=linux'

    # EAP Version
    path = '/home/mmillis/Downloads/' + file_name
    urllib.request.urlretrieve(url, path)

    print('Unzipping File....')
    archive = tarfile.open('/home/mmillis/Downloads/' + file_name)

    # dir_name = os.path.commonprefix(archive.getnames())[:-1]
    dir_name = os.path.commonprefix(archive.getnames())

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
    elif name == 'pycharm':
        code = 'PC'
    elif name == 'webstorm':
        code = 'WS'
    else:
        exit('unkown app name')

    return code

if __name__ == '__main__':
    if(os.geteuid() != 0):
        exit('Need to be root')

    if len(sys.argv) < 2:
        exit('Need to pass in app name')

    main()

