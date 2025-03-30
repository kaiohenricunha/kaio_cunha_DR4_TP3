import socket
import os

def cliente_de_arquivos(host="127.0.0.1", porta=9090):
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    cliente.connect((host, porta))
    print(f"Conectado ao servidor {host}:{porta}")

    while True:
        comando = input("Digite o comando (UPLOAD <arq>, DOWNLOAD <arq>, EXIT): ")
        if not comando:
            continue

        partes = comando.split()
        acao = partes[0].upper()

        if acao == "UPLOAD":
            if len(partes) < 2:
                print("Uso: UPLOAD <arquivo>")
                continue
            nome_arquivo = partes[1]
            if not os.path.exists(nome_arquivo):
                print("Arquivo não existe!")
                continue

            # Envia o comando e o nome do arquivo
            cliente.sendall(comando.encode("utf-8"))

            # Calcula e envia o tamanho do arquivo
            tamanho_arquivo = os.path.getsize(nome_arquivo)
            cliente.sendall(str(tamanho_arquivo).encode("utf-8"))

            # Envia o arquivo em blocos
            with open(nome_arquivo, "rb") as f:
                while True:
                    chunk = f.read(1024)
                    if not chunk:
                        break
                    cliente.sendall(chunk)

            # Recebe confirmação do servidor
            resposta = cliente.recv(1024).decode("utf-8")
            if resposta == "UPLOAD_OK":
                print("Upload concluído com sucesso!")
            else:
                print("Falha no upload.")

        elif acao == "DOWNLOAD":
            if len(partes) < 2:
                print("Uso: DOWNLOAD <arquivo>")
                continue
            nome_arquivo = partes[1]

            # Envia comando para o servidor
            cliente.sendall(comando.encode("utf-8"))

            # Recebe tamanho do arquivo ou mensagem de erro
            resposta = cliente.recv(1024).decode("utf-8")
            if resposta.startswith("ERROR"):
                print("Arquivo não encontrado no servidor.")
            else:
                # Prepara para receber o arquivo
                tamanho_arquivo = int(resposta)
                cliente.sendall(b"OK")  # Confirma que está pronto
                with open(nome_arquivo, "wb") as f:
                    bytes_restantes = tamanho_arquivo
                    while bytes_restantes > 0:
                        chunk = cliente.recv(min(1024, bytes_restantes))
                        if not chunk:
                            break
                        f.write(chunk)
                        bytes_restantes -= len(chunk)
                print(f"Download de '{nome_arquivo}' concluído.")

        elif acao == "EXIT":
            cliente.sendall(comando.encode("utf-8"))
            print("Encerrando cliente.")
            cliente.close()
            break

        else:
            print("Comando inválido.")

if __name__ == "__main__":
    cliente_de_arquivos()
