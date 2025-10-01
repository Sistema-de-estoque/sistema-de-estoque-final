import csv 
import os 

CAMINHO_ARQUIVO = os.path.join('dados', 'produtos.csv')

CABECALHO = ['Codigo', 'Nome', 'Descricao', 'Categoria', 'UnidadeMedida', 'EstoqueMin', 'Quantidade']

def adicionar_produto():
    """Adiciona um novo produto ao arquivo CSV."""
    print("\n--- Adicionar Novo Produto ---")
    nome = input("Digite o nome do produto: ")
    descricao = input("Digite a descrição: ")
    categoria = input("Digite a categoria: ")
    unidade_medida = input("Digite a unidade de medida: ")
    estoque_min = input("Digite o estoque mínimo: ")
    # Adicionada a pergunta para a nova coluna 'Quantidade'
    quantidade = input("Digite a quantidade inicial em estoque: ")

    novo_codigo = obter_proximo_codigo()

    with open(CAMINHO_ARQUIVO, 'a', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        # Adicionado o novo campo 'quantidade' na escrita da linha
        escritor.writerow([novo_codigo, nome, descricao, categoria, unidade_medida, estoque_min, quantidade])

    print("\n✅ Produto adicionado com sucesso!")

def listar_produtos():
    """Lê e exibe todos os produtos do arquivo CSV."""
    print("\n--- Lista de Produtos ---")
    try:
        with open(CAMINHO_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)

            produtos_existem = False
            for produto in leitor:
                print(
                    f"Código: {produto['Codigo']}, "
                    f"Nome: {produto['Nome']}, "
                    f"Descrição: {produto['Descricao']}, "
                    f"Categoria: {produto['Categoria']}, "
                    f"Un. Medida: {produto['UnidadeMedida']}, "
                    f"Estoque Mín.: {produto['EstoqueMin']}, "
                    # Adicionada a exibição do novo campo 'Quantidade'
                    f"Quantidade: {produto['Quantidade']}"
                )
                produtos_existem = True

            if not produtos_existem:
                print("Nenhum produto cadastrado.")

    except FileNotFoundError:
        print("Nenhum produto cadastrado.")

def atualizar_produto():
    """Atualiza as informações de um produto existente."""
    print("\n--- Atualizar Produto ---")
    listar_produtos()
    codigo_para_atualizar = input("\nDigite o Código do produto que deseja atualizar: ")

    try:
        produtos = []
        with open(CAMINHO_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                produtos.append(linha)

        produto_encontrado = False
        for produto in produtos:
            if produto['Codigo'] == codigo_para_atualizar:
                print("\nDigite os novos dados (deixe em branco para manter o valor atual):")

                novo_nome = input(f"Nome atual: {produto['Nome']}\nNovo nome: ")
                nova_descricao = input(f"Descrição atual: {produto['Descricao']}\nNova descrição: ")
                nova_categoria = input(f"Categoria atual: {produto['Categoria']}\nNova categoria: ")
                nova_unidade_medida = input(f"Unidade de Medida atual: {produto['UnidadeMedida']}\nNova Un. Medida: ")
                novo_estoque_min = input(f"Estoque Mín. atual: {produto['EstoqueMin']}\nNovo Estoque Mín.: ")
                # Adicionada a atualização para o novo campo 'Quantidade'
                nova_quantidade = input(f"Quantidade atual: {produto['Quantidade']}\nNova quantidade: ")

                if novo_nome:
                    produto['Nome'] = novo_nome
                if nova_descricao:
                    produto['Descricao'] = nova_descricao
                if nova_categoria:
                    produto['Categoria'] = nova_categoria
                if nova_unidade_medida:
                    produto['UnidadeMedida'] = nova_unidade_medida
                if novo_estoque_min:
                    produto['EstoqueMin'] = novo_estoque_min
                # Adicionada a lógica de atualização para 'Quantidade'
                if nova_quantidade:
                    produto['Quantidade'] = nova_quantidade

                produto_encontrado = True
                break

        if produto_encontrado:
            with open(CAMINHO_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=CABECALHO)
                escritor.writeheader()
                escritor.writerows(produtos)
            print("\n✅ Produto atualizado com sucesso!")
        else:
            print("\n❌ Código não encontrado.")

    except FileNotFoundError:
        print("\n❌ Nenhum produto cadastrado para atualizar.")

def deletar_produto():
    """Remove um produto do arquivo CSV pelo Código."""
    print("\n--- Deletar Produto ---")
    listar_produtos()
    codigo_para_deletar = input("\nDigite o Código do produto que deseja deletar: ")

    try:
        produtos_mantidos = []
        produto_deletado = False
        with open(CAMINHO_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for produto in leitor:
                if produto['Codigo'] != codigo_para_deletar:
                    produtos_mantidos.append(produto)
                else:
                    produto_deletado = True

        if produto_deletado:
            with open(CAMINHO_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=CABECALHO)
                escritor.writeheader()
                escritor.writerows(produtos_mantidos)
            print("\n✅ Produto deletado com sucesso!")
        else:
            print("\n❌ Código não encontrado.")

    except FileNotFoundError:
        print("\n❌ Nenhum produto cadastrado para deletar.")


def obter_proximo_codigo():
    """Lê o arquivo e retorna o próximo Código disponível."""
    try:
        with open(CAMINHO_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            # Pula o cabeçalho
            next(leitor, None)
            ultimo_codigo = 0
            for linha in leitor:
                if linha:  # Verifica se a linha não está vazia
                    ultimo_codigo = int(linha[0])
            return ultimo_codigo + 1
    except (IOError, StopIteration):
        return 1