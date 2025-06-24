import socket
import sys

# Script ultra-enxuto para enviar um único datagrama UDP.
# Uso: python3 udp_send.py <IP_DO_ALVO> <PORTA> "<MENSAGEM>"

if len(sys.argv) != 4:
    print(f"Uso: {sys.argv[0]} <IP> <PORTA> \"<MENSAGEM>\"")
    sys.exit(1) # Encerra se os argumentos estiverem incorretos

# Pega os argumentos da linha de comando.
HOST = sys.argv[1]
PORT = int(sys.argv[2])
MESSAGE = sys.argv[3].encode('utf-8') # Codifica a mensagem para bytes

# Cria o socket, envia a mensagem e fecha. Sem laços, sem esperas.
try:
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        s.sendto(MESSAGE, (HOST, PORT))
        # print("Pacote enviado.") # Descomente para confirmação visual
except Exception as e:
    print(f"Erro ao enviar pacote: {e}")