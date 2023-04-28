from netmiko import ConnectHandler
import re

# Define the SSH connection parameters for the first Huawei device
device1 = {
    'device_type': 'huawei',
    'ip': input("Please write the IP of the source device: "),
    'username': 'X', #USERNAME
    'password': 'X', #PASSWORD
    'session_log': 'ssh_device1.log',
}

interface = input("Please enter the interface to retrieve MAC addresses: ")

# Define the commands to execute on the first device
commands1 = [
    'screen-length 0 temporary',
    f'display Mac-address dynamic interface {interface}',
]

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

    print(f"Found {mac_count} MAC addresses")

# Define the SSH connection parameters for the second Huawei device
device2 = {
    'device_type': 'huawei',
    'ip': input("Please write the IP of the destination device: "),
    'username': 'X', #USERNAME
    'password': 'X', #PASSWORD
    'session_log': 'ssh_device2.log',
}

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
