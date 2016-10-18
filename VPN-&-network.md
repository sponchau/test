`georges$ip route add 192.168.255.0/24 via 172.17.0.2`
`bash#iptables -t nat -A PREROUTING -j DNAT -d 172.17.0.2 -p udp --dport 8081 --to 192.168.255.2:8081`
`bash#iptables -t nat -A PREROUTING -j DNAT -d 172.17.0.2 -p tcp --dport 8081 --to 192.168.255.2:8081`
`iptables -t nat -A POSTROUTING -j MASQUERADE`
`sysctl net.ipv4.ip_forward=1`
` iptables -t nat -L`

georgeslamp : 172.17.0.3/16
mysql : 172.17.0.4/16
ovpnserver : 172.17.0.2/16 eth0 192.168.255.1/24
raspberry : 192.168.255.3/24

kylemanna/openvpn