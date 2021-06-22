from scapy.all import *
import codecs
import binascii

def ip_make_tos(tos, ecn, dscp):
    if ecn is not None:
        tos = (tos & ~(0x3)) | ecn

    if dscp is not None:
        tos = (tos & ~(0xfc)) | (dscp << 2)

    return tos

def simple_udp_packet(pktlen=58,
                      eth_dst='01:00:5E:00:01:C0',
                      eth_src='02:00:00:00:02:00',
                      dl_vlan_enable=True,
                      vlan_vid=129,
                      vlan_pcp=7,
                      dl_vlan_cfi=0,
                      ip_src='10.0.2.0',
                      ip_dst='239.0.1.192',
                      ip_tos=0,
                      ip_ecn=None,
                      ip_dscp=None,
                      ip_ttl=32,
                      udp_sport=50204,
                      udp_dport=51915,
                      ip_ihl=None,
                      ip_options=False,
                      ip_flag=0,
                      ip_id=0,
                      with_udp_chksum=True,
                      udp_payload=binascii.unhexlify("0000041c000000088db0000100000000")
                      ):
    if with_udp_chksum:
        udp_hdr = UDP(sport=udp_sport, dport=udp_dport)
    else:
        udp_hdr = UDP(sport=udp_sport, dport=udp_dport, chksum=0)

    ip_tos = ip_make_tos(ip_tos, ip_ecn, ip_dscp)

    # Note Dot1Q.id is really CFI

    if (dl_vlan_enable):
        pkt = Ether(dst=eth_dst, src=eth_src) / \
              Dot1Q(prio=vlan_pcp, id=dl_vlan_cfi, vlan=vlan_vid) / \
              IP(src=ip_src, dst=ip_dst, tos=ip_tos, ttl=ip_ttl, ihl=ip_ihl, id=ip_id) / \
              udp_hdr

    else:
        if not ip_options:
            pkt = Ether(dst=eth_dst, src=eth_src) / \
                  IP(src=ip_src, dst=ip_dst, tos=ip_tos, ttl=ip_ttl, ihl=ip_ihl, id=ip_id, flags=ip_flag) / \
                  udp_hdr
        else:
            pkt = Ether(dst=eth_dst, src=eth_src) / \
                  IP(src=ip_src, dst=ip_dst, tos=ip_tos, ttl=ip_ttl, ihl=ip_ihl, options=ip_options, id=ip_id,
                     flags=ip_flag) / \
                  udp_hdr

    if udp_payload:
        pkt = pkt / udp_payload

    pkt = pkt / codecs.decode("".join(["%02x" % (x % 256) for x in range(pktlen - len(pkt))]), "hex")

    return pkt

"""
a=Ether(src="02.00.00.00.02.00", dst="01.00.5E.00.01.00",type=0x8100)
a.show()

b=IP(ttl=10, src="10.0.2.0", dst="239.0.1.192" )
b.show()

c=TCP(sport=50204, dport=51915, flags='A')
c.show()

"""

# sendp(a/b/c) #2계층
# sendp("I'm travelling Ethernet", iface="Intel(R) Ethernet Connection (7) I219-LM", loop=1, inter=0.2)
# send() #3계층

# sendp("I'm travelling Ethernet", iface="Realtek USB GbE Family Controller", loop=1, inter=0.2)
# sdata=b'x02/x00/x00/x00/x03/x00/x02/x00/x00/x00/x05/x00/x81/x00/xe0/x81/x08/x00/x45/x00/x00/x2c/x00/x00/x00/x00/x20/x11/x7e/xc2/x0a/x00/x05/x00/x0a/x00/x03/x00/xc4/x1a/xca/xca/x00/x18/x7d/xb6/x00/x00/x04/x1a/x00/x00/x00/x08/x0a/x10/x00/x00/x00/x40/x00/x00'

sdata = simple_udp_packet()
for i in range(1):
    sdata.show()
    # sendp(sdata, iface="Realtek USB GbE Family Controller", loop=0, inter=0.2)
    sendp(sdata, iface="Realtek USB GbE Family Controller #2")

print('hi')

'''
a1 = Ether()
a1.dst = '01:00:5E:00:00:01'
a1.src = '02:00:00:00:05:00'
a1.type = 0x8100

a2 = Dot1Q()
a2.id = 0
a2.prio = 0x0007
a2.vlan = 129
a2.type = 0x0800

a3 = IP()
a3.ihl = 5
a3.len = 68
a3.id = 0
a3.ttl = 32
a3.proto = 17
a3.chksum = 0x9CA8
a3.src = '10.0.5.0'
a3.dst = '239.0.0.1'

a4 = UDP()
a4.sport = 49216
a4.dport = 51915
a4.len = 48
a4.chksum = 0x6F20

a5 = Raw()
a5.load = 0x0000004000000020000000007000000000000000000000000000000000000000000000000000000

myPacket = a1/a2/a3/a4/a5
myPacket.show()

sendp(a1/a2/a3/a4/a5)
'''
