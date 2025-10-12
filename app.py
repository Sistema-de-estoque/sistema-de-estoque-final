from modulos import gestao_produtos, movimentacao_estoque, autenticacao, relatorios

def menu_principal():
    """Esta função contém o loop do menu principal da aplicação."""
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
        print("\n[ Relatórios ]")
        print("7. Relatório de Inventário Completo")
        print("8. Relatório de produtos em nível crítico")
        print("9.Relatório de produtos próximo ao vencimento")
        print("\n[ Opções ]")
        print("0. Sair (Logout)")

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
            movimentacao_estoque.registrar_saida()
        elif escolha == '7':
            relatorios.relatorio_inventario()
        elif escolha == '8': 
            relatorios.relatorio_nivel_critico()
        elif escolha == '9': 
            relatorios.relatorio_prox_vencimento()
        elif escolha == '0':
            print("\nFazendo logout...")
            break
        else:
            print("\nOpção inválida. Tente novamente.")

def main():
    """Função principal que gerencia o estado do programa (logado ou não)."""
    while True:
        usuario_logado = autenticacao.main() 

        if usuario_logado:
            print(f"\nBem-vindo(a), {usuario_logado}!")
            menu_principal()
        else:
            print("\nSaindo do sistema. Até logo!")
            break

if __name__ == "__main__":
    main()