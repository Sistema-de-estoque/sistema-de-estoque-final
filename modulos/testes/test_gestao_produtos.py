import os
import csv
import pytest
from unittest.mock import patch


from modulos import gestao_produtos as gp

# Caminho do CSV temporário para testes
CAMINHO_TESTE = os.path.join('dados', 'teste_produtos.csv')


@pytest.fixture(autouse=True)

#Cria o csv temporário, e remove depois
def setup_teardown():
    os.makedirs('dados', exist_ok=True)
    with open(CAMINHO_TESTE, 'w', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow(gp.CABECALHO)
    gp.CAMINHO_ARQUIVO = CAMINHO_TESTE
    yield
    if os.path.exists(CAMINHO_TESTE):
        os.remove(CAMINHO_TESTE)


def test_inicializar_arquivo_cria_arquivo():
    os.remove(CAMINHO_TESTE)
    gp.inicializar_arquivo()
    assert os.path.exists(CAMINHO_TESTE)
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        header = next(reader)
        assert header == gp.CABECALHO


def test_obter_proximo_codigo_retorna_1_se_arquivo_vazio():
    assert gp.obter_proximo_codigo() == 1


def test_obter_proximo_codigo_incrementa():
    with open(CAMINHO_TESTE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([1, 'Produto1', 'Desc', 'Cat', 'Un', '5', '10'])
    assert gp.obter_proximo_codigo() == 2



def test_adicionar_produto(monkeypatch):
    inputs = iter(['Produto Teste', 'Desc Teste', 'Cat Teste', 'Un Teste', '5', '20'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    gp.adicionar_produto()
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        linhas = list(reader)
        assert len(linhas) == 1
        assert linhas[0]['Nome'] == 'Produto Teste'
        assert linhas[0]['Quantidade'] == '20'

def test_adicionar_produto_campos_invalidos(monkeypatch):
    inputs = iter(['Produto Inválido', 'Desc Teste', 'Cat Teste', 'Un Teste', '-5', 'abc'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    gp.adicionar_produto()
    
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        linhas = list(reader)
        assert len(linhas) == 0, "Produto com campos inválidos não deve ser adicionado"


def test_atualizar_produto(monkeypatch):
    with open(CAMINHO_TESTE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([1, 'Produto1', 'Desc1', 'Cat1', 'Un1', '5', '10'])
    inputs = iter(['1', 'Produto Atualizado', '', '', '', '', '50'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    gp.atualizar_produto()
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        linhas = list(reader)
        assert linhas[0]['Nome'] == 'Produto Atualizado'
        assert linhas[0]['Quantidade'] == '50'

def test_atualizar_produto_inexistente(monkeypatch):
   
    inputs = iter(['99', 'Novo Nome', '', '', '', '', '20'])  
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    
    gp.atualizar_produto()
    
  
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        linhas = list(reader)
        assert len(linhas) == 0, "Nenhum produto deve ser alterado se o código não existe"



def test_deletar_produto(monkeypatch):
    with open(CAMINHO_TESTE, 'a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        writer.writerow([1, 'Produto1', 'Desc1', 'Cat1', 'Un1', '5', '10'])
    inputs = iter(['1'])
    monkeypatch.setattr('builtins.input', lambda _: next(inputs))
    gp.deletar_produto()
    with open(CAMINHO_TESTE, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        linhas = list(reader)
        assert len(linhas) == 0
