import argparse
import subprocess
import sys
from pathlib import Path
from time import sleep

ROOT = Path(__file__).resolve().parent
SCRIPTS = {
    "tcp-server": ROOT / "tcp_server.py",
    "tcp-client": ROOT / "tcp_client.py",
    "udp-server": ROOT / "udp_server.py",
    "udp-client": ROOT / "udp_client.py",
}


def run_script(script_name: str, stdin_text: str | None = None) -> int:
    script_path = SCRIPTS[script_name]
    command = [sys.executable, str(script_path)]

    if stdin_text is not None:
        result = subprocess.run(
            command,
            cwd=str(ROOT),
            input=stdin_text,
            text=True,
            capture_output=False,
        )
    else:
        result = subprocess.run(command, cwd=str(ROOT))

    return result.returncode


def main():


    # Questao A
    print("Questao A")
    print("Running TCP Client...")
    run_script("tcp-client", stdin_text="Hello, TCP Server!")
    sleep(15)
    print("Running TCP Server...")
    run_script("tcp-server")

    # Questao B
    print("\nQuestao B")
    print("Running UDP Client...")
    run_script("udp-client")
    sleep(15)
    print("Running UDP Server...")
    run_script("udp-server")


    # Questao C
    print("\nQuestao C")
    


