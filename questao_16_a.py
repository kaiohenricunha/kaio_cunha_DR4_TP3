import socket
import ssl

def servidor_https(host="0.0.0.0", porta=8443):
    # Cria um socket comum (IPv4, TCP)
    servidor_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor_socket.bind((host, porta))
    servidor_socket.listen(5)
    print(f"Servidor HTTPS rodando em {host}:{porta}")

    # Cria um contexto SSL, carregando o certificado e a chave
    contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
    contexto.load_cert_chain(certfile="server.crt", keyfile="server.key")

    while True:
        conexao, endereco = servidor_socket.accept()
        print(f"Conexão recebida de {endereco}")

        # “Envelopa” o socket com SSL/TLS
        with contexto.wrap_socket(conexao, server_side=True) as conexao_ssl:
            # Recebe a requisição
            requisicao = conexao_ssl.recv(1024).decode("utf-8", errors="ignore")
            if not requisicao:
                continue

            # Exemplo simples de parsing: verifica se é GET /
            linha_inicial = requisicao.split("\r\n")[0]
            if "GET / " in linha_inicial:
                try:
                    with open("index.html", "r", encoding="utf-8") as arquivo_html:
                        conteudo = arquivo_html.read()
                    resposta = (
                        "HTTP/1.1 200 OK\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "\r\n"
                        f"{conteudo}"
                    )
                except FileNotFoundError:
                    resposta = (
                        "HTTP/1.1 404 Not Found\r\n"
                        "Content-Type: text/html; charset=utf-8\r\n"
                        "\r\n"
                        "<h1>404 - Arquivo index.html não foi encontrado</h1>"
                    )
            else:
                resposta = (
                    "HTTP/1.1 404 Not Found\r\n"
                    "Content-Type: text/html; charset=utf-8\r\n"
                    "\r\n"
                    "<h1>404 - Página não encontrada</h1>"
                )

            conexao_ssl.sendall(resposta.encode("utf-8"))

if __name__ == "__main__":
    servidor_https()
