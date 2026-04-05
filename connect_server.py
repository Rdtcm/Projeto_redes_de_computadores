import socket

# Configurações para conectar ao seu servidor
TCP_IP = '127.0.0.1' 
TCP_PORTA = 10352      
TAMANHO_BUFFER = 1024

# 1. Criação do socket
cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    # 2. Conecta ao servidor APENAS UMA VEZ antes do loop 
    cliente.connect((TCP_IP, TCP_PORTA))
    print(f"[*] Conectado com sucesso ao servidor {TCP_IP}:{TCP_PORTA}")

    while True:
        # 3. Solicita a mensagem dentro do loop para enviar várias vezes [cite: 17]
        mensagem = input("\nDigite o comando (ou /quit para sair): ")

        if not mensagem:
            continue

        # 4. Envia a mensagem para o servidor
        cliente.send(mensagem.encode('UTF-8'))

        # Condição de saída baseada no protocolo do seu servidor [cite: 17]
        if mensagem.lower() == '/quit':
            break

        # 5. Recebe a resposta do servidor [cite: 11]
        data = cliente.recv(TAMANHO_BUFFER)
        
        if not data:
            print("[!] Conexão perdida com o servidor.")
            break

        print(f"[RESPOSTA]: {data.decode('UTF-8')}")

except ConnectionRefusedError:
    print("[ERRO] Não foi possível conectar. O servidor está rodando?") [cite: 13]
except Exception as e:
    print(f"[ERRO] Ocorreu uma falha: {e}")
finally:
    # 6. Fecha a conexão de forma limpa ao sair
    cliente.close()
    print("[*] Conexão encerrada.")
