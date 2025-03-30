import socket
import os

def iniciar_servidor_de_arquivos(host="0.0.0.0", porta=9090):
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.bind((host, porta))
    servidor.listen(5)
    print(f"Servidor de arquivos iniciado em {host}:{porta}...")

    while True:
        cliente, endereco = servidor.accept()
        print(f"Conexão estabelecida com {endereco}")

        while True:
            dados_recebidos = cliente.recv(1024).decode("utf-8")
            if not dados_recebidos:
                break

            partes = dados_recebidos.split()
            comando = partes[0].upper()

            if comando == "UPLOAD":
                # Exemplo: "UPLOAD nome_do_arquivo"
                nome_arquivo = partes[1]
                # Recebe o tamanho do arquivo
                tamanho_arquivo = int(cliente.recv(1024).decode("utf-8"))

                # Lê os bytes do arquivo e salva localmente
                with open(nome_arquivo, "wb") as f:
                    bytes_restantes = tamanho_arquivo
                    while bytes_restantes > 0:
                        chunk = cliente.recv(min(1024, bytes_restantes))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_restantes -= len(chunk)

                print(f"Arquivo '{nome_arquivo}' recebido com sucesso!")
                cliente.sendall(b"UPLOAD_OK")

            elif comando == "DOWNLOAD":
                # Exemplo: "DOWNLOAD nome_do_arquivo"
                nome_arquivo = partes[1]
                if not os.path.exists(nome_arquivo):
                    # Se o arquivo não existe, retorna erro
                    cliente.sendall(b"ERROR_FILE_NOT_FOUND")
                else:
                    # Se existe, envia o tamanho do arquivo e aguarda um "OK"
                    tamanho_arquivo = os.path.getsize(nome_arquivo)
                    cliente.sendall(str(tamanho_arquivo).encode("utf-8"))
                    confirmacao = cliente.recv(1024).decode("utf-8")
                    if confirmacao == "OK":
                        # Lê e envia o arquivo em blocos
                        with open(nome_arquivo, "rb") as f:
                            while True:
                                chunk = f.read(1024)
                                if not chunk:
                                    break
                                cliente.sendall(chunk)
                        print(f"Arquivo '{nome_arquivo}' enviado com sucesso!")

            elif comando == "EXIT":
                print(f"Encerrando conexão com {endereco}")
                cliente.close()
                break

            else:
                cliente.sendall(b"COMANDO_INVALIDO")

if __name__ == "__main__":
    iniciar_servidor_de_arquivos()
