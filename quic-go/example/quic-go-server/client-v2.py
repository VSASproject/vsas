import socket
import json
import struct
import re

MAX_LEN = 1000000
HEADER_LEN = 12
server_ip = "localhost"
local_ip = "localhost"
server_port = 4242
local_port = 4243
MTU=1480

def check_recv(bucket,bucket_size): #受到packet数量
    n = 0
    for i in range(bucket_size):
        if bucket[i] == 1:
            n += 1
    return n

def check_full(bucket,bucket_size): #是否完整
    for i in range(bucket_size):
        if bucket[i] == 0:
            return False
    return True


def get_packet_payload(packet):
    return packet[HEADER_LEN:]


def get_packet_number(packet):
    udp_header = packet[:HEADER_LEN]
    udp_header_str = struct.unpack("!III", udp_header)
    frame_no = udp_header_str[0]
    packet_no = udp_header_str[1]
    if_last_packet_flag = udp_header_str[2]
    return frame_no, packet_no, if_last_packet_flag


def save_data_dict_to_file(bucket_dict,target_path,num_packets):
    full_buf = bytearray()
    for i in range(0,num_packets):
        if bucket_dict.get(i) != None:
            full_buf += bucket_dict[i]
    with open(target_path,'wb') as f1:
        f1.write(full_buf)


def clear_udp_recv_queue(udp_socket):
    while True:
        n = udp_socket.recv(2000)
        print(n)
        if n.decode() == "OK":
            break


def udp_request(filename, target_path):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    remoteaddr = (server_ip, server_port)
    localaddr = (local_ip, local_port)
    udp_socket.bind(localaddr)
    udp_socket.sendto(filename.encode("utf-8"), remoteaddr)
    # num_packets_str, n = udp_socket.recvfrom(2000)
    bucket = [0] * MAX_LEN
    bucket_dict = {}
    first_requested_frame_flag = 0
    current_frame_no = -1
    num_packets = -1
    while True:
        packet, n = udp_socket.recvfrom(MTU)
        frame_no, packet_no, if_last_packet_flag = get_packet_number(packet)
        if first_requested_frame_flag == 0:
            current_frame_no = frame_no
            first_requested_frame_flag = 1
        if current_frame_no < frame_no:
            break
        if current_frame_no > frame_no:
            continue
        if bucket[packet_no] == 1:
            continue
        if packet_no % 1000 == 0:
            print("Received packet " + str(packet_no))
        if packet_no > num_packets:
            num_packets = packet_no
        bucket_dict[packet_no] = get_packet_payload(packet)
        bucket[packet_no] = 1
        if if_last_packet_flag == 1:  # last packet, stop
            break
    print("Received all packets, total:", num_packets, "packets")
    save_data_dict_to_file(bucket_dict, target_path, num_packets)
    #clear_udp_recv_queue(udp_socket)


def manifest_to_list(manifest_path):
    with open(manifest_path, 'r') as myfile:
        data = myfile.read()
    # parse file
    obj = json.loads(data)
    return obj


def stream_with_manifest(manifest_path):
    manifest = manifest_to_list(manifest_path)
    str_for = r'\d+_(\d+)'

    for chunk in manifest:
        filename = chunk['filename']

        match = re.search(str_for, filename)
        current_frame_no = int(match.group(1))

        print("Fetching " + filename)
        udp_request(filename, "Fetched/"+filename+".back")
        print("Fetched.")


if __name__=="__main__":
    stream_with_manifest("manifest.json")
