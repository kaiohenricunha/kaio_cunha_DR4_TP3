import socket

def scan_port(host, port):
    """Tenta conectar ao host na porta especificada e retorna True se estiver aberta."""
    try:
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.settimeout(0.5)  # tempo limite de meio segundo
        s.connect((host, port))
        s.close()
        return True
    except:
        return False

def port_scanner():
    host = input("Digite o endereço IP ou hostname que deseja escanear: ")
    print(f"\nIniciando varredura de portas em {host}...")
    
    for port in range(1, 1025):  # vamos escanear da porta 1 até 1024
        if scan_port(host, port):
            print(f"Porta {port} está aberta.")
    
    print("\nVarredura finalizada.")

if __name__ == "__main__":
    port_scanner()
