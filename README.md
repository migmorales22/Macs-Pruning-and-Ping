# macs-pruning-and-ping

This script automates the process of configuring eBGP in Huawei devices using Jinja2 templates. It prompts the user for all necessary eBGP variables, such as AS numbers, peer IPs, and network prefixes, and then uses these inputs to generate a router configuration. By leveraging the power of Jinja2, the script allows for easy customization of eBGP templates and can be used to quickly and efficiently set up eBGP on multiple routers. Whether you are a network administrator or studying for your CCNP, this script is a valuable tool for automating eBGP configuration.

**Note:**  The script will prompt you for all the necessary eBGP variables:
```js
Enter the local ASN: 271812
Enter the name of the internet provider (COGENT-VERIZON): VERIZON
Enter the ipv4 address of the neighbor with underlines (1_1_1_1): 1_1_1_1
Enter the ipv6 address of the neighbor with underlines (2800_1_F_1): 2800_1_F_1
Enter the interface (100GE2/0/2): 100GE2/0/2
Enter the interface description: CP:100GB ! EBGP:VERIZON 1-800000001 | PEER:1.1.1.1
Enter the source ipv4 address and his mask (1.1.1.2 255.255.255.252): 1.1.1.2 255.255.255.252
Enter the source ipv6 address and his mask (2800:1:F::2/127): 2800:1:F::2/127
Enter the neighbor ipv4 address (1.1.1.1): 1.1.1.1
Enter the neighbor ipv6 address (2800:1:F::1): 2800:1:F::1
Enter the remote ASN: 701
Enter the description for the BGPv4 peer: VERIZON_100GB_100GE2/0/2
Enter the description for the BGPv6 peer: VERIZON_100GB_100GE2/0/2
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

```js
#
sys
#
#BEHAVIOR INBOUND.
#
traffic behavior BH_INTERNET_IPV4_NBR_1_1_1_1_IN
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
traffic behavior BH_INTERNET_IPV6_NBR_2800_1_F_1_IN
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
traffic behavior BH_INTERNET_CLIENTES_IPV6_NBR_2800_1_F_1_IN
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
#TRAFFIC-POLICY AND CLASSIFIER INBOUND.
#
traffic policy TP_INTERNET_VERIZON_NBR_1_1_1_1_IN
 share-mode
 statistics enable
 classifier CL_INTERNET_IPV4_IN behavior BH_INTERNET_IPV4_NBR_1_1_1_1_IN precedence 5
 classifier CL_INTERNET_IPV6_IN behavior BH_INTERNET_IPV6_NBR_2800_1_F_1_IN precedence 10
 classifier CL_INTERNET_CLIENTES_IPV6_IN behavior BH_INTERNET_CLIENTES_IPV6_NBR_2800_1_F_1_IN precedence 15
#
#BEHAVIOR OUTBOUND.
#
traffic behavior BH_INTERNET_IPV4_NBR_1_1_1_1_OUT
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
traffic behavior BH_INTERNET_PA_IPV6_NBR_2800_1_F_1_OUT
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
traffic behavior BH_INTERNET_CLIENTES_IPV6_NBR_2800_1_F_1_OUT
 car cir 98000000 pir 98000000 cbs 18700000 pbs 18700000 green pass yellow pass service-class af1 color green red discard color-aware
#
#TRAFFIC-POLICY AND CLASSIFIER OUTBOUND.
#
traffic policy TP_INTERNET_VERIZON_NBR_1_1_1_1_OUT
 share-mode
 statistics enable
 classifier CL_INTERNET_IPV4_OUT behavior BH_INTERNET_IPV4_NBR_1_1_1_1_OUT precedence 5
 classifier CL_INTERNET_IPV6_OUT behavior BH_INTERNET_IPV6_NBR_2800_1_F_1_OUT precedence 10
 classifier CL_INTERNET_CLIENTES_IPV6_OUT behavior BH_INTERNET_CLIENTES_IPV6_NBR_2800_1_F_1_OUT precedence 15
