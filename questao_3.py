import socket

# Criando um socket RAW para capturar todo o tráfego IP
raw_socket = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)

# Receber dados
while True:
    pacote, addr = raw_socket.recvfrom(65535)
    print(f"Recebido de {addr}: {pacote}")
