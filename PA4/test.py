#!/usr/bin/python
"""Chat server for CST311 Programming Assignment 3"""
__author__ = "Team 8"
__credits__ = [
  "Michael Cervantes",
  "Jerry Do",
  "Ramo Tucakovic"
]

from mininet.net import Mininet
from mininet.node import Controller, RemoteController, OVSController
from mininet.node import Host, Node
from mininet.node import OVSKernelSwitch, UserSwitch
from mininet.node import IVSSwitch
from mininet.cli import CLI
from mininet.log import setLogLevel, info
from mininet.link import TCLink, Intf
from subprocess import call

def myNetwork():

    net = Mininet( topo=None,
                   build=False,
                   ipBase='10.0.0.0/24')

    info( '*** Adding controller\n' )
    c0=net.addController(name='c0',
                      controller=Controller,
                      protocol='tcp',
                      port=6633)

    info( '*** Add switches\n')
    s2 = net.addSwitch('s2', cls=OVSKernelSwitch)
    s1 = net.addSwitch('s1', cls=OVSKernelSwitch)

    r3 = net.addHost('r3', cls=Node, ip='10.0.0.3/24')
    r3.cmd('sysctl -w net.ipv4.ip_forward=1')

    r4 = net.addHost('r4', cls=Node, ip='192.168.1.1/30')
    r4.cmd('sysctl -w net.ipv4.ip_forward=1')

    r5 = net.addHost('r5', cls=Node, ip='10.0.1.3/24')
    r5.cmd('sysctl -w net.ipv4.ip_forward=1')

    info( '*** Add hosts\n')
    h1 = net.addHost('h1', cls=Host, ip='10.0.0.1/24', defaultRoute='via 10.0.0.3')
    h2 = net.addHost('h2', cls=Host, ip='10.0.0.2/24', defaultRoute='via 10.0.0.3')
    h3 = net.addHost('h3', cls=Host, ip='10.0.1.1/24', defaultRoute='via 10.0.1.3')
    h4 = net.addHost('h4', cls=Host, ip='10.0.1.2/24', defaultRoute='via 10.0.1.3')

    info( '*** Add links\n')
    net.addLink(h1, s1)
    net.addLink(h2, s1)

    net.addLink(h3, s2)
    net.addLink(h4, s2)

    net.addLink(s2, r5)
    net.addLink(s1, r3)

    net.addLink(r3, r4, intfName1='r3-eth1', params1={'ip': '192.168.1.2/30'},
                intfName2='r4-eth0', params2={'ip': '192.168.1.1/30'})
    
    net.addLink(r4, r5, intfName1='r4-eth1', params1={'ip': '192.168.2.2/30'},
                intfName2='r5-eth1', params2={'ip': '192.168.2.1/30'})
    
    info('*** Port rules***\n')
    r3.cmd('ip route add 10.0.1.0/24 via 192.168.1.1 dev r3-eth1')
    r3.cmd('ip route add 192.168.2.0/30 via 192.168.1.1 dev r3-eth1')

    r4.cmd('ip route add 10.0.0.0/24 via 192.168.1.2 dev r4-eth0')
    r4.cmd('ip route add 10.0.1.0/24 via 192.168.2.1 dev r4-eth1')

    r5.cmd('ip route add 192.168.1.0/30 via 192.168.2.2 dev r5-eth1')
    r5.cmd('ip route add 10.0.0.0/24 via 192.168.2.2 dev r5-eth1')

    info( '*** Starting network\n')
    net.build()
    info( '*** Starting controllers\n')
    for controller in net.controllers:
        controller.start()

    info( '*** Starting switches\n')
    net.get('s2').start([c0])
    net.get('s1').start([c0])

    info( '*** Post configure switches and hosts\n')
    #subprocess.call(["python3", "certificate_authority.py"])
    #makeTerm(h2, "tlswebserver", "xterm", None, "python3 PA4_TLS_web_server.py")
    #makeTerm(h4, "tlswebserver", "xterm", None, "python3 PA4_ModifiedServer.py")
    #makeTerm(h2, "tlswebserver", "xterm", None, "python3 PA4_ModifiedServer.py")
    #makeTerm(h2, "tlswebserver", "xterm", None, "python3 PA4_ModifiedClient.py")
    CLI(net)
    net.stop()

if __name__ == '__main__':
    setLogLevel( 'info' )
    myNetwork()