import csv
import os

from modulos.gestao_produtos import listar_produtos, CABECALHO, CAMINHO_ARQUIVO

# Este módulo também vai precisar saber onde estão os dados
CAMINHO_ARQUIVO_PRODUTOS = os.path.join('dados', 'produtos.csv')
# Futuramente, vocês terão um CAMINHO_ARQUIVO_ESTOQUE para o estoque.csv com lotes

def registrar_saida():
    """Função principal para dar baixa em um produto do estoque."""
    print("\n--- Registrar Saída de Produto ---")
    
    #
    # AQUI ENTRA A LÓGICA DO SEU GRUPO:
    # 1. Pedir o código do produto e a quantidade.
    # 2. Verificar se o produto existe.
    # 3. Verificar se a quantidade em estoque é suficiente.
    # 4. Abater a quantidade do estoque.
    # 5. Salvar a alteração no CSV.
    # 6. Registrar a operação em um log.
    #
    
    print("Funcionalidade de retirada ainda não implementada.")
    input("\nPressione Enter para voltar ao menu...")

def registrar_entrada():
    print("\n--- Registrar Entrada de Produto ---")
    listar_produtos()
    codigo_ou_nome = input("\nDigite o Código ou Nome do produto que deseja dar entrada: ")

    try:
        produtos = []
        produto_encontrado = False
        with open(CAMINHO_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                produtos.append(linha)

        for produto in produtos:
            if produto['Codigo'] == codigo_ou_nome or produto['Nome'].lower() == codigo_ou_nome.lower():
                print(f"\nProduto encontrado: {produto['Nome']} (Qtd atual: {produto['Quantidade']})")

                while True:
                    try:
                        entrada = int(input("Digite a quantidade a adicionar: "))
                        if entrada < 1:
                            print("❌ A quantidade deve ser maior que zero.")
                            continue
                        break
                    except ValueError:
                        print("❌ Digite um número válido.")

                produto['Quantidade'] = str(int(produto['Quantidade']) + entrada)
                produto_encontrado = True
                break

        if produto_encontrado:
            with open(CAMINHO_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=CABECALHO)
                escritor.writeheader()
                escritor.writerows(produtos)
            print("\n Entrada registrada com sucesso!")
        else:
            print("\n Produto não encontrado.")

    except FileNotFoundError:
        print("\n Nenhum produto cadastrado.")

    input("\nPressione Enter para voltar ao menu...")