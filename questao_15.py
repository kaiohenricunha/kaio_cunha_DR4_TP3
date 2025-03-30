import socket
import ssl

def servidor_https(host="0.0.0.0", porta=8443):
    # Cria um socket comum (IPv4, TCP)
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as servidor:
        servidor.bind((host, porta))
        servidor.listen(5)
        print(f"Servidor HTTPS rodando em {host}:{porta}")

        # Cria um contexto SSL e carrega o certificado e chave
        contexto = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        contexto.load_cert_chain(certfile="server.crt", keyfile="server.key")

        while True:
            conexao, endereco = servidor.accept()
            print(f"Conexão recebida de {endereco}")
            
            # Encapsula a conexão TCP em SSL/TLS
            with contexto.wrap_socket(conexao, server_side=True) as conexao_ssl:
                # Recebe o request
                try:
                    requisicao = conexao_ssl.recv(1024).decode("utf-8")
                except ssl.SSLError as e:
                    print("Erro SSL:", e)
                    continue

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

                # Envia a resposta pela conexão segura
                conexao_ssl.sendall(resposta.encode("utf-8"))

if __name__ == "__main__":
    servidor_https()
