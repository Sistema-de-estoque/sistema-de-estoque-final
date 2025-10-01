# app.py

import os
import csv

# Importa os módulos que criamos
from modulos import gestao_produtos
from modulos import movimentacao_estoque

def inicializar_arquivo():
    """Cria o arquivo CSV com o cabeçalho se ele não existir."""
    caminho = gestao_produtos.CAMINHO_ARQUIVO
    cabecalho = gestao_produtos.CABECALHO
    
    # Cria a pasta 'dados' se ela não existir
    os.makedirs('dados', exist_ok=True)

    if not os.path.exists(caminho):
        with open(caminho, 'w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(cabecalho)

def main():
    """Função principal que exibe o menu e gerencia as operações."""
    inicializar_arquivo()

    while True:
        print("\n--- Sistema de Controle de Estoque Hospitalar ---")
        print("\n[ Gestão de Produtos ]")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Deletar Produto")
        print("\n[ Movimentação de Estoque ]")
        print("5. Registrar ENTRADA de produto")
        print("6. Registrar SAÍDA de produto") # <- A FUNÇÃO DO SEU GRUPO
        print("\n[ Opções ]")
        print("0. Sair")

        escolha = input(">> Escolha uma opção: ")

        if escolha == '1':
            gestao_produtos.adicionar_produto()
        elif escolha == '2':
            gestao_produtos.listar_produtos()
        elif escolha == '3':
            gestao_produtos.atualizar_produto()
        elif escolha == '4':
            gestao_produtos.deletar_produto()
        elif escolha == '5':
            movimentacao_estoque.registrar_entrada()
        elif escolha == '6':
            movimentacao_estoque.registrar_saida() # Chamando a função do seu grupo
        elif escolha == '0':
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

# Garante que o programa principal só será executado quando este script for o arquivo principal
if __name__ == "__main__":
    main()