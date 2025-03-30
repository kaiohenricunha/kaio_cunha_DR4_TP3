import socket

def cliente_tcp(host="127.0.0.1", porta=5000):
    # Cria o socket (IPv4, TCP)
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    
    # Conecta ao servidor
    cliente.connect((host, porta))
    print(f"Conectado ao servidor em {host}:{porta}")

    # Solicita uma mensagem do usuário
    mensagem = input("Digite a mensagem a enviar: ")

    # Envia os dados
    cliente.sendall(mensagem.encode("utf-8"))

    # Recebe a resposta (eco) do servidor
    resposta = cliente.recv(1024)
    print("Resposta do servidor:", resposta.decode("utf-8"))

    # Fecha a conexão
    cliente.close()

if __name__ == "__main__":
    cliente_tcp()
