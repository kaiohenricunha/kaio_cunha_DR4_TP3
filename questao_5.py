import socket

def iniciar_servidor_tcp(host="0.0.0.0", porta=5000):
    # Cria o socket (IPv4, TCP)
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    # Faz o bind do socket no host e porta
    servidor.bind((host, porta))

    # Começa a escutar conexões (até 5 na fila)
    servidor.listen(5)
    print(f"Servidor iniciado em {host}:{porta}. Aguardando conexões...")

    while True:
        # Aceita uma conexão
        cliente, endereco = servidor.accept()
        print(f"Conexão recebida de {endereco}.")

        # Recebe dados e envia de volta (Echo)
        dados = cliente.recv(1024)
        if dados:
            print(f"Mensagem recebida: {dados.decode('utf-8')}")
            cliente.sendall(dados)  # devolve a mesma mensagem

        # Fecha a conexão com o cliente
        cliente.close()
        print(f"Conexão encerrada com {endereco}.")

if __name__ == "__main__":
    iniciar_servidor_tcp()
