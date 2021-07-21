import socket
import struct
import time
import datetime
import pings

DEFAULT_PORT = 7 # 7, 9, 30000
BROADCAST_ADDR = '192.168.1.255'
R_IP  = "192.168.1.102"      # casper
R_MAC = "D4:5D:64:40:2D:71"  # casper

def send_magic_packet(addr):
    # create socket
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        # parse address
        mac_ = addr.upper().replace("-", "").replace(":", "")
        if len(mac_) != 12:
            raise Exception("invalid MAC address format: {}".format(addr))
        buf_ = b'f' * 12 + (mac_ * 20).encode()
        # encode to magic packet payload
        magicp = b''
        for i in range(0, len(buf_), 2):
            magicp += struct.pack('B', int(buf_[i:i + 2], 16))

        # send magic packet
        print("sending magic packet for: {}".format(addr))
        s.sendto(magicp, (BROADCAST_ADDR, DEFAULT_PORT))

def ping_monitoring(addr):
    p = pings.Ping() # Pingオブジェクト作成
    while True:
        res = p.ping(R_IP)  # 対象IP を監視
        print(res)
        if res.is_reached():
          # 監視対象への接続ができた
            print(res)
        else:
          # 監視対象への接続ができなかった
            mac_addr = R_MAC
            send_magic_packet(mac_addr)
            open(r'C:\CasperWakeUp.txt', 'a').write('WakeUp %s\n' % datetime.datetime.now())
        time.sleep(30)

if __name__ == '__main__':
    ping_monitoring(R_IP)