#
#INBOUND AND OUTBOUND FILTER FOR IPv4.
#
xpl route-filter XPL_VERIZON_SALIDA_1_1_1_1_100G
 if ip route-destination in INT_PFX_CLIENTES_1 then
  refuse
 elseif ip route-destination in INT_PFX_CLIENTES_2 then
  refuse
 elseif ip route-destination in INT_PFX_CLIENTES_3 then
  refuse
 elseif ip route-destination in INT_PFX_CLIENTES_4 then
  refuse
 elseif ip route-destination in INT_PFX_CLIENTES_5 then
  refuse
 elseif ip route-destination in INT_PFX_CLIENTES_6 then
  refuse
 else
  refuse
 endif
 end-filter
#
xpl route-filter policy_nbr_1_1_1_1_ipv4_unicast_in
 if (as-path in aspath_1_p1_deny and ip route-destination in pfx_RFC1918_p1_deny) then
  refuse
 elseif (as-path in aspath_1_p2_permit and ip route-destination in pfx_RFC1918_p2_permit) then
  approve
 endif
 end-filter
#
xpl route-filter policy_nbr_1_1_1_1_ipv4_unicast_out
 if (as-path in aspath_150 and ip route-destination in pfx_RFC1918_out_ebgp_p1_deny) then
  refuse
 elseif (as-path in aspath_150 and ip route-destination in pfx_RFC1918_out_ebgp_p2_permit) then
  call route-filter XPL_VERIZON_SALIDA_1_1_1_1_100G
 endif
 end-filter
#
#INBOUND AND OUTBOUND FILTER FOR IPv6.
#
xpl route-filter XPL_VERIZON_2800_1_F_1_ipv6_out
 if ipv6 route-destination in PFX_INFINITUM_IPv6 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_1 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_2 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_3 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_4 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_5 then
  refuse
 elseif ipv6 route-destination in INT_PFX_IPV6_CLIENTES_6 then
  refuse
 else
  refuse
 endif
 end-filter
#
xpl route-filter policy_nbr_2800_1_F_1_ipv6_in
 if (as-path in aspath_1_p2_permit and ipv6 route-destination in pfx_BCP_IPv6_in_ebgp_permit) then
  approve
 endif
 end-filter
#
xpl route-filter XPL_POLICY_VERIZON_2800_1_F_1_ipv6_out
 if as-path in aspath_150 then
  call route-filter XPL_VERIZON_2800_1_F_1_ipv6_out
 endif
 end-filter
#
#INTERFACE CONFIG AND BGP PEER.
#
interface 100GE2/0/2
description CP:100GB ! EBGP:VERIZON 1-800000001 | PEER:1.1.1.1
undo shutdown
set flow-stat interval 30
ipv6 enable
ip address 1.1.1.2 255.255.255.252
ipv6 address 2800:1:F::2/127
traffic-policy TP_INTERNET_VERIZON_NBR_1_1_1_1_IN inbound
traffic-policy TP_INTERNET_VERIZON_NBR_1_1_1_1_OUT outbound
#
commit
#
bgp 271812
 peer 1.1.1.1 as-number 701
 peer 1.1.1.1 description VERIZON_100GB_100GE2/0/2
 peer 2800:1:F::1 as-number 701
 peer 2800:1:F::1 description VERIZON_100GB_100GE2/0/2
 ipv4-family unicast
  peer 1.1.1.1 enable
  YES
  peer 1.1.1.1 public-as-only
  peer 1.1.1.1 route-filter policy_nbr_1_1_1_1_ipv4_unicast_in import
  peer 1.1.1.1 route-filter policy_nbr_1_1_1_1_ipv4_unicast_out export
  peer 1.1.1.1 advertise-community
  peer 1.1.1.1 advertise-ext-community
 ipv6-family unicast
  peer 2800:1:F::1 enable
  peer 2800:1:F::1 public-as-only force
  peer 2800:1:F::1 route-filter policy_nbr_2800_1_F_1_ipv6_in import
  peer 2800:1:F::1 route-filter XPL_POLICY_VERIZON_2800_1_F_1_ipv6_out export
  peer 2800:1:F::1 advertise-community
  peer 2800:1:F::1 advertise-ext-community
#
commit
#
quit
#
save
#
```
## Requirements

* jinja2
* contextlib
* Python 3.9 =>
