import csv
import hashlib #Fornece algoritmos de hash seguros
import os
import hmac # Fornece comparações seguras 
import uuid  # Importado para gerar IDs únicos

usuariosCsv = 'usuarios.csv'
# Define o cabeçalho do arquivo CSV
CSV_HEADER = ['id', 'nome', 'sal', 'hash_senha']

# Função para garantir que o arquivo CSV exista e tenha o cabeçalho
def inicializar_csv():
    if not os.path.exists(usuariosCsv):
        with open(usuariosCsv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)

# Função para criar o hash das senhas com sal e PBKDF2
def hash_senha(senha, sal):
    return hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), sal, 100000)

# Registrar um novo usuário no arquivo CSV com ID único
def RegistrarUsuario():
    print('\n----Registro de novo usuário----')
    NomeUsuario = input("Digite o nome do usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # Pula o cabeçalho
            for linha in reader:
                # Agora o nome do usuário está na segunda coluna (índice 1)
                if linha and linha[1] == NomeUsuario:
                    print("Erro: Usuário já existe! Tente outro nome.")
                    return
    except (FileNotFoundError, StopIteration):
        # Se o arquivo não existe ou está vazio (além do cabeçalho), continua
        pass

    # Gerando ID único
    id_usuario = str(uuid.uuid4())
    
    # Criando o sal
    sal = os.urandom(16)

    # Criando o hash da senha
    hashed = hash_senha(senha, sal)

    # Salvando o ID, usuário, sal e hash no CSV
    with open(usuariosCsv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([id_usuario, NomeUsuario, sal.hex(), hashed.hex()])

    print("Usuário registrado com sucesso!")

# Autenticar usuário
def login():
    print("\n----Login de Usuário----")
    NomeUsuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader) # Pula o cabeçalho
            for linha in reader:
                # Colunas ajustadas para a nova estrutura: id, nome, sal, hash
                if linha and linha[1] == NomeUsuario:
                    stored_sal_hex = linha[2]
                    stored_hash_hex = linha[3]

                    stored_hash = bytes.fromhex(stored_hash_hex)
                    sal = bytes.fromhex(stored_sal_hex)

                    # Recalcular o hash com a senha informada
                    inputhash = hash_senha(senha, sal)

                    # Comparação segura
                    if hmac.compare_digest(stored_hash, inputhash):
                        print(f"Seja bem-vindo(a), {NomeUsuario}!")
                        return True
                    else:
                        print("Senha incorreta. Tente novamente.")
                        return False
            
            print("Usuário não encontrado.")
            return False

    except (FileNotFoundError, StopIteration):
        print("Nenhum usuário cadastrado. Por favor registre-se primeiro.")
        return False

# Função para alterar nome de usuário e senha
def alterarUsuario():
    print("\n----Alteração de Dados do Usuário----")
    nome_alvo = input("Digite o nome do usuário que deseja alterar: ")

    usuarios = []
    usuario_encontrado = False
    
    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            # Lê todos os usuários para a memória (incluindo o cabeçalho)
            usuarios = list(reader)

        # Verifica se o arquivo tem conteúdo além do cabeçalho
        if len(usuarios) <= 1:
            print("Nenhum usuário cadastrado para alterar.")
            return

        # Itera sobre os usuários (pulando o cabeçalho)
        for i in range(1, len(usuarios)):
            if usuarios[i][1] == nome_alvo:
                usuario_encontrado = True
                print(f"Usuário '{nome_alvo}' encontrado. Deixe em branco para não alterar.")
                
                # Alterar nome de usuário
                novo_nome = input("Digite o novo nome de usuário: ").strip()
                if novo_nome:
                    # Verifica se o novo nome já existe
                    nome_existente = False
                    for j in range(1, len(usuarios)):
                        if usuarios[j][1] == novo_nome:
                            nome_existente = True
                            break
                    if nome_existente:
                        print("Erro: Este nome de usuário já está em uso. A alteração do nome foi cancelada.")
                    else:
                        usuarios[i][1] = novo_nome
                        print("Nome de usuário alterado com sucesso!")

                # Alterar senha
                nova_senha = input("Digite a nova senha: ").strip()
                if nova_senha:
                    novo_sal = os.urandom(16)
                    novo_hash = hash_senha(nova_senha, novo_sal)
                    usuarios[i][2] = novo_sal.hex()
                    usuarios[i][3] = novo_hash.hex()
                    print("Senha alterada com sucesso!")
                
                break # Sai do loop após encontrar e processar o usuário
        
        if not usuario_encontrado:
            print("Usuário não encontrado.")
            return

        # Reescreve o arquivo CSV com os dados atualizados
        with open(usuariosCsv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(usuarios)
            
    except FileNotFoundError:
        print("Nenhum usuário cadastrado.")

# Menu principal
def main():
    inicializar_csv() # Garante que o arquivo CSV exista
    while True:
        print("\nO que você deseja fazer?")
        print("1. Registrar um novo usuário")
        print("2. Fazer login")
        print("3. Alterar dados do usuário")
        print("4. Sair")
        escolha = input("Digite sua escolha (1/2/3/4): ")

        if escolha == "1":
            RegistrarUsuario()
        elif escolha == "2":
            login()
        elif escolha == "3":
            alterarUsuario()
        elif escolha == "4":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
    