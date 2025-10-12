import csv 
from fpdf import FPDF
from datetime import datetime
from pathlib import Path 

from modulos.gestao_produtos import ler_todos_produtos
from modulos.movimentacao_estoque import ler_todos_lotes, calcular_total_estoque

def relatorio_inventario():
    print("Gerando relatório de inventario completo...")

    todos_produtos = ler_todos_produtos()
    todos_lotes = ler_todos_lotes()

    if not todos_produtos: 
        print("Nenhum produto cadastrado no estoque para gerar relatório.")
        input("Pressione ENTER para voltar ao menu...")
        return 

    exportar = input("Deseja exportar o Relatório detalhado para PDF ? (s/n)").lower()
    if  exportar == 's': 
        exportar_inventario(todos_produtos, todos_lotes)


def exportar_inventario(produtos, lotes):
    pdf = FPDF()
    pdf.add_page()


    pdf.set_font("Arial", 'B', 18) 
    pdf.cell(0, 10, "Relatório de Inventario Completo", ln=True, align='C')

    pdf.set_font("Arial", '', 10)
    data_hoje = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
    pdf.cell(0, 10, f"Gerado em {data_hoje}", ln=True, align='C')
    pdf.ln(10)

    for produto in produtos: 
        pdf.set_font("Arial", 'B', 12)
        pdf.cell(0, 10, f"Produto: {produto['Nome']} (Cod: {produto['Codigo']})", ln=True, border='B')

        lotes_deste_produto = [l for l in lotes if l['CodigoProduto'] == produto['Codigo']]
        
        if not lotes_deste_produto:
            pdf.set_font("Arial", 'I', 10)
            pdf.cell(0, 10, "   - Sem lotes registrados no estoque.", ln=True)
        else:
            pdf.set_font("Arial", 'B', 10)
            pdf.cell(60, 8, 'Lote', border=1, align='C')
            pdf.cell(60, 8, 'Quantidade', border=1, align='C')
            pdf.cell(60, 8, 'Data de Validade', border=1, align='C', ln=True)

            
            pdf.set_font("Arial", '', 10)
            for lote in lotes_deste_produto:
                pdf.cell(60, 8, lote['Lote'], border=1)
                pdf.cell(60, 8, str(lote['Quantidade']), border=1, align='C')
                pdf.cell(60, 8, lote['DataValidade'], border=1, align='C', ln=True)
        
        pdf.ln(10) 

    try:
        download_path = Path.home() / "Downloads"

        nome_arquivo = "relatorio_inventario.pdf"

        caminho_completo = download_path/ nome_arquivo 

        pdf.output(caminho_completo)

        print(f"\nRelatorio '{nome_arquivo}' gerado com sucesso na sua pasta de Downloads!")
        print(f"   Caminho: {caminho_completo}")
        
    except Exception as e:
        print(f"\nErro ao gerar o PDF: {e}")

#RELATÓRIO DE NIVEL CRÍTICO

def obter_produto_critico(): 
    produtos_criticos = []
    catalogo_produtos = ler_todos_produtos()

    if not catalogo_produtos: 
        return [] 
    
    for produto in catalogo_produtos: 
        try: 
            codigo = produto['Codigo']
            estoque_minimo = int(produto['EstoqueMin'])
            quantidade_real = calcular_total_estoque(codigo)

            if quantidade_real <= estoque_minimo: 
                produto['QuantidadeReal'] = quantidade_real
                produtos_criticos.append(produto)
        except(ValueError, KeyError): 
            continue
    return produtos_criticos

def relatorio_nivel_critico():
    print("\n--- Relatório de Produtos em Nível Crítico ---")

    lista_criticos = obter_produto_critico()

    if not lista_criticos:
        print("\nÓtima notícia! Nenhum produto em nível crítico de estoque.")
    else:
        print("\nATENÇÃO! Os seguintes produtos precisam de reposição urgente:")
        for produto in lista_criticos:
            print(
                f"  - Código: {produto['Codigo']}, "
                f"Nome: {produto['Nome']} | "
                f"Estoque Atual: {produto['QuantidadeReal']} | "
                f"Estoque Mínimo: {produto['EstoqueMin']}"
            )
        
        exportar = input("\nDeseja exportar este relatório para PDF? (s/n): ").lower()
        if exportar == 's':
            exportar_relatorio_critico_pdf(lista_criticos)

    input("\nPressione Enter para voltar ao menu...")

