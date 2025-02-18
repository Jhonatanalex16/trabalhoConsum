import threading  # Módulo para trabalhar com threads
import queue      # Módulo para fila segura entre threads
import time       # Para simular tempo de execução
import random     # Para gerar tempos aleatórios

# Tamanho máximo da fila de impressão
TAMANHO_MAXIMO_FILA = 5

# Número máximo permitido de produtores e consumidores
LIMITE_MAX_PRODUTORES = 5
LIMITE_MAX_CONSUMIDORES = 5

# Criação da fila de impressão compartilhada
fila_impressao = queue.Queue(TAMANHO_MAXIMO_FILA)

# Lista global de threads de produtores e consumidores
produtores = []
consumidores = []

# Objeto para sincronizar a saída e evitar mistura com o menu
lock_saida = threading.Lock()

def produtor(id_produtor):
    for i in range(1, 6):  # Cada produtor cria 5 trabalhos
        trabalho = f"Trabalho {i} do Produtor {id_produtor}"
        fila_impressao.put(trabalho)  # Adiciona o trabalho na fila
        with lock_saida:
            print(f"Produtor {id_produtor} adicionou: {trabalho}")
        time.sleep(random.random())  # Simula tempo de criação do trabalho

def consumidor(id_consumidor):
    while True:
        trabalho = fila_impressao.get()
        if trabalho is None:
            fila_impressao.task_done()
            break
        with lock_saida:
            print(f"Consumidor {id_consumidor} processando: {trabalho}")
        time.sleep(random.random())  # Simula tempo de processamento
        fila_impressao.task_done()

def iniciar_sistema(num_produtores, num_consumidores):
    global produtores, consumidores
    produtores = []
    consumidores = []
    
    for i in range(num_produtores):
        thread_produtor = threading.Thread(target=produtor, args=(i,))
        produtores.append(thread_produtor)
        thread_produtor.start()
    
    for i in range(num_consumidores):
        thread_consumidor = threading.Thread(target=consumidor, args=(i,))
        consumidores.append(thread_consumidor)
        thread_consumidor.start()
    
    # Aguarda a conclusão dos produtores
    for thread_produtor in produtores:
        thread_produtor.join()

    # Aguarda a fila ser esvaziada antes de continuar
    fila_impressao.join()

    # Envia sinais para os consumidores pararem
    for _ in consumidores:
        fila_impressao.put(None)

    # Aguarda consumidores terminarem
    for thread_consumidor in consumidores:
        thread_consumidor.join()

    print("\nSistema finalizado! Retornando ao menu...\n")

def obter_valor_numerico(mensagem, limite):
    while True:
        try:
            valor = int(input(mensagem))
            if 1 <= valor <= limite:
                return valor
            print(f"O número deve estar entre 1 e {limite}.")
        except ValueError:
            print("Por favor, insira um número válido.")

def menu():
    while True:
        print("\n--- MENU ---")
        print(f"1. Iniciar sistema (Máximo {LIMITE_MAX_PRODUTORES} produtores e {LIMITE_MAX_CONSUMIDORES} consumidores)")
        print("2. Sair")
        escolha = input("Escolha uma opção: ")
        
        if escolha == "1":
            num_produtores = obter_valor_numerico(f"Digite o número de produtores (máximo {LIMITE_MAX_PRODUTORES}): ", LIMITE_MAX_PRODUTORES)
            num_consumidores = obter_valor_numerico(f"Digite o número de consumidores (máximo {LIMITE_MAX_CONSUMIDORES}): ", LIMITE_MAX_CONSUMIDORES)
            iniciar_sistema(num_produtores, num_consumidores)
        elif escolha == "2":
            print("Saindo...")
            break
        else:
            print("Opção inválida! Tente novamente.")

if __name__ == "__main__":
    menu()
