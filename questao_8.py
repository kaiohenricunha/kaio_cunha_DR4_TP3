import socket

def cliente_udp(host="127.0.0.1", porta=5001):
    # Cria o socket (IPv4, UDP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    mensagem = input("Digite a mensagem a enviar: ")
    # Envia a mensagem para o servidor
    cliente.sendto(mensagem.encode("utf-8"), (host, porta))

    # Aguarda a resposta
    resposta, _ = cliente.recvfrom(1024)
    print("Resposta do servidor:", resposta.decode("utf-8"))

    # Fecha o socket
    cliente.close()

if __name__ == "__main__":
    cliente_udp()
