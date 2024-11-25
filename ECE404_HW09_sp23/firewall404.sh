# Homework Number: 09
# Name: Parth R Doshi
# ECN Login: doshi36    
# Due Date: 3/28

#1 Flush and delete all previously defined rules and chains.
sudo iptables -t filter -F
sudo iptables -t filter -X
sudo iptables -t mangle -F
sudo iptables -t mangle -X
sudo iptables -t nat -F
sudo iptables -t nat -X
sudo iptables -t raw -F
sudo iptables -t raw -X

#2 Write a rule that only accepts packets that originate from f1.com.
sudo iptables -t filter -A INPUT -s "f1.com" -j ACCEPT

#3 For all outgoing packets, change their source IP address to your own machine’s IP address
# (Hint: Refer to the MASQUERADE target in the nat table).
sudo iptables -t nat -A POSTROUTING -o all -j MASQUERADE

#4 Write a rule to protect yourself against indiscriminate and nonstop scanning of ports on your machine.
sudo iptables -A FORWARD -p tcp --tcp-flags SYN,ACK,FIN,RST SYN -m limit --limit 1/s -j ACCEPT

#5 Write a rule to protect yourself from a SYN-flood Attack by limiting the number of incoming
# 'new connection' requests to 1 per second once your machine has reached 500 requests.
sudo iptables -A FORWARD -p tcp --syn -m limit --limit 1/s --limit-burst 500 -j ACCEPT

#6 Write a rule to allow full loopback access on your machine i.e. access using localhost
# (Hint: You will need two rules, one for the INPUT chain and one the OUTPUT chain on the
# FILTER table. The interface is ’lo’.)
sudo iptables -t filter -A INPUT -i lo -j ACCEPT
sudo iptables -t filter -A OUTPUT -o lo -j ACCEPT

#7 Write a port forwarding rule that routes all traffic arriving on port 8888 to port 25565. Make
# sure you specify the correct table and chain. Subsequently, the target for the rule should be
# DNAT.
sudo iptables -t nat -A PREROUTING -p tcp --dport 8888 -j DNAT --to-destination :25565

#8 Write a rule that only allows outgoing ssh connections to engineering.purdue.edu. You
# will need two rules, one for the INPUT chain and one for the OUTPUT chain on the FILTER
# table. Make sure to specify the correct options for the --state suboption for both rules.
sudo iptables -A OUTPUT -p tcp --dport 22 -d engineering.purdue.edu -m state --state NEW,ESTABLISHED -j ACCEPT
sudo iptables -A INPUT -p tcp --sport 22 -s engineering.purdue.edu -m state --state ESTABLISHED,RELATED -j ACCEPT

#9 Drop any other packets if they are not caught by the above rules.
sudo iptables -A OUTPUT -j DROP
sudo iptables -A INPUT -j DROP