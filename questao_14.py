import socket
import ssl
from datetime import datetime

def obter_certificado(host, porta=443):
    # Cria um contexto SSL seguro usando as configurações padrão
    contexto = ssl.create_default_context()

    # Abre uma conexão TCP com o host na porta HTTPS (por padrão, 443)
    with socket.create_connection((host, porta)) as conexao:
        # Envolve o socket em SSL, fornecendo o nome do host para SNI
        with contexto.wrap_socket(conexao, server_hostname=host) as conexao_ssl:
            # Retorna o certificado no formato de dicionário
            return conexao_ssl.getpeercert()

def exibir_informacoes_certificado(cert, host):
    print(f"\nInformações do certificado de '{host}':")

    # Pegando o "subject" (dono do certificado)
    subject = dict(x[0] for x in cert.get("subject", []))
    print(f"  - Subject (CN): {subject.get('commonName')}")
    
    # Pegando o "issuer" (autoridade emissora)
    issuer = dict(x[0] for x in cert.get("issuer", []))
    print(f"  - Issuer (CN): {issuer.get('commonName')}")
    
    # Datas de validade
    valido_de = datetime.strptime(cert["notBefore"], "%b %d %H:%M:%S %Y %Z")
    valido_ate = datetime.strptime(cert["notAfter"], "%b %d %H:%M:%S %Y %Z")
    print(f"  - Válido de: {valido_de}")
    print(f"  - Válido até: {valido_ate}")

    # Subject Alt Names (SAN), se existirem
    san = cert.get("subjectAltName", [])
    if san:
        nomes = [valor for (tipo, valor) in san if tipo == "DNS"]
        print(f"  - Subject Alt Names (DNS): {', '.join(nomes)}")
    else:
        print("  - Subject Alt Names (DNS): Não especificado")

def main():
    host = input("Digite o nome do servidor HTTPS: ")
    try:
        certificado = obter_certificado(host)
        exibir_informacoes_certificado(certificado, host)
    except Exception as e:
        print(f"Erro ao obter o certificado de {host}: {e}")

if __name__ == "__main__":
    main()
