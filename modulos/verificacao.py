import csv
import time
import os
import threading
from tkinter import messagebox, Tk

# Caminho do arquivo CSV
NOME_ARQUIVO_CSV = os.path.join('dados', 'produtos.csv')

# Intervalo entre verificações (em segundos)
INTERVALO_VERIFICACAO_SEGUNDOS = 10

# Conjunto para rastrear produtos já alertados
produtos_alertados = set()

# Lock para evitar leitura simultânea
lock = threading.Lock()


def emitir_alerta(produto):
   
   # Exibe uma janela de alerta em uma thread separada.
    
    def _mostrar_alerta():
        root = Tk()
        root.withdraw()  # Oculta a janela principal
        root.attributes('-topmost', True)
        messagebox.showwarning(
            "⚠️ Alerta de Estoque Baixo!",
            f"Produto: {produto['Nome']}\n"
            f"Quantidade Atual: {produto['Quantidade']}\n"
            f"Estoque Mínimo: {produto['EstoqueMin']}"
        )
        
        root.destroy()

    # Thread para exibir a janela sem travar o programa
    thread_alerta = threading.Thread(target=_mostrar_alerta, daemon=True)
    thread_alerta.start()

def exibir_mensagem(titulo,mensagem):
    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo(titulo,mensagem)
    root.destroy()

def verificar_estoque():
    
   # Lê o CSV e verifica produtos com estoque abaixo do mínimo.
    
    with lock:
        try:
            with open(NOME_ARQUIVO_CSV, mode='r', encoding='utf-8') as arquivo_csv:
                leitor_csv = csv.DictReader(arquivo_csv)
                for linha in leitor_csv:
                    try:
                        nome = linha['Nome']
                        quantidade_atual = int(linha['Quantidade'])
                        estoque_minimo = int(linha['EstoqueMin'])

                        if quantidade_atual < estoque_minimo:
                            if nome not in produtos_alertados:
                                produtos_alertados.add(nome)
                                emitir_alerta(linha)
                                #print(f"[!] ALERTA: '{nome}' abaixo do mínimo ({quantidade_atual}/{estoque_minimo})")
                                
                        else:
                            # Se o estoque foi reabastecido, remove do conjunto
                            if nome in produtos_alertados:
                                produtos_alertados.remove(nome)
                                exibir_mensagem("Estoque Normalizado", f"[✔] Produto '{nome}' voltou ao nível normal.")
                                
                                

                    except (ValueError, KeyError) as e:
                        print(f"Erro ao processar linha {linha}: {e}")

        except FileNotFoundError:
            print(f"Erro: arquivo '{NOME_ARQUIVO_CSV}' não encontrado.")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def thread_monitorar_estoque():
    
    # Thread principal que executa a verificação em loop.
   
    while True:
        #print(f"[{time.strftime('%H:%M:%S')}] Verificando estoque...")
        verificar_estoque()
        time.sleep(INTERVALO_VERIFICACAO_SEGUNDOS)


def main():
    #print("Iniciando o monitor de estoque com threads...")
    #print(f"Verificando '{NOME_ARQUIVO_CSV}' a cada {INTERVALO_VERIFICACAO_SEGUNDOS} segundos.")
    #print("Pressione CTRL+C para encerrar.\n")

    try:
        # Inicia a thread de monitoramento
        t = threading.Thread(target=thread_monitorar_estoque, daemon=True)
        t.start()

        # Mantém o programa ativo
        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitor de estoque encerrado pelo usuário.")
        time.sleep(2)
        os.system('cls')
    except Exception as e:
        print(f"Erro crítico: {e}")


if __name__ == "__main__":
    main()





