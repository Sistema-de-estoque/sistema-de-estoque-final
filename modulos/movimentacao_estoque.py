import csv
import os
from datetime import datetime

CAMINHO_ARQUIVO_PRODUTOS = os.path.join('dados', 'produtos.csv')
CAMINHO_ARQUIVO_ESTOQUE = os.path.join('dados', 'estoque.csv')
CABECALHO_ESTOQUE = ['CodigoProduto', 'Lote', 'Quantidade', 'DataValidade']

def inicializar_estoque_csv(): 
    if not os.path.exists(CAMINHO_ARQUIVO_ESTOQUE): 
        with open(CAMINHO_ARQUIVO_ESTOQUE, 'w', newline='', encoding='utf-8') as file:
            escritor = csv.writer(file)
            escritor.writerow(CABECALHO_ESTOQUE)

def registrar_entrada():
    print("\n--- Registrar Entrada de lote no estoque ---")
    codigo = input("\nDigite o Código do produto que deseja dar entrada: ")
    lote = input('Digite o número do lote:')

    while True: 
        try: 
            quantidade = int(input("Digite a quantidade de unidades "))
        
            if quantidade > 0: 
                break 
            else: 
                print("A quantidade deve ser um número maior que 0.")
        except ValueError: 
            print("Entrada inválida. Por favor digite um número inteiro.")

    
    while True: 
        try: 
            validade_str = input("Digite a data de validade (DD/MM/AAAA): ")
            datetime.strptime(validade_str, '%d/%m/%Y')
            break 
        except ValueError: 
            print("Data ou formato inválido! Use DD/MM/AAAA")

    
    try: 
        with open(CAMINHO_ARQUIVO_ESTOQUE, 'a', newline='', encoding='utf-8') as file: 
            escritor = csv.writer(file)
            escritor.writerow([codigo, lote, quantidade, validade_str])
        
        print("\nEntrada no lote registrada com sucesso.")
    
    except Exception: 
        print("\nErro ao salvar os dados")
    
    input("\nPressione enter para voltar ao menu...")


def registrar_saida():
    print("\n--- Registrar Saída de Produto do Estoque ---")
    
    codigo = input("\nDigite o Código do produto para a retirada: ")
    
    try:
        quantidade_desejada = int(input("Digite a quantidade a ser retirada: "))
        if quantidade_desejada <= 0:
            print("A quantidade deve ser maior que zero.")
            input("\nPressione Enter para voltar ao menu...")
            return
    except ValueError:
        print("Quantidade inválida. Por favor, insira um número inteiro.")
        input("\nPressione Enter para voltar ao menu...")
        return

    lotes_do_produto = buscar_lotes_por_produto(codigo)
    
    if not lotes_do_produto:
        print(f"Produto com código '{codigo}' não encontrado no estoque ou sem quantidade.")
        input("\nPressione Enter para voltar ao menu...")
        return


    total_em_estoque = sum(int(lote['Quantidade']) for lote in lotes_do_produto)
    if total_em_estoque < quantidade_desejada:
        print(f"Estoque insuficiente. Total disponível: {total_em_estoque}, Pedido: {quantidade_desejada}.")
        input("\nPressione Enter para voltar ao menu...")
        return

    estoque_restante_do_produto = aplicar_retirada_fefo(lotes_do_produto, quantidade_desejada)

    atualizar_arquivo_estoque(codigo, estoque_restante_do_produto)

    print(f"\nRetirada de {quantidade_desejada} unidade(s) do produto {codigo} registrada com sucesso!")

    input("Pressione Enter para voltar ao menu...")


def buscar_lotes_por_produto(codigo_produto):
    lotes = []
    try:
        with open(CAMINHO_ARQUIVO_ESTOQUE, 'r', newline='', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                if linha['CodigoProduto'] == codigo_produto:
                    lotes.append(linha)
    except FileNotFoundError:
        return []
    return lotes

def aplicar_retirada_fefo(lotes, quantidade_a_retirar):
    for lote in lotes:
        lote['DataValidadeObj'] = datetime.strptime(lote['DataValidade'], '%d/%m/%Y')
        lote['Quantidade'] = int(lote['Quantidade'])

    lotes.sort(key=lambda x: x['DataValidadeObj'])
    
    quantidade_restante_para_retirar = quantidade_a_retirar
    lotes_que_sobram = []

    for lote in lotes:
        if quantidade_restante_para_retirar <= 0:
            lotes_que_sobram.append(lote)
            continue

        quantidade_neste_lote = lote['Quantidade']
        
        if quantidade_neste_lote >= quantidade_restante_para_retirar:
            lote['Quantidade'] -= quantidade_restante_para_retirar
            quantidade_restante_para_retirar = 0
            if lote['Quantidade'] > 0: 
                lotes_que_sobram.append(lote)
        else:
            quantidade_restante_para_retirar -= quantidade_neste_lote
    for lote in lotes_que_sobram:
        del lote['DataValidadeObj']
        lote['Quantidade'] = str(lote['Quantidade'])

    return lotes_que_sobram

def atualizar_arquivo_estoque(codigo_produto_afetado, novos_lotes_do_produto):
    """Reescreve o arquivo de estoque com as novas quantidades, preservando os outros produtos."""
    todos_os_outros_lotes = []
    
    with open(CAMINHO_ARQUIVO_ESTOQUE, 'r', newline='', encoding='utf-8') as f:
        leitor = csv.DictReader(f)
        for linha in leitor:
            if linha['CodigoProduto'] != codigo_produto_afetado:
                todos_os_outros_lotes.append(linha)
    
    dados_completos_para_salvar = todos_os_outros_lotes + novos_lotes_do_produto

    
    with open(CAMINHO_ARQUIVO_ESTOQUE, 'w', newline='', encoding='utf-8') as f:
        escritor = csv.DictWriter(f, fieldnames=CABECALHO_ESTOQUE)
        escritor.writeheader()
        escritor.writerows(dados_completos_para_salvar)

def calcular_total_estoque(codigo_produto):
    """Soma as quantidades de todos os lotes de um produto no estoque.csv."""
    total = 0
    try:
        with open(CAMINHO_ARQUIVO_ESTOQUE, 'r', newline='', encoding='utf-8') as file:
            leitor = csv.DictReader(file)
            for linha in leitor:
                if linha['CodigoProduto'] == codigo_produto:
                    total += int(linha['Quantidade'])
    except FileNotFoundError:
        return 0
    
    return total