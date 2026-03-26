import socket
import threading


# Constants
HOST_IP = '192.168.10.100'  # Ip address of the server
PORT = '10352'  # Port number for the server

CLIENTS_IP = ['192.168.0.3']  # List of connected client IPs

# Lista para armazenar clientes conectados: [(client_socket, client_address), ...]
connected_clients = []


def banner():
    """
COMMAND & CONTROL SERVER

Alunos: Derick e Ryan

_¶¶¶¶¶______________________________________¶¶¶¶
__¶¶____¶¶¶_______¶¶¶¶¶¶_¶¶¶_¶¶¶¶¶______¶¶¶¶___¶
__¶_¶¶_____¶¶¶¶¶¶__________________¶¶¶¶¶¶_____¶¶
__¶___¶__________¶___________________________¶__¶
__¶____¶___________________________________¶¶___¶
__¶______¶¶_______________________________¶_____¶
__¶_______¶____________________________¶¶_______¶
__¶______¶________________________________¶_____¶
___¶____¶__________________________________¶___¶
__¶¶___¶____________________________________¶___¶
__¶_¶¶¶______________________________________¶_¶
_¶___¶________________________________________¶¶_¶
_¶________________¶¶¶¶¶¶____¶¶¶¶¶¶______________¶_¶
¶__¶____________¶¶¶¶¶¶¶¶____¶¶¶¶¶¶¶¶____________¶_¶
¶__¶__________¶¶__¶¶¶¶¶¶____¶¶¶____¶¶¶¶_________¶_¶
¶_¶¶________¶¶¶_¶¶¶__¶¶¶____¶¶___¶¶¶_¶¶¶_________¶_¶
¶_¶¶________¶¶_¶¶¶¶¶¶_¶______¶_¶¶¶¶¶¶¶¶_¶_______¶¶_¶
¶_¶¶______¶__¶_¶¶¶¶_¶¶________¶¶_¶¶¶¶¶_¶__¶_____¶¶_¶
¶_¶¶¶____¶¶¶_¶¶_¶¶¶_¶¶¶______¶¶¶__¶¶¶_¶_¶_¶____¶¶¶_¶
¶_¶_¶____¶_¶¶__¶___¶¶¶________¶¶¶___¶__¶¶_¶____¶_¶_¶
¶_¶¶_¶__¶___¶¶___¶¶¶¶¶________¶¶¶¶¶___¶¶¶__¶__¶__¶_¶
_¶_¶_¶_¶¶___¶¶¶¶_¶¶¶¶¶________¶¶¶¶__¶¶¶¶___¶____¶_¶
__¶_¶_¶¶______¶¶__¶¶_¶________¶¶¶__¶¶¶___¶__¶¶¶¶_¶
___¶¶¶¶____¶___¶¶____¶________¶___¶¶¶___¶______¶
_____¶¶¶¶______¶¶____¶________¶___¶¶¶_______¶¶
_______¶¶¶¶____¶¶___¶__________¶___¶¶______¶
_________¶¶____¶¶___¶__________¶___¶¶____¶¶
___________¶¶_¶¶¶___¶__________¶___¶¶_¶¶¶
______________¶_¶___¶__________¶___¶_¶
_______________¶¶___¶__________¶___¶¶
________________¶___¶_¶¶¶¶¶¶¶¶_¶___¶
________________¶___¶¶¶¶¶¶¶¶¶¶¶¶___¶
_________________¶__¶¶¶¶¶¶¶¶¶¶¶¶__¶
__________________¶_¶¶¶¶¶¶¶¶¶¶¶¶_¶
__________________¶___¶¶¶¶¶¶¶¶___¶
___________________¶___¶¶¶¶¶¶___¶
____________________¶__________¶
_____________________¶¶¶¶¶¶¶¶¶¶


comandos disponiveis: 
    - /help: exibe os comandos disponiveis
    - /quit: sai do servidor
    - /list: lista os clientes conectados
    - /send <client_id> <message>: envia uma mensagem para um cliente específico
    - /send <message>: envia uma mensagem para todos os clientes conectados
"""

    def start_server():
        # Create a TCP/IP socket
        server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # Bind the socket to the address and port
        server_socket.bind((HOST_IP, int(PORT)))

        # Listen for incoming connections
        server_socket.listen(1)
        print(f"Server is listening on {HOST_IP}:{PORT}")

        while True:
            # Wait for a connection
            client_socket, client_address = server_socket.accept()
            print(f"Connection from {client_address} has been established.")

            # Armazenar o cliente conectado
            connected_clients.append((client_socket, client_address))

            # Handle the client connection in a separate thread
            client_thread = threading.Thread(
                target=handle_client, args=(client_socket, client_address))
            client_thread.start()

    def process_command(command):
        # Placeholder function to process commands received from clients
        if command == "/help":
            return "Available commands: /help, /quit, /list, /send <client_id> <message>, /send <message>"
        elif command == "/quit":
            return quit()
        elif command == "/list":
            if not connected_clients:
                return "No clients connected."
            else:
                client_list = "\n".join(
                    [f"{i}: {addr}" for i, (_, addr) in enumerate(connected_clients)])
                return f"Connected clients:\n{client_list}"
        elif command.startswith("/send "):
            parts = command.split(" ", 2)
            if len(parts) == 3:
                client_id = parts[1]
                message = parts[2]
                if send_message_to_client(client_id, message):
                    return f"Message sent to client {client_id}: {message}"
                else:
                    return f"Invalid client ID: {client_id}"
            elif len(parts) == 2:
                message = parts[1]
                send_message_to_all_clients(message)
                return f"Message sent to all clients: {message}"
            else:
                return "Invalid /send command. Use /send <client_id> <message> or /send <message>"
        else:
            return "Unknown command. Type /help for a list of available commands."

    def handle_client(client_socket, client_address):
        # Send a welcome message to the client

        welcome_message = (
            f"Welcome to the Command & Control Server! \n{banner()}"
        )
        client_socket.sendall(welcome_message.encode())

        while True:
            try:
                # Receive data from the client
                data = client_socket.recv(1024).decode()
                if not data:
                    break  # Client has disconnected

                # Process the received command
                response = process_command(data)
                client_socket.sendall(response.encode())
            except Exception as e:
                print(f"Error handling client: {e}")
                break

        # Remover o cliente da lista quando desconectar
        if (client_socket, client_address) in connected_clients:
            connected_clients.remove((client_socket, client_address))

        # Close the client socket
        client_socket.close()

    def send_message_to_client(client_id, message):
        try:
            idx = int(client_id)
            if 0 <= idx < len(connected_clients):
                client_socket, _ = connected_clients[idx]
                client_socket.sendall(message.encode())
                return True
            else:
                return False
        except (ValueError, OSError):
            return False

    def send_message_to_all_clients(message):
        for client_socket, _ in connected_clients:
            try:
                client_socket.sendall(message.encode())
            except OSError:
                pass  # Ignore errors for disconnected clients
        return True

    def quit():
        """Close all client connections and shut down the server."""
        for client_socket, _ in connected_clients:
            client_socket.close()
        print("Server is shutting down. Good Bye!")
        exit(0)
