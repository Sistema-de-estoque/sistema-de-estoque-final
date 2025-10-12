# modulos/autenticacao.py

import csv
import hashlib
import os
import hmac
import uuid

usuariosCsv = os.path.join('dados','usuarios.csv')
CSV_HEADER = ['id', 'nome', 'sal', 'hash_senha']

def inicializar_csv():
    os.makedirs('dados', exist_ok=True)
    if not os.path.exists(usuariosCsv):
        with open(usuariosCsv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(CSV_HEADER)

def hash_senha(senha, sal):
    return hashlib.pbkdf2_hmac('sha256', senha.encode('utf-8'), sal, 100000)

def RegistrarUsuario():
    print('\n----Registro de novo usuário----')
    NomeUsuario = input("Digite o nome do usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for linha in reader:
                if linha and linha[1] == NomeUsuario:
                    print("Erro: Usuário já existe! Tente outro nome.")
                    return
    except (FileNotFoundError, StopIteration):
        pass

    id_usuario = str(uuid.uuid4())
    sal = os.urandom(16)
    hashed = hash_senha(senha, sal)

    with open(usuariosCsv, 'a', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        writer.writerow([id_usuario, NomeUsuario, sal.hex(), hashed.hex()])

    print("Usuário registrado com sucesso!")


def login():
    print("\n----Login de Usuário----")
    NomeUsuario = input("Digite o nome de usuário: ")
    senha = input("Digite a senha: ")

    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            next(reader)
            for linha in reader:
                if linha and linha[1] == NomeUsuario:
                    stored_sal_hex = linha[2]
                    stored_hash_hex = linha[3]
                    stored_hash = bytes.fromhex(stored_hash_hex)
                    sal = bytes.fromhex(stored_sal_hex)
                    inputhash = hash_senha(senha, sal)

                    if hmac.compare_digest(stored_hash, inputhash):
                        return NomeUsuario 
                    else:
                        print("Senha incorreta. Tente novamente.")
                        return None 
            
            print("Usuário não encontrado.")
            return None

    except (FileNotFoundError, StopIteration):
        print("Nenhum usuário cadastrado. Por favor registre-se primeiro.")
        return None

def alterarUsuario():
    print("\n----Alteração de Dados do Usuário----")
    nome_alvo = input("Digite o nome do usuário que deseja alterar: ")

    usuarios = []
    usuario_encontrado = False
    
    try:
        with open(usuariosCsv, 'r', newline='', encoding='utf-8') as file:
            reader = csv.reader(file)
            usuarios = list(reader)

        if len(usuarios) <= 1:
            print("Nenhum usuário cadastrado para alterar.")
            return

        for i in range(1, len(usuarios)):
            if usuarios[i][1] == nome_alvo:
                usuario_encontrado = True
                print(f"Usuário '{nome_alvo}' encontrado. Deixe em branco para não alterar.")
                
                novo_nome = input("Digite o novo nome de usuário: ").strip()
                if novo_nome:
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

                nova_senha = input("Digite a nova senha: ").strip()
                if nova_senha:
                    novo_sal = os.urandom(16)
                    novo_hash = hash_senha(nova_senha, novo_sal)
                    usuarios[i][2] = novo_sal.hex()
                    usuarios[i][3] = novo_hash.hex()
                    print("Senha alterada com sucesso!")
                
                break 
        
        if not usuario_encontrado:
            print("Usuário não encontrado.")
            return

        with open(usuariosCsv, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerows(usuarios)
            
    except FileNotFoundError:
        print("Nenhum usuário cadastrado.")

def main():
    inicializar_csv()
    while True:
        print("\n--- Menu de Autenticação ---")
        print("1. Fazer login")
        print("2. Registrar um novo usuário")
        print("3. Alterar dados do usuário")
        print("4. Sair do programa")
        escolha = input("Digite sua escolha (1/2/3/4): ")

        if escolha == "1":
            # Tenta fazer o login
            usuario_logado = login()
            if usuario_logado:
                return usuario_logado
        elif escolha == "2":
            RegistrarUsuario()
        elif escolha == "3":
            alterarUsuario()
        elif escolha == "4":
            return None
        else:
            print("Opção inválida. Tente novamente.")

