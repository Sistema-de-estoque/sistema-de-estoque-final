import pytest
from unittest.mock import MagicMock
from datetime import datetime, timedelta
from modulos import relatorios

@pytest.fixture
def mock_produtos():
    return [
        {'Codigo': '1', 'Nome': 'Produto 1', 'Descricao': 'Desc 1', 'Categoria': 'Cat 1', 'Unidade': 'Un', 'EstoqueMin': '5'},
        {'Codigo': '2', 'Nome': 'Produto 2', 'Descricao': 'Desc 2', 'Categoria': 'Cat 2', 'Unidade': 'Un', 'EstoqueMin': '10'}
    ]

@pytest.fixture
def mock_lotes():
    hoje = datetime.now()
    return [
        {
            'CodigoProduto': '1',
            'Lote': 'L001',
            'Quantidade': '10',
            'DataValidade': (hoje + timedelta(days=5)).strftime('%d/%m/%Y'),
            'NomeProduto': 'Produto 1',
            'DiasParaVencer': 5
        },
        {
            'CodigoProduto': '2',
            'Lote': 'L002',
            'Quantidade': '1',
            'DataValidade': (hoje + timedelta(days=10)).strftime('%d/%m/%Y'),
            'NomeProduto': 'Produto 2',
            'DiasParaVencer': 10
        }
    ]


# Teste do relatório de inventário completo
def test_relatorio_inventario_sem_produtos(monkeypatch):
    monkeypatch.setattr("modulos.relatorios.ler_todos_produtos", lambda: [])
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert relatorios.relatorio_inventario() is None

def test_relatorio_inventario_com_exportacao(monkeypatch, mock_produtos, mock_lotes):
    monkeypatch.setattr("modulos.relatorios.ler_todos_produtos", lambda: mock_produtos)
    monkeypatch.setattr("modulos.relatorios.ler_todos_lotes", lambda: mock_lotes)
    monkeypatch.setattr("builtins.input", lambda prompt: "s")
    
    mock_exportar = MagicMock()
    monkeypatch.setattr("modulos.relatorios.exportar_inventario", mock_exportar)

    relatorios.relatorio_inventario()
    mock_exportar.assert_called_once_with(mock_produtos, mock_lotes)

# Teste do relatório de produtos críticos
def test_obter_produto_critico(monkeypatch, mock_produtos):
    monkeypatch.setattr("modulos.relatorios.calcular_total_estoque", lambda codigo: 3 if codigo == '1' else 15)
    monkeypatch.setattr("modulos.relatorios.ler_todos_produtos", lambda: mock_produtos)
    
    criticos = relatorios.obter_produto_critico()
    assert len(criticos) == 1
    assert criticos[0]['Codigo'] == '1'
    assert criticos[0]['QuantidadeReal'] == 3

def test_relatorio_nivel_critico_sem_produtos(monkeypatch):
    monkeypatch.setattr("modulos.relatorios.obter_produto_critico", lambda: [])
    monkeypatch.setattr("builtins.input", lambda _: "")
    assert relatorios.relatorio_nivel_critico() is None

def test_relatorio_nivel_critico_com_exportacao(monkeypatch, mock_produtos):
    criticos_mock = [{'Codigo': '1', 'Nome': 'Produto 1', 'EstoqueMin': '5', 'QuantidadeReal': 3}]
    monkeypatch.setattr("modulos.relatorios.obter_produto_critico", lambda: criticos_mock)
    monkeypatch.setattr("builtins.input", lambda prompt: "s" if "exportar" in prompt.lower() else "")
    
    mock_exportar = MagicMock()
    monkeypatch.setattr("modulos.relatorios.exportar_relatorio_critico_pdf", mock_exportar)

    relatorios.relatorio_nivel_critico()
    mock_exportar.assert_called_once_with(criticos_mock)


# Teste de lote próximo ao vencimento
def test_lote_prox_vencimento(monkeypatch, mock_lotes, mock_produtos):
    monkeypatch.setattr("modulos.relatorios.ler_todos_produtos", lambda: mock_produtos)
    monkeypatch.setattr("modulos.relatorios.ler_todos_lotes", lambda: mock_lotes)

    resultado = relatorios.lote_prox_vencimento(15)
    assert len(resultado) == len(mock_lotes)
    for lote in resultado:
        assert 'DiasParaVencer' in lote
        assert 'NomeProduto' in lote

def test_relatorio_prox_vencimento_sem_lotes(monkeypatch):
    monkeypatch.setattr("modulos.relatorios.lote_prox_vencimento", lambda dias: [])
    monkeypatch.setattr("builtins.input", lambda prompt: "30")
    assert relatorios.relatorio_prox_vencimento() is None

def test_relatorio_prox_vencimento_com_exportacao(monkeypatch, mock_lotes):
    monkeypatch.setattr("modulos.relatorios.lote_prox_vencimento", lambda dias: mock_lotes)
    
    def fake_input(prompt):
        if "exportar" in prompt.lower():
            return "s"
        elif "quantos dias" in prompt.lower():
            return "30"
        return ""
    
    monkeypatch.setattr("builtins.input", fake_input)
    mock_exportar = MagicMock()
    monkeypatch.setattr("modulos.relatorios.exportar_relatorio_vencimento_pdf", mock_exportar)

    relatorios.relatorio_prox_vencimento()
    mock_exportar.assert_called_once_with(mock_lotes, 30)
