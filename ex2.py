import socket
import threading


PORT = 10352
IP_CLIENTE = "192.168.15.100"


def chat_servidor_p2p():
    """Servidor para chat P2P - Cliente 1"""
    servidor = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    servidor.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    servidor.bind(('0.0.0.0', PORT))
    servidor.listen(1)

    print("[SERVIDOR] Aguardando conexão...")
    conexao, endereco = servidor.accept()
    print(f"[CONECTADO] Cliente: {endereco}")

    # Thread para receber mensagens
    def receber():
        while True:
            try:
                msg = conexao.recv(1024).decode('UTF-8')
                if msg:
                    print(f"\n{msg}")
                    print("Você: ", end='', flush=True)
            except:
                break

    thread_receber = threading.Thread(target=receber)
    thread_receber.daemon = True
    thread_receber.start()

    # Enviar mensagens
    while True:
        try:
            msg = input("Você: ")
            if msg:
                conexao.send(msg.encode('UTF-8'))
        except KeyboardInterrupt:
            print("\n[ENCERRANDO...]")
            conexao.close()
            break


def chat_cliente_p2p():
    """Cliente para chat P2P - Cliente 2"""
    cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    try:
        cliente.connect((IP_CLIENTE, PORT))
        print("[CONECTADO] Conectado ao servidor")

        # Thread para receber mensagens
        def receber():
            while True:
                try:
                    msg = cliente.recv(1024).decode('UTF-8')
                    if msg:
                        print(f"\n{msg}")
                        print("Você: ", end='', flush=True)
                except:
                    break

        thread_receber = threading.Thread(target=receber)
        thread_receber.daemon = True
        thread_receber.start()

        # Enviar mensagens
        while True:
            try:
                msg = input("Você: ")
                if msg:
                    cliente.send(msg.encode('UTF-8'))
            except KeyboardInterrupt:
                print("\n[ENCERRANDO...]")
                cliente.close()
                break

    except ConnectionRefusedError:
        print("[ERRO] Não consegui conectar ao servidor")

# ========== PARA USAR ==========
# Execute em dois terminais:
# Terminal 1: python -c "from ex2 import chat_servidor_p2p; chat_servidor_p2p()"
# Terminal 2: python -c "from ex2 import chat_cliente_p2p; chat_cliente_p2p()"
#
# OU use os arquivos chat_server.py e chat_client.py para múltiplos clientes
