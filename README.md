# Macs-Pruning-and-Ping

This script automates the process of connecting to two Huawei devices. Firstly, it prompts the user to provide the IP address and interface of the source device. Then, it establishes an SSH connection to the device and retrieves the MAC addresses associated with the specified interface. The script filters out the MAC addresses with the correct format of XXXX-XXXX-XXXX and eliminates duplicates, saving them in a set for further use.

Afterward, the script prompts the user to provide the IP address of the destination device. It connects to this device via SSH and retrieves the dynamic ARP entries that correspond to the previously extracted MAC addresses. The script then extracts the IP addresses and VRF for each MAC address and saves the corresponding ping commands to a file named 'pings.txt'. To prevent duplication, the script checks the file for existing ping commands before adding new ones.

**Note:** Here's an example of how the script would look when running it in the terminal:

* Enter the IP address of the source device.
* Enter the interface connected to the MAC addresses you want to retrieve.
* The script will display the number of MAC addresses found on the specified interface.
* Enter the IP address of the destination device to retrieve the associated IP addresses and VRFs.

```js
Please write the IP of the source device: 10.72.180.97
Please enter the interface to retrieve MAC addresses: 50|100GE8/1/0
Found 648 MAC addresses
Please write the IP of the destination device: 10.87.190.22
```
Ping commands saved to pings.txt.

## Walkthrough:

First write your username and password for the devices 1 and 2:
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
device2 = {
    'device_type': 'huawei',
    'ip': input("Please write the IP of the destination device: "),
    'username': 'X', #USERNAME
    'password': 'X', #PASSWORD
    'session_log': 'ssh_device2.log',
}
```
Know the links you want to retrive the MACs, and the specific interfaces:
```js
interface = input("Please enter the interface to retrieve MAC addresses for (or leave empty to retrieve for all interfaces): ")
```

We define the commands to sent to the first device, which will be:
```js
commands1 = [
    'screen-length 0 temporary',
    f'display Mac-address dynamic interface {interface}',
]
```
We set the first SSH connection, and save the MAC addresses extracted in a set().
```js
# Open an SSH connection to the first Huawei device
with ConnectHandler(**device1) as ssh1:

    # Execute the first two commands and capture the output
    for command in commands1:
        output = ssh1.send_command(command)

    # Extract the MAC addresses with the format of XXXX-XXXX-XXXX
    mac_addresses = set()
    mac_count = 0
    for line in output.split('\n'):
        if '-' in line:
            mac = line.split()[0]
            if len(mac) == 14 and mac.count('-') == 2:
                mac_addresses.add(mac)
                mac_count += 1

    print(f"Found {mac_count} MAC addresses"
```
Then the second SSH connection, which sent every MAC extracted in the command (display arp dynnamic | inc {mac}), and parse the output to extract the IP and VRF associated.
```js
# Open an SSH connection to the second Huawei device
with ConnectHandler(**device2) as ssh2:
    max_length = ssh2.send_command('screen-length 0 temporary')

    # Execute the commands and capture the output
    for mac in mac_addresses:
        command = f'display arp dynamic | inc {mac}'
        output = ssh2.send_command(command , read_timeout=120)

        # Save the output to a file
        with open('output.txt', 'a+') as f:
            f.write("\n")
            f.write(output)
            f.seek(0)
            output = f.read()

        # Extract the IP addresses and VPN instances for all MAC addresses
        matches = re.findall(r'^(\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}).*?\s+(\S+)\s*$', output, flags=re.MULTILINE)

        # Print the results
        for match in matches:
            ip = match[0]
            vpn_instance = match[1]
            ping_command = f"ping -vpn-instance {vpn_instance} {ip}"

            # Check if the ping command already exists in the file
            with open('pings.txt', 'a+') as s:
                s.seek(0)
                if ping_command in s.read():
                    continue  # Skip this ping if it already exists in the file

                # Save the ping command to the file
                s.write(ping_command + '\n')
```

After that, the script saves the pings like this: ping -vpn-instance {vpn_instance} {ip}

## Pings:

**Note:** The pings.txt will have the commands ready to put on a excel for validation at the time of the maintenance window:
```js
ping -vpn-instance DSL_ACCESO 10.102.10.69
ping -vpn-instance INTERNET_GT_DEPTAL 10.82.216.33
ping -vpn-instance WALMART_INTERNET 10.174.187.103
ping -vpn-instance IP_PBX_ACCESO 10.72.249.228
ping -vpn-instance COOPEASRURAL 10.78.156.115
ping -vpn-instance DSL_ACCESO 10.102.133.69
```

## Requirements:

* netmiko==4.1.2
* re
* Python 3.11 =>
