import csv
import time
import os
import threading
from tkinter import messagebox, Tk

# CAMINHOS PARA OS ARQUIVOS COM A NOVA ESTRUTURA 

NOME_ARQUIVO_PRODUTOS = os.path.join('dados', 'produtos.csv') 
NOME_ARQUIVO_ESTOQUE = os.path.join('dados', 'estoque.csv')   

# Intervalo entre verificações (em segundos)
INTERVALO_VERIFICACAO_SEGUNDOS = 2

# Conjunto para rastrear CÓDIGOS de produtos já alertados (usar código é mais seguro que nome)
produtos_alertados = set()

# Lock para evitar leitura simultânea dos arquivos
lock = threading.Lock()


def emitir_alerta(produto):
    
    def _mostrar_alerta():
        root = Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        messagebox.showwarning(
            "⚠️ Alerta de Estoque Baixo!",
            f"Produto: {produto['Nome']}\n"
            f"Quantidade Total: {produto['Quantidade']}\n"
            f"Estoque Mínimo: {produto['EstoqueMin']}"
        )
        root.destroy()

    thread_alerta = threading.Thread(target=_mostrar_alerta, daemon=True)
    thread_alerta.start()

def exibir_mensagem(titulo, mensagem):

    root = Tk()
    root.withdraw()
    root.attributes('-topmost', True)
    messagebox.showinfo(titulo, mensagem)
    root.destroy()

def verificar_estoque():
   
    with lock:
        try:
           
            estoque_agregado = {}
            with open(NOME_ARQUIVO_ESTOQUE, mode='r', encoding='utf-8') as arquivo_estoque:
                leitor_estoque = csv.DictReader(arquivo_estoque)
                for linha in leitor_estoque:
                    try:
                        codigo = linha['CodigoProduto']
                        quantidade = int(linha['Quantidade'])
                        
                        # Se o código já existe no dicionário, soma a quantidade. Se não, cria a entrada.
                        estoque_agregado[codigo] = estoque_agregado.get(codigo, 0) + quantidade

                    except (ValueError, KeyError) as e:
                        print(f"Erro ao processar linha do arquivo de estoque {linha}: {e}")

            # Ler o arquivo de produtos e comparar com o estoque agregado 
            with open(NOME_ARQUIVO_PRODUTOS, mode='r', encoding='utf-8') as arquivo_produtos:
                leitor_produtos = csv.DictReader(arquivo_produtos)
                for produto_info in leitor_produtos:
                    try:
                        codigo_produto = produto_info['Codigo']
                        nome_produto = produto_info['Nome']
                        estoque_minimo = int(produto_info['EstoqueMin'])

                        # Busca a quantidade total no dicionário de estoque que criamos.
                        # Se o produto não está no arquivo de estoque, sua quantidade é 0.
                        
                        quantidade_atual = estoque_agregado.get(codigo_produto, 0)

                        # A lógica de alerta agora usa o CÓDIGO para rastreamento
                        if quantidade_atual < estoque_minimo:
                            if codigo_produto not in produtos_alertados:
                                produtos_alertados.add(codigo_produto)
                                alerta_info = {
                                    'Nome': nome_produto, # O nome é usado apenas para exibição
                                    'Quantidade': quantidade_atual,
                                    'EstoqueMin': estoque_minimo
                                }
                                emitir_alerta(alerta_info)
                        else:
                            # Se o estoque foi reabastecido, remove do conjunto de alertas
                            if codigo_produto in produtos_alertados:
                                produtos_alertados.remove(codigo_produto)
                                exibir_mensagem("Estoque Normalizado", f"[✔] Produto '{nome_produto}' ({codigo_produto}) voltou ao nível normal.")

                    except (ValueError, KeyError) as e:
                        print(f"Erro ao processar linha do arquivo de produtos {produto_info}: {e}")

        except FileNotFoundError as e:
            print(f"Erro: arquivo não encontrado. Verifique se '{e.filename}' existe na pasta 'dados'.")
        except Exception as e:
            print(f"Erro inesperado: {e}")


def thread_monitorar_estoque():
  
    while True:
        verificar_estoque()
        time.sleep(INTERVALO_VERIFICACAO_SEGUNDOS)


def main():
    try:
        if not os.path.exists('dados'):
            os.makedirs('dados')
            print("Pasta 'dados' criada. Por favor, adicione 'produtos.csv' e 'estoque.csv'.")
            
        t = threading.Thread(target=thread_monitorar_estoque, daemon=True)
        t.start()

        while True:
            time.sleep(1)

    except KeyboardInterrupt:
        print("\nMonitor de estoque encerrado pelo usuário.")
        time.sleep(2)
        os.system('cls' if os.name == 'nt' else 'clear')
    except Exception as e:
        print(f"Erro crítico: {e}")


if __name__ == "__main__":
    main()