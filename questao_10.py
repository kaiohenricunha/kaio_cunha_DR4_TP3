import socket

def cliente_http(host="127.0.0.1", porta=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as cliente:
        cliente.connect((host, porta))
        
        # Monta a requisição HTTP (GET /)
        requisicao = (
            f"GET / HTTP/1.1\r\n"
            f"Host: {host}\r\n"
            "Connection: close\r\n"
            "\r\n"
        )
        
        # Envia a requisição
        cliente.sendall(requisicao.encode("utf-8"))
        
        # Recebe a resposta
        resposta = b""
        while True:
            dados = cliente.recv(1024)
            if not dados:
                break
            resposta += dados
        
        print("Resposta do servidor HTTP:\n")
        print(resposta.decode("utf-8"))

if __name__ == "__main__":
    cliente_http()
