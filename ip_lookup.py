#######################################################
#                                                     #
# Creator: HakuTento                                  #
#                                                     #
# Free for anyone to use. Do not remove this section. #
# Any suggestions, erros, or anything else please use #
# the github page for this.                           #
#                                                     #
#                                                     #
#                                                     #
#######################################################
import netifaces as nf   # make sure to run pip install netifaces
from socket import *
from requests import get # make sure to run pip install requests
import ifaddr            # may need to run pip install ifaddr
import getpass
import platform

# Looks for gateways that the machine is aware of.
gws = nf.gateways()
if len(gws[2]) > 1:
    for i, gate in enumerate(gws[2],1):
        print('Gateway' + str(i) + ': \t\t\t', gws[2][i-1][0])
elif len(gws[2]) == 1:
    print('Gateway: \t\t\t', gws[2][0][0])
else:
    print('No gateways found')
    exit

# Simple. Prints current logged in user and Machine name
print('WhoAmI: \t\t\t', getpass.getuser())
print('Hostname: \t\t\t', gethostname())

# This grabs the local ip. If it is the loop address it 
# makes as socket and checks the ip per the socket
if gethostbyname(gethostname()) == '127.0.0.1':
    s = socket(AF_INET, SOCK_DGRAM)
    s.connect(("8.8.8.8",80))
    print('Local IP:\t', s.getsockname()[0])
    s.close()
else:
    print('Local IP:\t\t\t', gethostbyname(gethostname()))

# Obtains public ip address
p_ip = get('https://api.ipify.org').text
print('Public IP: \t\t\t', p_ip)

# Heavy part. Gets system list of network adapters and the os version.
# Then depending on os type, parses the info to grab adapter name and
# ip4 address. Ends up *nix and Windows stack the ip address differently.
# Not really a surprise, just means more lines.
adapters = list(ifaddr.get_adapters())
os = platform.system()

for nic in range(len(adapters)):
    net_card = adapters

    if os == 'Windows':
        if len(net_card[nic].ips[0].nice_name) < 5:
            print("%s: \t\t\t\t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[-1].ip))
        elif len(net_card[nic].ips[0].nice_name) < 11:
            print("%s: \t\t\t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[-1].ip))
        else:
            print("%s: \t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[-1].ip))
    elif os == 'Linux':
        if len(net_card[nic].ips[0].nice_name) < 5:
            print("%s: \t\t\t\t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[0].ip))
        elif len(net_card[nic].ips[0].nice_name) < 11:
            print("%s: \t\t\t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[0].ip))
        else:
            print("%s: \t %s" % (adapters[nic].ips[0].nice_name, adapters[nic].ips[0].ip))
