import socket
import ssl
from datetime import datetime

def cliente_https(host="127.0.0.1", porta=8443):
    # Cria um contexto SSL “default” para cliente, que já faz verificação de certificado
    contexto = ssl.create_default_context()

    # Se estiver usando certificados autoassinados em testes locais e quiser ignorar erros,
    # descomente a linha abaixo (não recomendado em produção):
    # contexto.check_hostname = False
    # contexto.verify_mode = ssl.CERT_NONE

    with socket.create_connection((host, porta)) as conexao:
        # Envolve o socket em SSL, enviando o host para SNI
        with contexto.wrap_socket(conexao, server_hostname=host) as ssock:
            # Exemplo de requisição HTTP simples
            requisicao = (
                f"GET / HTTP/1.1\r\n"
                f"Host: {host}\r\n"
                "Connection: close\r\n"
                "\r\n"
            )
            ssock.sendall(requisicao.encode("utf-8"))

            # Recebe a resposta do servidor
            resposta = b""
            while True:
                dados = ssock.recv(1024)
                if not dados:
                    break
                resposta += dados

            print("Resposta do servidor HTTPS:\n")
            print(resposta.decode("utf-8", errors="ignore"))

            # Obtendo o certificado apresentado pelo servidor
            cert = ssock.getpeercert()
            if cert:
                print("\n=== Certificado recebido do servidor ===")

                # Subject (nome comum)
                subject = dict(item[0] for item in cert.get("subject", []))
                print(f"Subject (CN): {subject.get('commonName')}")

                # Emissor
                issuer = dict(item[0] for item in cert.get("issuer", []))
                print(f"Issuer (CN) : {issuer.get('commonName')}")

                # Validade
                valido_de = cert["notBefore"]
                valido_ate = cert["notAfter"]
                print(f"Válido de   : {valido_de}")
                print(f"Válido até  : {valido_ate}")
            else:
                print("Não foi possível obter o certificado do servidor.")

if __name__ == "__main__":
    cliente_https()
