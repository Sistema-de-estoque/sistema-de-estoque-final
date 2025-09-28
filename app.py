import csv
import os

# Define o nome do arquivo e os cabeçalhos das colunas
NOME_ARQUIVO = 'contatos.csv'
CABECALHO = ['id', 'nome', 'email', 'telefone']

def inicializar_arquivo():
    """Cria o arquivo CSV com o cabeçalho se ele não existir."""
    if not os.path.exists(NOME_ARQUIVO):
        with open(NOME_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
            escritor = csv.writer(arquivo_csv)
            escritor.writerow(CABECALHO)

def obter_proximo_id():
    """Lê o arquivo e retorna o próximo ID disponível."""
    try:
        with open(NOME_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.reader(arquivo_csv)
            # Pula o cabeçalho
            next(leitor, None)
            ultimo_id = 0
            for linha in leitor:
                if linha: # Verifica se a linha não está vazia
                    ultimo_id = int(linha[0])
            return ultimo_id + 1
    except (IOError, StopIteration):
        return 1

# --- CREATE ---
def adicionar_contato():
    """Adiciona um novo contato ao arquivo CSV."""
    print("\n--- Adicionar Novo Contato ---")
    nome = input("Digite o nome: ")
    email = input("Digite o email: ")
    telefone = input("Digite o telefone: ")
    
    novo_id = obter_proximo_id()
    
    with open(NOME_ARQUIVO, 'a', newline='', encoding='utf-8') as arquivo_csv:
        escritor = csv.writer(arquivo_csv)
        escritor.writerow([novo_id, nome, email, telefone])
        
    print("\n✅ Contato adicionado com sucesso!")

# --- READ ---
def listar_contatos():
    """Lê e exibe todos os contatos do arquivo CSV."""
    print("\n--- Lista de Contatos ---")
    try:
        with open(NOME_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            # Usar DictReader para facilitar a leitura por nome da coluna
            leitor = csv.DictReader(arquivo_csv)
            
            # Verifica se há contatos para listar
            contatos_existem = False
            for contato in leitor:
                print(f"ID: {contato['id']}, Nome: {contato['nome']}, Email: {contato['email']}, Telefone: {contato['telefone']}")
                contatos_existem = True
            
            if not contatos_existem:
                print("Nenhum contato cadastrado.")

    except FileNotFoundError:
        print("Nenhum contato cadastrado.")

# --- UPDATE ---
def atualizar_contato():
    """Atualiza as informações de um contato existente."""
    print("\n--- Atualizar Contato ---")
    listar_contatos()
    id_para_atualizar = input("\nDigite o ID do contato que deseja atualizar: ")
    
    try:
        # Lê todos os contatos para a memória
        contatos = []
        with open(NOME_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for linha in leitor:
                contatos.append(linha)

        contato_encontrado = False
        for contato in contatos:
            if contato['id'] == id_para_atualizar:
                print("\nDigite os novos dados (deixe em branco para manter o valor atual):")
                
                novo_nome = input(f"Nome atual: {contato['nome']}\nNovo nome: ")
                novo_email = input(f"Email atual: {contato['email']}\nNovo email: ")
                novo_telefone = input(f"Telefone atual: {contato['telefone']}\nNovo telefone: ")
                
                if novo_nome:
                    contato['nome'] = novo_nome
                if novo_email:
                    contato['email'] = novo_email
                if novo_telefone:
                    contato['telefone'] = novo_telefone
                    
                contato_encontrado = True
                break
        
        if contato_encontrado:
            # Reescreve o arquivo inteiro com os dados atualizados
            with open(NOME_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=CABECALHO)
                escritor.writeheader()
                escritor.writerows(contatos)
            print("\n✅ Contato atualizado com sucesso!")
        else:
            print("\n❌ ID não encontrado.")
            
    except FileNotFoundError:
        print("\n❌ Nenhum contato cadastrado para atualizar.")

# --- DELETE ---
def deletar_contato():
    """Remove um contato do arquivo CSV pelo ID."""
    print("\n--- Deletar Contato ---")
    listar_contatos()
    id_para_deletar = input("\nDigite o ID do contato que deseja deletar: ")
    
    try:
        # Lê todos os contatos, exceto o que será deletado
        contatos_mantidos = []
        contato_deletado = False
        with open(NOME_ARQUIVO, 'r', newline='', encoding='utf-8') as arquivo_csv:
            leitor = csv.DictReader(arquivo_csv)
            for contato in leitor:
                if contato['id'] != id_para_deletar:
                    contatos_mantidos.append(contato)
                else:
                    contato_deletado = True
        
        if contato_deletado:
            # Reescreve o arquivo apenas com os contatos mantidos
            with open(NOME_ARQUIVO, 'w', newline='', encoding='utf-8') as arquivo_csv:
                escritor = csv.DictWriter(arquivo_csv, fieldnames=CABECALHO)
                escritor.writeheader()
                escritor.writerows(contatos_mantidos)
            print("\n✅ Contato deletado com sucesso!")
        else:
            print("\n❌ ID não encontrado.")
            
    except FileNotFoundError:
        print("\n❌ Nenhum contato cadastrado para deletar.")


# --- MENU PRINCIPAL ---
def main():
    """Função principal que exibe o menu e gerencia as operações."""
    inicializar_arquivo()
    
    while True:
        print("\n--- Sistema de Gerenciamento de Contatos (CSV) ---")
        print("1. Adicionar Contato")
        print("2. Listar Contatos")
        print("3. Atualizar Contato")
        print("4. Deletar Contato")
        print("5. Sair")
        
        escolha = input("Escolha uma opção: ")
        
        if escolha == '1':
            adicionar_contato()
        elif escolha == '2':
            listar_contatos()
        elif escolha == '3':
            atualizar_contato()
        elif escolha == '4':
            deletar_contato()
        elif escolha == '5':
            print("\nSaindo do sistema. Até logo!")
            break
        else:
            print("\n❌ Opção inválida. Tente novamente.")

# Garante que o programa principal só será executado quando este script for o arquivo principal
if __name__ == "__main__":
    main()

    