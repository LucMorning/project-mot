from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.enum.text import PP_ALIGN
from openpyxl import load_workbook
import os

def create_pptx_report():
    print("Gerando apresentação de slides (PPTX)...")
    prs = Presentation()

    # 1. Slide de Título
    title_slide_layout = prs.slide_layouts[0]
    slide = prs.slides.add_slide(title_slide_layout)
    title = slide.shapes.title
    subtitle = slide.placeholders[1]
    title.text = "Projeto MOTIVA"
    subtitle.text = "Diagnóstico do Cenário Atual (As-Is)\nGestão de CAPEX e Sistemas"

    # 2. Slide de Contexto de Negócio
    bullet_slide_layout = prs.slide_layouts[1]
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Contexto de Negócio: O Peso do CAPEX"
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = "O núcleo de CAPEX é o motor de crescimento e manutenção das concessões."
    p = tf.add_paragraph()
    p.text = "Investimentos de grande escala (Ex: Serra das Araras - R$ 8 bilhões)."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Concessões de longo prazo (até 30 anos) exigem alta governança."
    p.level = 1
    p = tf.add_paragraph()
    p.text = "Decisões atuais impactam décadas de fluxo de caixa."
    p.level = 1

    # 3. Slide de Metodologia
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Metodologia: O Caminho do Diagnóstico"
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = "Análise granular e profunda em 6 passos:"
    steps = [
        "1. Imersão no Negócio (CAPEX)",
        "2. Organização e Cruzamento de Dados (68 Entrevistas)",
        "3. Análise Micro via IA (Termos Técnicos)",
        "4. Mapeamento As-Is (Processos e Regras)",
        "5. Diagnóstico de Falhas (As 'Doenças')",
        "6. Consolidação e Reporte Executivo"
    ]
    for step in steps:
        p = tf.add_paragraph()
        p.text = step
        p.level = 1

    # 4. Slide de Sistemas (Fragmentação)
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Cenário de Sistemas: Fragmentação e Silos"
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = "Principais sistemas identificados nas entrevistas:"
    systems = ["SAP (ERP/Financeiro)", "Archer (Riscos/Compliance)", "SIC (Investimentos)", "P6/Primavera (Cronograma)", "Excel (A 'Sombra' do Sistema)"]
    for sys in systems:
        p = tf.add_paragraph()
        p.text = sys
        p.level = 1

    # 5. Slide de Diagnóstico - Falhas de Integração
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Diagnóstico: As 'Doenças' do Ecossistema"
    body = slide.placeholders[1]
    tf = body.text_frame
    items = [
        "Falta de integração entre SAP e ferramentas de engenharia.",
        "Dependência crítica de Excel para o acompanhamento físico-financeiro.",
        "Processos manuais de extração de dados gerando retrabalho.",
        "Ineficiência na rastreabilidade de pleitos e medições."
    ]
    for item in items:
        p = tf.add_paragraph()
        p.text = item
        p.level = 0

    # 6. Slide de Evidências Reais (Lendo do XLSX gerado anteriormente)
    if os.path.exists("diagnostico_as_is_detalhado.xlsx"):
        wb = load_workbook("diagnostico_as_is_detalhado.xlsx")
        ws = wb.active
        
        slide = prs.slides.add_slide(bullet_slide_layout)
        slide.shapes.title.text = "Evidências de Campo (Recortes Micro)"
        body = slide.placeholders[1]
        tf = body.text_frame
        tf.clear()
        
        # Pegar as 5 primeiras evidências significativas
        count = 0
        for row in ws.iter_rows(min_row=2, max_row=10, values_only=True):
            if row[2] and len(row[2]) > 50:
                p = tf.add_paragraph()
                p.text = f'"{row[2][:120]}..."'
                p.font.italic = True
                p.font.size = Pt(14)
                p2 = tf.add_paragraph()
                p2.text = f"- {row[0]} ({row[1]})"
                p2.font.size = Pt(12)
                p2.space_after = Pt(10)
                count += 1
                if count >= 4: break

    # 7. Slide Próximos Passos
    slide = prs.slides.add_slide(bullet_slide_layout)
    slide.shapes.title.text = "Próximos Passos"
    body = slide.placeholders[1]
    tf = body.text_frame
    tf.text = "Preparação para o desenho do 'To-Be':"
    next_steps = [
        "Consolidação das regras de negócio por sistema.",
        "Mapeamento detalhado dos fluxos de 'Req to Pay'.",
        "Apresentação do diagnóstico para Diretoria de CAPEX."
    ]
    for ns in next_steps:
        p = tf.add_paragraph()
        p.text = ns
        p.level = 1

    # Salvar
    output_file = "Report_Diagnostico_AsIs_MOTIVA.pptx"
    prs.save(output_file)
    print(f"Apresentação gerada com sucesso: {output_file}")

if __name__ == "__main__":
    create_pptx_report()
