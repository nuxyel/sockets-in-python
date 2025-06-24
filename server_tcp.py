import socket

# --- Configurações do Servidor ---
# Define o endereço IP e a porta em que o servidor irá escutar.
# "0.0.0.0" significa que o servidor aceitará conexões de qualquer interface de rede da máquina.
# Isso é crucial para pentest, pois permite que outras máquinas na rede se conectem, não apenas o localhost.
HOST = "0.0.0.0"
PORT = 4433
LOG_FILE = "server_log.txt"

# --- Função Principal do Servidor ---
def start_server():
    """
    Inicializa e executa o servidor TCP.
    """
    # A declaração 'with' (context manager) é a forma mais segura de trabalhar com sockets.
    # Ela garante que o socket do servidor (server_socket) será fechado automaticamente
    # no final da execução, mesmo que ocorram erros.
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as server_socket:
        # Tenta vincular o socket ao endereço e porta definidos.
        try:
            server_socket.bind((HOST, PORT))
        except OSError as e:
            # Trata erros comuns, como a porta já estar em uso.
            print(f"[ERRO] Falha ao vincular à porta {PORT}: {e}")
            return # Encerra a função se não for possível iniciar o servidor.

        # Coloca o servidor em modo de escuta, aguardando por conexões.
        # O argumento '5' é o 'backlog', o número de conexões não aceitas que o sistema
        # manterá na fila antes de recusar novas conexões.
        server_socket.listen(5)
        print(f"[INFO] Servidor escutando em {HOST}:{PORT}...")

        # --- Laço Principal de Aceitação de Clientes ---
        # Este laço 'while True' é a principal melhoria. Ele faz o servidor rodar
        # indefinidamente, aceitando um cliente após o outro, em vez de fechar após o primeiro.
        while True:
            try:
                # O método .accept() é bloqueante: ele pausa a execução e espera
                # até que um novo cliente se conecte.
                # Quando um cliente se conecta, ele retorna um novo objeto de socket para a comunicação
                # com esse cliente (client_socket) e o endereço do cliente (client_address).
                client_socket, client_address = server_socket.accept()
                
                # A função 'handle_client' será chamada para tratar a nova conexão.
                # Isso organiza o código, separando a lógica de aceitar conexões da lógica
                # de comunicação com cada cliente.
                handle_client(client_socket, client_address)

            except KeyboardInterrupt:
                # Permite que você pare o servidor de forma limpa pressionando Ctrl+C no terminal.
                print("\n[INFO] Servidor encerrado pelo usuário.")
                break
            except Exception as e:
                # Captura outros erros que possam ocorrer no laço de aceitação.
                print(f"[ERRO] Erro ao aceitar conexão: {e}")

def handle_client(client_socket, client_address):
    """
    Gerencia a comunicação com um cliente conectado.
    """
    # A declaração 'with' aqui garante que tanto o socket do cliente quanto o arquivo
    # de log sejam fechados corretamente quando a comunicação com este cliente terminar.
    with client_socket, open(LOG_FILE, "a") as log_file:
        print(f"[CONEXÃO] Conexão recebida de: {client_address[0]}:{client_address[1]}")
        log_file.write(f"--- Nova Conexão de {client_address[0]}:{client_address[1]} ---\n")
        
        # --- Laço de Recebimento de Dados ---
        # Este laço 'while True' permite receber múltiplas mensagens do mesmo cliente,
        # simulando uma sessão contínua ou um shell reverso simples.
        while True:
            try:
                # Tenta receber dados do cliente. O '1024' é o tamanho do buffer em bytes.
                data = client_socket.recv(1024)
                
                # Se 'recv' retornar uma string de bytes vazia, significa que o cliente
                # fechou a conexão de forma limpa.
                if not data:
                    print(f"[DESCONEXÃO] Cliente {client_address[0]} desconectou.")
                    break # Sai do laço de recebimento de dados.

                # Decodifica os dados recebidos (de bytes para string)
                decoded_data = data.decode('utf-8', errors='ignore')
                
                # Imprime os dados no console e os salva no arquivo de log.
                # O 'end=""' evita que o print adicione uma nova linha, mostrando exatamente o que foi recebido.
                print(f"[DADOS DE {client_address[0]}] {decoded_data}", end="")
                log_file.write(decoded_data)
                log_file.flush() # Força a escrita imediata no arquivo, útil para logs em tempo real.
                
                # --- Resposta para o Cliente (Opcional, mas útil) ---
                # Enviar uma confirmação de volta pode ser útil para saber que o servidor está vivo.
                # client_socket.sendall(b"ACK\n") # Exemplo de resposta

            except ConnectionResetError:
                # Ocorre se a conexão for forçadamente fechada pelo cliente.
                print(f"[ERRO] Conexão resetada por {client_address[0]}.")
                break
            except Exception as e:
                # Captura outros erros durante a comunicação.
                print(f"[ERRO] Erro na comunicação com {client_address[0]}: {e}")
                break

# --- Ponto de Entrada do Script ---
# Garante que a função 'start_server()' só será chamada quando o script for executado diretamente.
if __name__ == "__main__":
    start_server()