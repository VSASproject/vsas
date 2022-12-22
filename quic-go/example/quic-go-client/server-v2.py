import socket
import os
import math
import struct
import time

server_ip = "127.0.0.1"
local_ip = "127.0.0.1"
server_port = 4243
local_port = 4242
remoteaddr = (server_ip, server_port)
localaddr = (local_ip, local_port)

HEADER_LEN = 12
MTU = 1480
MAX_PAYLOAD = (MTU-HEADER_LEN)
num_frame = 0


def send_file_v1(udp_socket, frame_no, num_packets, filename):
    with open(filename, 'rb') as file:
        for num_packet_ in range(num_packets):
            flag = 0
            if num_packet_ == num_packets - 1:
                flag = 1
            data_header = struct.pack("!III", frame_no, num_packet_, flag)
            data_buf = file.read(MAX_PAYLOAD)
            if data_buf == "":
                break  # end of file
            full_buf = data_header + data_buf
            udp_socket.sendto(full_buf, remoteaddr)


def udp_serve(frame_no):
    udp_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp_socket.bind(localaddr)
    buf, n = udp_socket.recvfrom(100)
    filename = buf.decode('utf-8')
    print("Received File Request: " + filename)
    filename = os.path.join("TrackedMeshes", filename)
    file_size = os.path.getsize(filename)
    num_packets = math.ceil(file_size / MAX_PAYLOAD)
    print(num_packets)
    send_file_v1(udp_socket,frame_no, num_packets,filename)


if __name__ == "__main__":
    while True:
        num_frame += 1
        udp_serve(num_frame)