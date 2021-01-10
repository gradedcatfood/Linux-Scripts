#!/usr/bin/python3

import pyudev
import subprocess

def main():
    context = pyudev.Context()
    monitor = pyudev.Monitor.from_netlink(context)
    monitor.filter_by(subsystem='usb')
    monitor.start()

    for device in iter(monitor.poll, None):
        # I can add more logic here, to run different scripts for different devices.
        # subprocess.call(['/home/foo/foobar.sh', '--foo', '--bar'])
        get_devices = 'xinput list|grep -w "SteelSeries SteelSeries Rival 310 eSports Mouse"'
        result = subprocess.run(get_devices, stdout=subprocess.PIPE, shell=True)

        string_result = result.stdout.decode("utf-8").encode("ascii", "ignore")

        lines = string_result.splitlines()

        id = False
        need_to_fix = False
        for line in lines:
            parts = line.decode("utf-8").split('\t')

            device_name = parts[0].strip()

            if device_name == 'SteelSeries SteelSeries Rival 310 eSports Mouse':
                id = parts[1].split('=')[1]
                break

        if id:
            get_props = f"xinput list-props {id}"
            result = subprocess.run(get_props, stdout=subprocess.PIPE, shell=True)
            string_result = result.stdout.decode("utf-8").encode("ascii", "ignore")
            lines = string_result.splitlines()

            for line in lines:
                props = line.decode("utf-8").split('\t')

                if len(props) > 1:
                    if props[1] == "libinput Accel Speed (309):":
                        if props[2] != "-0.600000":
                            need_to_fix = True
                            break
        
        if need_to_fix and id:
            command = f'xinput set-prop {id} "libinput Accel Speed" -0.6'
            subprocess.run(command, stdout=subprocess.PIPE, shell=True)
            print('Fixed')       

if __name__ == '__main__':
    main()
