# macs-pruning-and-ping

This script automates the process of connecting to two Huawei devices. Firstly, it prompts the user to provide the IP address and interface of the source device. Then, it establishes an SSH connection to the device and retrieves the MAC addresses associated with the specified interface. The script filters out the MAC addresses with the correct format of XXXX-XXXX-XXXX and eliminates duplicates, saving them in a set for further use.

Afterward, the script prompts the user to provide the IP address of the destination device. It connects to this device via SSH and retrieves the dynamic ARP entries that correspond to the previously extracted MAC addresses. The script then extracts the IP addresses and VRF for each MAC address and saves the corresponding ping commands to a file named 'pings.txt'. To prevent duplication, the script checks the file for existing ping commands before adding new ones.

**Note:** Here is a revised version of the final inputs prompt:

* Enter the IP address of the source device.
* Enter the interface connected to the MAC addresses you want to retrieve. If you leave this field blank, the script will retrieve MAC addresses for all interfaces.
* The script will display the number of MAC addresses found on the specified interface(s).
* Enter the IP address of the destination device to retrieve the associated IP addresses and VPN instances.

```js
Please write the IP of the source device: 10.72.180.97
Please enter the interface to retrieve MAC addresses for (or leave empty to retrieve for all interfaces): 50|100GE8/1/0
Found 648 MAC addresses
Please write the IP of the destination device: 10.87.190.22
```

**Note:**  The script will prompt you for the source and destination device, also for the specified interface of the source device:

**Note:** Please write your username and password for the devices 1 and 2:
```js
device1 = {
    'device_type': 'huawei',
    'ip': input("Please write the IP of the source device: "),
    'username': 'X', #USERNAME
    'password': 'X', #PASSWORD
    'session_log': 'ssh_device1.log',
}
```
```js
interface = input("Please provide the interface for the source device: ")
```
```js
device2 = {
    'device_type': 'huawei',
    'ip': input("Please write the IP of the destination device: "),
    'username': 'X', #USERNAME
    'password': 'X', #PASSWORD
    'session_log': 'ssh_device2.log',
}
```
Once you have entered all the information, the script will generate a router configuration using Jinja2 templates in a .txt file, which you can then use this configuration to set up eBGP on your router, or even send this info directly to your router.
To change the .txt file just rename it in here:
```js
with open('BGP-PEER-CONFIG-XXX.txt', 'a') as f: #save the output in a txt file
        with redirect_stdout(f):
            print(output)
```

If you want to customize the eBGP template, you can edit the template file 'bgp_huawei_template.j2' before running the script. 

## Output

The output for the script that ran in the first note:


## Requirements

* netmiko==4.1.2
* re
* Python 3.11 =>
