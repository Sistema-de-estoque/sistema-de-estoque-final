import os
import csv

from modulos import gestao_produtos
from modulos import movimentacao_estoque



def main():
    gestao_produtos.inicializar_arquivo()
    movimentacao_estoque.inicializar_estoque_csv()

    while True:
        print("\n--- Sistema de Controle de Estoque Hospitalar ---")
        print("\n[ Gestão de Produtos ]")
        print("1. Cadastrar Produto")
        print("2. Listar Produtos")
        print("3. Atualizar Produto")
        print("4. Deletar Produto")
        print("\n[ Movimentação de Estoque ]")
        print("5. Registrar ENTRADA de produto")
        print("6. Registrar SAÍDA de produto")
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
            gestao_produtos.listar_produtos()
            movimentacao_estoque.registrar_entrada()
        elif escolha == '6':
            gestao_produtos.listar_produtos()
            movimentacao_estoque.registrar_saida() # Chamando a função do seu grupo
        elif escolha == '0':
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

# Garante que o programa principal só será executado quando este script for o arquivo principal
if __name__ == "__main__":
    main()