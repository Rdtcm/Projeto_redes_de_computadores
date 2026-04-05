import socket
import threading
import sys

HOST_IP = '127.0.0.1'
PORT = 10352

# Lista de tuplas: [(socket, address), ...]
connected_clients = []

def banner():
    text = """
    ===========================================
    |       COMMAND & CONTROL SERVER          |
    |          Alunos: Derick e Ryan          |
    ===========================================
    Comandos (digite no CLIENTE): 
    - /help: exibe esta lista
    - /list: lista IDs dos clientes no servidor
    - /send <id> <msg>: mensagem para um ID
    - /send <msg>: mensagem para TODOS
    - /quit: encerra sua conexão
    ===========================================
    """
    print(text)
    return text

def handle_client(client_socket, client_address):
    welcome = banner()
    client_socket.sendall(welcome.encode())

    while True:
        try:
            data = client_socket.recv(1024).decode('UTF-8').strip()
            if not data or data.lower() == '/quit':
                break
            
            print(f"[*] Comando recebido de {client_address}: {data}")

            # --- LÓGICA DOS COMANDOS ---
            
            if data == "/help":
                response = "Comandos: /help, /list, /send <id> <msg>, /send <msg>, /quit"
            
            elif data == "/list":
                if not connected_clients:
                    response = "Nenhum cliente conectado."
                else:
                    # Cria uma lista de strings: "ID 0: ('127.0.0.1', 1234)"
                    lista = "\n".join([f"ID {i}: {c[1]}" for i, c in enumerate(connected_clients)])
                    response = f"Clientes ativos:\n{lista}"

            elif data.startswith("/send"):
                parts = data.split(" ", 2)
                
                # Caso 1: /send <id> <mensagem>
                if len(parts) == 3 and parts[1].isdigit():
                    target_id = int(parts[1])
                    msg_to_send = parts[2]
                    if 0 <= target_id < len(connected_clients):
                        target_sock = connected_clients[target_id][0]
                        target_sock.sendall(f"\n[ORDEM PRIVADA]: {msg_to_send}\n".encode())
                        response = f"Mensagem enviada para o ID {target_id}."
                    else:
                        response = "Erro: ID de cliente inválido."
                
                # Caso 2: /send <mensagem> (Broadcast)
                elif len(parts) >= 2:
                    msg_to_send = data.replace("/send ", "", 1)
                    for sock, addr in connected_clients:
                        if sock != client_socket: # Não manda para si mesmo
                            sock.sendall(f"\n[COMANDO GLOBAL]: {msg_to_send}\n".encode())
                    response = "Comando global enviado para todos."
                else:
                    response = "Uso: /send <msg> ou /send <id> <msg>"
            
            else:
                response = f"Servidor processou: {data.upper()}"

            client_socket.sendall(response.encode())

        except Exception as e:
            print(f"[!] Erro com {client_address}: {e}")
            break

    print(f"[-] Conexão encerrada: {client_address}")
    # Remove da lista ao desconectar
    for item in connected_clients:
        if item[0] == client_socket:
            connected_clients.remove(item)
            break
    client_socket.close()

def start_server():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server.bind((HOST_IP, PORT))
    server.listen(5)
    print(f"[*] Servidor C2 Online em {HOST_IP}:{PORT}")

    while True:
        client_sock, addr = server.accept()
        connected_clients.append((client_sock, addr))
        print(f"[+] Novo cliente controlado: {addr}")
        
        thread = threading.Thread(target=handle_client, args=(client_sock, addr))
        thread.daemon = True
        thread.start()

if __name__ == "__main__":
    try:
        start_server()
    except KeyboardInterrupt:
        print("\n[!] Desligando...")
        sys.exit(0)
