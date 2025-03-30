import socket

def iniciar_servidor_udp(host="0.0.0.0", porta=5001):
    # Cria o socket (IPv4, UDP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    # Associa o socket ao host e porta
    servidor.bind((host, porta))
    print(f"Servidor UDP iniciado em {host}:{porta}. Aguardando mensagens...")

    while True:
        # Recebe dados (até 1024 bytes) e o endereço de quem enviou
        dados, endereco = servidor.recvfrom(1024)
        mensagem = dados.decode("utf-8")
        print(f"Mensagem recebida de {endereco}: {mensagem}")

        # Envia uma resposta ao cliente
        resposta = f"Servidor recebeu: {mensagem}"
        servidor.sendto(resposta.encode("utf-8"), endereco)

if __name__ == "__main__":
    iniciar_servidor_udp()
