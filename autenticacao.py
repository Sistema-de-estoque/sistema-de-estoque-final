import csv
import hashlib
import os
import hmac   

usuariosCsv = 'usuarios.csv'

# Função para criar o hash das senhas com sal e PBKDF2
def hash_senha(senha, sal):
    return hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), sal, 100000)

# Registrar um novo usuário no arquivo CSV
def RegistrarUsuario():
    print('\n----Registro de novo usuário----')
    NomeUsuario = input("Digite o nome do usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='') as file:
            reader = csv.reader(file)
            for linha in reader:
                if linha and linha[0] == NomeUsuario:
                    print("Erro: Usuário já existe! Tente outro nome.")
                    return
    except FileNotFoundError:
        pass

    # Criando o sal
    sal = os.urandom(16)

    # Criando o hash da senha
    hashed = hash_senha(senha, sal)

    # Salvando o usuário, o sal e o hash no CSV
    with open(usuariosCsv, 'a', newline='') as file:
        writer = csv.writer(file)
        writer.writerow([NomeUsuario, sal.hex(), hashed.hex()])

    print("Usuário registrado com sucesso!")

# Autenticar usuário
def login():
    print("\n----Login de Usuário----")
    NomeUsuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='') as file:
            reader = csv.reader(file)
            for linha in reader:
                if linha and linha[0] == NomeUsuario:
                    stored_sal_hex = linha[1]
                    stored_hash_hex = linha[2]

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

    except FileNotFoundError:
        print("Nenhum usuário cadastrado. Por favor registre-se primeiro.")
        return False

# Menu principal
def main():
    while True:
        print("\nO que você deseja fazer?")
        print("1. Registrar um novo usuário")
        print("2. Fazer login")
        print("3. Sair")
        escolha = input("Digite sua escolha (1/2/3): ")

        if escolha == "1":
            RegistrarUsuario()
        elif escolha == "2":
            login()
        elif escolha == "3":
            print("Saindo do programa.")
            break
        else:
            print("Opção inválida. Tente novamente.")

if __name__ == '__main__':
    main()