def exportar_relatorio_critico_pdf(produtos_criticos):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", 'B', 16)
    
    pdf.cell(0, 10, "Relatorio de Produtos em Nivel Critico", border=1, ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    data_hoje = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
    pdf.cell(0, 10, f"Gerado em: {data_hoje}", ln=True, align='C')
    pdf.ln(10)  
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(25, 10, 'Codigo', border=1, align='C')
    pdf.cell(80, 10, 'Nome do Produto', border=1, align='C')
    pdf.cell(30, 10, 'Est. Atual', border=1, align='C')
    pdf.cell(30, 10, 'Est. Minimo', border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    for produto in produtos_criticos:
        pdf.cell(25, 10, str(produto['Codigo']), border=1, align='C')
        pdf.cell(80, 10, produto['Nome'], border=1)
        pdf.cell(30, 10, str(produto['QuantidadeReal']), border=1, align='C')
        pdf.cell(30, 10, str(produto['EstoqueMin']), border=1, align='C', ln=True)
        
    try:
        downloads_path = Path.home() / "Downloads"
        nome_arquivo = "relatorio_nivel_critico.pdf"
        caminho_completo = downloads_path / nome_arquivo
        pdf.output(caminho_completo)
        
        print(f"\nRelatorio '{nome_arquivo}' gerado com sucesso na sua pasta de Downloads!")
        print(f"   Caminho: {caminho_completo}")
        
    except Exception as e:
        print(f"\nErro ao gerar o PDF: {e}")


def lote_prox_vencimento(dias_limite): 
    print(f"Verificando os lotes que vencem nos próximos {dias_limite} dias")
    lotes_criticos = []

    todos_produtos = ler_todos_produtos()

    mapa_produtos = {produto['Codigo']: produto['Nome'] for produto in todos_produtos}

    todos_lotes = ler_todos_lotes()

    if not todos_lotes: 
        return []
    
    data_hoje = datetime.now()

    for lote in todos_lotes: 
        try: 
            data_vencimento = datetime.strptime(lote['DataValidade'], '%d/%m/%Y')

            diferenca = data_vencimento - data_hoje
            dias_para_vencer = diferenca.days

            if 0 <= dias_para_vencer <= dias_limite: 
                lote['DiasParaVencer'] = dias_para_vencer
                lote['NomeProduto'] = mapa_produtos.get(lote['CodigoProduto'], 'Produto não encontrado')
                lotes_criticos.append(lote)
        except(ValueError, KeyError): 
            continue

    lotes_criticos.sort(key=lambda x: x['DiasParaVencer'])

    return lotes_criticos

def relatorio_prox_vencimento(): 
    print("----------Relatório de produtos próximo ao vencimento.----------")

    try: 
        dias = int(input("Verificar produtos que vencem no próximos quantos dias ? (ex:30): ")) 
    except ValueError: 
        print("Período inválido. Por favor, insira um número.")
        input("\nPressione Enter para voltar ao menu.") 
        return
    
    lista_lotes_criticos = lote_prox_vencimento(dias)

    if not lista_lotes_criticos: 
        print(f"\nNenhum produto irá vencer nos próximos {dias} dias.")
    else: 
        print(f"\nATENÇÃO! Os seguintes lotes irão vencer nos próximos {dias} dias:")
        for lote in lista_lotes_criticos: 
            print(
                f"  - Produto: {lote['NomeProduto']} (Cód: {lote['CodigoProduto']}) | "
                f"Lote: {lote['Lote']} | "
                f"Quantidade: {lote['Quantidade']} | "
                f"Vence em: {lote['DataValidade']} ({lote['DiasParaVencer']} dias)"
            )
        exportar = input("\nDeseja exportar este relatório para PDF? (s/n): ").lower()
        if exportar == 's':
            exportar_relatorio_vencimento_pdf(lista_lotes_criticos, dias)

def exportar_relatorio_vencimento_pdf(lotes_criticos, dias_limite):
    pdf = FPDF()
    pdf.add_page(orientation='L') 
    pdf.set_font("Arial", 'B', 16)
    
    pdf.cell(0, 10, f"Relatorio de Lotes Vencendo nos Proximos {dias_limite} Dias", border=1, ln=True, align='C')
    
    pdf.set_font("Arial", '', 10)
    data_hoje = datetime.now().strftime("%d/%m/%Y as %H:%M:%S")
    pdf.cell(0, 10, f"Gerado em: {data_hoje}", ln=True, align='C')
    pdf.ln(5)
    
    pdf.set_font("Arial", 'B', 10)
    pdf.cell(80, 10, 'Nome do Produto', border=1, align='C')
    pdf.cell(40, 10, 'Lote', border=1, align='C')
    pdf.cell(30, 10, 'Quantidade', border=1, align='C')
    pdf.cell(40, 10, 'Data Venc.', border=1, align='C')
    pdf.cell(40, 10, 'Dias Restantes', border=1, align='C', ln=True)
    
    pdf.set_font("Arial", '', 10)
    for lote in lotes_criticos:
        pdf.cell(80, 10, lote['NomeProduto'], border=1)
        pdf.cell(40, 10, lote['Lote'], border=1)
        pdf.cell(30, 10, str(lote['Quantidade']), border=1, align='C')
        pdf.cell(40, 10, lote['DataValidade'], border=1, align='C')
        pdf.cell(40, 10, str(lote['DiasParaVencer']), border=1, align='C', ln=True)
        
    try:
        downloads_path = Path.home() / "Downloads"
        nome_arquivo = "relatorio_proximo_vencimento.pdf"
        caminho_completo = downloads_path / nome_arquivo
        pdf.output(caminho_completo)
        
        print(f"\nRelatorio '{nome_arquivo}' gerado com sucesso na sua pasta de Downloads!")
        print(f"Caminho: {caminho_completo}")
        
    except Exception as e:
        print(f"\nErro ao gerar o PDF: {e}")