import socket

def servidor_http(host="0.0.0.0", porta=8080):
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, porta))
        servidor.listen(5)
        print(f"Servidor HTTP rodando em {host}:{porta}")
        
        while True:
            conexao, endereco = servidor.accept()
            with conexao:
                # Recebe o request
                requisicao = conexao.recv(1024).decode("utf-8")
                if not requisicao:
                    continue
                
                # Exemplo básico de parsing: verifica se é GET / 
                linha_inicial = requisicao.split("\r\n")[0]
                if "GET / " in linha_inicial:
                    try:
                        with open("index.html", "r", encoding="utf-8") as arquivo_html:
                            conteudo = arquivo_html.read()
                        # Monta a resposta (HTTP 200)
                        resposta = (
                            "HTTP/1.1 200 OK\r\n"
                            "Content-Type: text/html; charset=utf-8\r\n"
                            "\r\n"
                            f"{conteudo}"
                        )
                    except FileNotFoundError:
                        # Se o arquivo não for encontrado
                        resposta = (
                            "HTTP/1.1 404 Not Found\r\n"
                            "Content-Type: text/html; charset=utf-8\r\n"
                            "\r\n"
                            "<h1>404 - Arquivo index.html não foi encontrado</h1>"
                        )
                else:
                    # Para qualquer outra rota, retorna 404 Not Found
                    resposta = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "\r\n"
                        "<h1>404 - Página não encontrada</h1>"
                    )
                
                conexao.sendall(resposta.encode("utf-8"))
if __name__ == "__main__":
    servidor_http()
