import socket
import threading
import sys

# Constants
HOST_IP = '127.0.0.1'  
PORT = 10352           

# Lista para armazenar clientes conectados: [(client_socket, client_address), ...]
connected_clients = []

def banner():
    text = """
    ===========================================
    |       COMMAND & CONTROL SERVER          |
    |          Alunos: Derick e Ryan          |
    ===========================================
    Comandos disponíveis: 
    - /help: exibe os comandos disponíveis
    - /list: lista os clientes conectados
    - /send <id> <msg>: mensagem para um cliente
    - /send <msg>: mensagem para todos
    - /quit: encerra o servidor
    ===========================================
    """
    print(text)
    return text

def send_message_to_client(client_id, message):
    try:
        idx = int(client_id)
        if 0 <= idx < len(connected_clients):
            client_socket, _ = connected_clients[idx]
            client_socket.sendall(f"[SERVER]: {message}".encode())
            return True
        return False
    except (ValueError, IndexError):
        return False

def send_message_to_all_clients(message):
    for client_socket, _ in connected_clients:
        try:
            client_socket.sendall(f"[SERVER-ALL]: {message}".encode())
        except:
            pass
    return True

def handle_client(client_socket, client_address):
    print(f"[NOVA CONEXÃO] {client_address} conectado.")
    welcome = "Conectado ao C2 Server. Digite /help para comandos.\n"
    client_socket.sendall(welcome.encode())

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            
            print(f"[{client_address}] enviou: {data}")
            
            # Lógica simples de resposta para o cliente
            if data == "/help":
                response = "Comandos: /help, /list, /quit"
                client_socket.sendall(response.encode())
            else:
                client_socket.sendall(f"Recebido: {data}".upper().encode())

        except:
            break

    print(f"[DESCONECTADO] {client_address}")
    if (client_socket, client_address) in connected_clients:
        connected_clients.remove((client_socket, client_address))
    client_socket.close()

def start_server():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    
    try:
        server_socket.bind((HOST_IP, PORT))
        server_socket.listen(5)
        banner()
        print(f"[*] Servidor escutando em {HOST_IP}:{PORT}")
    except Exception as e:
        print(f"[!] Erro ao iniciar servidor: {e}")
        return

    while True:
        client_socket, client_address = server_socket.accept()
        connected_clients.append((client_socket, client_address))
        
        thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        thread.daemon = True
        thread.start()

# O "Pulo do Gato": Chamar a função principal para o script rodar!
if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[!] Encerrando servidor...")
        sys.exit(0)
