"""
Excel Reports Generator - MOTIVA AS IS Analysis

Gera Excel com layout profissional e visualizações executivas.

ABAS:
1. DASHBOARD - Métricas chave
2. MATRIZ_DORES - Mapa de calor dores x sistema
3. MAPA_AREA - Distribuição por área
4. REDE - Stakeholders com cargo
5. WORKAROUNDS - Gaps identificados
6. OPORTUNIDADES - Por sistema
7. LEGENDA - Glossário de termos
8. TO_BE - Esqueleto soluções
"""
import sqlite3
import pandas as pd
from pathlib import Path
from datetime import datetime
from openpyxl import load_workbook
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.drawing.image import Image
from openpyxl.utils import get_column_letter

from src.config import DB_PATH, EXCEL_OUTPUT_DIR, PROJECT_ROOT

# Descrições para a Legenda de Dores
PAIN_POINTS_LEGEND = {
    'ETL Humano': 'Extração manual de dados de um sistema para planilhas ou outros sistemas (Copy-Paste).',
    'Silo de Informação': 'Dados que existem em apenas um sistema e não são compartilhados, gerando ilhas de informação.',
    'Divergência de Dados': 'Conflito entre fontes de dados (ex: SAP vs Spreadsheet), quebrando a Verdade Única.',
    'Lacuna de Processo': 'Etapas da cadeia de valor que não possuem sistema de apoio, sendo feitas por e-mail ou memórias.',
    'Baixa Confiabilidade': 'Dados imprecisos ou falta de integridade que impede a tomada de decisão executiva.',
    'Gargalo de Acesso': 'Dificuldade técnica ou burocrática para acessar informações críticas em tempo real.',
    'Trabalho Paralelo': 'Sistemas que não atendem as necessidades para o dia a dia, forçando o uso de ferramentas "sombra".',
    'Falta de Ferramenta': 'O processo é gerido fora de sistemas oficiais por ausência de módulo ou software específico.',
}


# ─────────────────────────────────────────────────────────────
# ESTILOS PROFISSIONAIS
# ─────────────────────────────────────────────────────────────

def apply_header_style(ws, cell_range):
    """Aplica estilo de cabeçalho profissional."""
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    for row in ws[cell_range]:
        for cell in row:
            cell.font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
            cell.fill = PatternFill(start_color='5E45E8', end_color='5E45E8', fill_type='solid')
            cell.alignment = Alignment(horizontal='center', vertical='center', wrap_text=True)
            cell.border = thin_border


def apply_data_style(ws, start_row, end_row=None, min_col=1, max_col=None):
    """Aplica estilo aos dados apenas no range especificado."""
    thin_border = Border(
        left=Side(style='thin'),
        right=Side(style='thin'),
        top=Side(style='thin'),
        bottom=Side(style='thin')
    )

    actual_max_col = max_col if max_col else ws.max_column

    for row in ws.iter_rows(min_row=start_row, max_row=end_row, min_col=min_col, max_col=actual_max_col):
        for cell in row:
            # Não aplicar se a célula é parte de um merge mas não é a principal (opcional, dependendo do openpyxl)
            cell.font = Font(name='Calibri', size=10)
            cell.alignment = Alignment(horizontal='left', vertical='center', wrap_text=True)
            cell.border = thin_border


def apply_severity_colors(ws, col_letter, start_row):
    """Aplica cores baseadas na severidade/críticas."""
    for row in range(start_row, ws.max_row + 1):
        cell = ws[f'{col_letter}{row}']
        if cell.value:
            try:
                val_str = str(cell.value).upper()
                if 'ALTO' in val_str or 'ALTA' in val_str or (isinstance(cell.value, (int, float)) and cell.value > 0):
                    cell.fill = PatternFill(start_color='FFCDD2', end_color='FFCDD2', fill_type='solid')
                elif 'MEDIO' in val_str or 'MEDIA' in val_str:
                    cell.fill = PatternFill(start_color='FFF9C4', end_color='FFF9C4', fill_type='solid')
                elif 'BAIXO' in val_str or 'BAIXA' in val_str:
                    cell.fill = PatternFill(start_color='C8E6C9', end_color='C8E6C9', fill_type='solid')
            except:
                pass


def auto_adjust_columns(ws):
    """Ajusta largura das colunas."""
    for column in ws.columns:
        max_length = 0
        column_letter = get_column_letter(column[0].column)
        for cell in column:
            try:
                if len(str(cell.value)) > max_length:
                    max_length = len(str(cell.value))
            except:
                pass
        adjusted_width = min(max_length + 2, 50)
        ws.column_dimensions[column_letter].width = adjusted_width


# ─────────────────────────────────────────────────────────────
# DADOS
# ─────────────────────────────────────────────────────────────

def get_dashboard_data(conn):
    """Retorna métricas executivas do dashboard."""
    df_metricas = pd.read_sql_query("""
        SELECT
            'Total Entrevistados' as metrica,
            COUNT(DISTINCT e.id) as valor
        FROM stg_entrevistados e
        WHERE EXISTS (SELECT 1 FROM fato_insights i WHERE i.id_entrevistado = e.id)

        UNION ALL

        SELECT
            'Total Insights',
            COUNT(*)
        FROM fato_insights

        UNION ALL

        SELECT
            'Dores Críticas (Alta Severidade)',
            COUNT(*)
        FROM fato_insights
        WHERE severidade = 'Alto'

        UNION ALL

        SELECT
            'Sistemas Mapeados',
            COUNT(DISTINCT id_sistema)
        FROM fato_sistemas_uso

        UNION ALL

        SELECT
            'Stakeholders Mapeados',
            COUNT(DISTINCT pessoa_citada)
        FROM fato_relacoes

        UNION ALL

        SELECT
            'Workarounds Ativos',
            COUNT(*)
        FROM fato_sistemas_uso
        WHERE workaround IS NOT NULL
            AND workaround != ''
            AND LOWER(workaround) NOT IN ('nenhum', 'n/a', 'nao', 'none', '-')
    """, conn)

    # Por área para MAPA_AREA
    df_area = pd.read_sql_query("""
        SELECT
            e.area,
            COUNT(DISTINCT e.id) as entrevistados,
            COUNT(DISTINCT i.id) as insights,
            COUNT(DISTINCT CASE WHEN i.severidade = 'Alto' THEN i.id END) as criticas
        FROM stg_entrevistados e
        LEFT JOIN fato_insights i ON i.id_entrevistado = e.id
        WHERE e.area IS NOT NULL
        GROUP BY e.area
        ORDER BY insights DESC
    """, conn)

    return df_metricas, df_area


def get_matriz_dores_por_etapa(conn):
    """Retorna dados para matriz dores x sistema - separado por etapa."""
    df = pd.read_sql_query("""
        SELECT
            i.subcategoria as dor,
            TRIM(j.value) as sistema,
            COUNT(*) as ocorrencias,
            SUM(CASE WHEN i.severidade = 'Alto' THEN 1 ELSE 0 END) as criticas
        FROM fato_insights i
        LEFT JOIN dim_cadeia_valor cv ON i.id_etapa_cadeia = cv.id
        LEFT JOIN json_each(i.sistemas_envolvidos) as j ON j.value IS NOT NULL
        WHERE cv.nome IS NOT NULL AND TRIM(j.value) != ''
        GROUP BY i.subcategoria, TRIM(j.value)
        ORDER BY ocorrencias DESC
    """, conn)
    return df


def get_rede_stakeholders(conn):
    """Retorna rede de stakeholders."""
    df = pd.read_sql_query("""
        SELECT
            e1.nome as de,
            e1.cargo as cargo_de,
            e1.area as area_de,
            r.tipo as tipo_relacao,
            COALESCE(e2.nome, r.pessoa_citada) as para,
            COALESCE(e2.cargo, 'N/A') as cargo_para,
            COUNT(*) as vezes_citado
        FROM fato_relacoes r
        JOIN stg_entrevistados e1 ON r.id_entrevistado = e1.id
        LEFT JOIN stg_entrevistados e2 ON LOWER(TRIM(r.pessoa_citada)) = LOWER(TRIM(e2.nome))
        GROUP BY e1.nome, e2.nome, r.tipo
        ORDER BY vezes_citado DESC
    """, conn)
    return df


def get_workarounds(conn):
    """Retorna workarounds identificados."""
    df = pd.read_sql_query("""
        SELECT
            ds.nome as sistema,
            fs.workaround as alternativa,
            e.area as area,
            COUNT(DISTINCT e.id) as usuarios
        FROM fato_sistemas_uso fs
        JOIN dim_sistemas ds ON fs.id_sistema = ds.id
        JOIN stg_entrevistados e ON fs.id_entrevistado = e.id
        WHERE fs.workaround IS NOT NULL
            AND fs.workaround != ''
            AND LOWER(fs.workaround) NOT IN ('nenhum', 'n/a', 'nao', 'none', '-')
        GROUP BY ds.nome, fs.workaround, e.area
        ORDER BY usuarios DESC
    """, conn)
    return df


def get_oportunidades(conn):
    """Retorna oportunidades por sistema."""
    df = pd.read_sql_query("""
        SELECT
            TRIM(j.value) as sistema,
            cv.nome as etapa,
            i.subcategoria as problema,
            i.risco_estimado as impacto,
            COUNT(DISTINCT e.id) as pessoas_afetadas
        FROM fato_insights i
        JOIN stg_entrevistados e ON i.id_entrevistado = e.id
        LEFT JOIN dim_cadeia_valor cv ON i.id_etapa_cadeia = cv.id
        LEFT JOIN json_each(i.sistemas_envolvidos) as j ON j.value IS NOT NULL
        WHERE TRIM(j.value) != '' AND TRIM(j.value) IS NOT NULL
        GROUP BY TRIM(j.value), cv.nome, i.subcategoria, i.risco_estimado
        ORDER BY pessoas_afetadas DESC
    """, conn)
    return df


# ─────────────────────────────────────────────────────────────
# GERADOR PRINCIPAL
# ─────────────────────────────────────────────────────────────

def generate_excel_report(output_path: str = None) -> str:
    """Gera Excel com layout profissional."""

    if output_path is None:
        output_path = EXCEL_OUTPUT_DIR / f"motiva_as_is_{datetime.now().strftime('%Y%m%d_%H%M%S')}.xlsx"

    output_path = Path(output_path)
    output_path.parent.mkdir(parents=True, exist_ok=True)

    conn = sqlite3.connect(DB_PATH)

    with pd.ExcelWriter(output_path, engine='openpyxl') as writer:
        # 1. MATRIZ DORES (UMA LINHA POR ETAPA, TABELAS POR DOR LADO A LADO)
        print("  [EXCEL] MATRIZ DORES...")
        df_metricas_dummy, df_area = get_dashboard_data(conn)
        df_legenda = pd.DataFrame([
            {"Tipo": k, "Descrição": v} for k, v in PAIN_POINTS_LEGEND.items()
        ])
        df_legenda.to_excel(
            writer, sheet_name='MATRIZ_DORES',
            startrow=2, startcol=0, index=False
        )

        df_matriz = pd.read_sql_query("""
            SELECT
                cv.id as etapa_id,
                cv.nome as etapa,
                i.subcategoria as dor,
                TRIM(j.value) as sistema,
                COUNT(*) as ocorrencias,
                SUM(CASE WHEN i.severidade = 'Alto' THEN 1 ELSE 0 END) as criticas
            FROM fato_insights i
            LEFT JOIN dim_cadeia_valor cv ON i.id_etapa_cadeia = cv.id
            LEFT JOIN json_each(i.sistemas_envolvidos) as j ON j.value IS NOT NULL
            WHERE cv.nome IS NOT NULL AND TRIM(j.value) != ''
            GROUP BY cv.id, cv.nome, i.subcategoria, TRIM(j.value)
            ORDER BY cv.id, ocorrencias DESC
        """, conn)

        start_row = 12 # Começar as matrizes abaixo da legenda
        for etapa_id in sorted(df_matriz['etapa_id'].unique()):
            df_etapa_master = df_matriz[df_matriz['etapa_id'] == etapa_id]
            etapa_nome = df_etapa_master['etapa'].iloc[0]

            pd.DataFrame([[f"{etapa_id}. {etapa_nome}"]]).to_excel(
                writer, sheet_name='MATRIZ_DORES',
                startrow=start_row, startcol=0, header=False, index=False
            )
            start_row += 1

            start_col = 0
            max_rows_in_this_etapa = 0
            for dor_nome, df_dor_group in df_etapa_master.groupby('dor', sort=False):
                df_sub = df_dor_group[['sistema', 'ocorrencias', 'criticas']].rename(
                    columns={'criticas': 'Críticas'}
                )
                pd.DataFrame([[dor_nome.upper()]]).to_excel(
                    writer, sheet_name='MATRIZ_DORES',
                    startrow=start_row, startcol=start_col, header=False, index=False
                )
                df_sub.to_excel(
                    writer, sheet_name='MATRIZ_DORES',
                    startrow=start_row + 1, startcol=start_col, index=False
                )
                max_rows_in_this_etapa = max(max_rows_in_this_etapa, len(df_sub) + 2)
                start_col += 4
            start_row += max_rows_in_this_etapa + 3

        # 2. SHEETS ADICIONAIS
        print("  [EXCEL] MAPA POR ÁREA...")
        df_area.to_excel(writer, sheet_name='MAPA_AREA', startrow=1, index=False)

        # 4. REDE STAKEHOLDERS
        print("  [EXCEL] REDE STAKEHOLDERS...")
        df_rede = get_rede_stakeholders(conn)
        df_rede.to_excel(writer, sheet_name='REDE_STAKEHOLDERS', startrow=1, index=False)

        # 5. WORKAROUNDS
        print("  [EXCEL] WORKAROUNDS...")
        df_work = get_workarounds(conn)
        df_work.to_excel(writer, sheet_name='WORKAROUNDS', startrow=1, index=False)

        # 6. OPORTUNIDADES
        print("  [EXCEL] OPORTUNIDADES...")
        df_oport = get_oportunidades(conn)
        df_oport.to_excel(writer, sheet_name='OPORTUNIDADES', startrow=1, index=False)

        # 7. TO_BE
        print("  [EXCEL] TO_BE...")
        df_to_be = pd.DataFrame(columns=['sistema', 'etapa', 'problema', 'solucao','tipo','prioridade','esforco','beneficio','responsavel','prazo','status'])
        df_to_be.to_excel(writer, sheet_name='TO_BE', startrow=1, index=False)

    # APLICAR FORMATAÇÃO
    print("  [EXCEL] Formatando...")
    wb = load_workbook(output_path)
    for sheet_name in wb.sheetnames:
        ws = wb[sheet_name]
        title_text = f"MOTIVA - {sheet_name.replace('_', ' ').upper()}"

        # Estilo do Titulo (Coluna B em diante se tiver logo, ou A se não tiver)
        title_cell_start = 'A1'
        
        # Tentar inserir Logo (CÁLCULO PRECISO DE CENTRALIZAÇÃO VIA EMU)
        logo_path = PROJECT_ROOT / "assets" / "motiva.png"
        if logo_path.exists():
            from openpyxl.drawing.spreadsheet_drawing import OneCellAnchor, AnchorMarker
            from openpyxl.drawing.xdr import XDRPositiveSize2D
            from openpyxl.utils.units import pixels_to_EMU
            
            try:
                img = Image(str(logo_path))
                # Manter proporção original
                ratio = img.width / img.height if img.height else 1
                target_h_px = 30
                target_w_px = target_h_px * ratio
                
                # Dimensões da célula A1 em pixels (aproximadas para CALIBRI 11)
                # Unidades Excel: Width (chars) ~ 7px, Height (points) ~ 1.33px
                cell_w_px = 22 * 7.5
                cell_h_px = 45 * 1.33
                
                # Cálculo de Offsets em Pixels -> EMUs (1px = 9525 EMUs)
                off_x_emu = pixels_to_EMU(max(0, (cell_w_px - target_w_px) // 2))
                off_y_emu = pixels_to_EMU(max(0, (cell_h_px - target_h_px) // 2))
                
                # Criar Anchor com Offsets de centralização
                marker = AnchorMarker(col=0, colOff=off_x_emu, row=0, rowOff=off_y_emu)
                size = XDRPositiveSize2D(pixels_to_EMU(target_w_px), pixels_to_EMU(target_h_px))
                img.anchor = OneCellAnchor(_from=marker, ext=size)
                
                ws.column_dimensions['A'].width = 22
                ws.row_dimensions[1].height = 45
                
                ws.add_image(img)
                title_cell_start = 'B1' # Desloca titulo
            except:
                pass

        ws[title_cell_start] = title_text
        ws[title_cell_start].font = Font(name='Calibri', size=16, bold=True, color='5E45E8')
        ws[title_cell_start].alignment = Alignment(horizontal='center', vertical='center')

        # Mesclar título (sempre até uma largura razoável)
        last_col_idx = max(ws.max_column, 15)
        if last_col_idx > (1 if title_cell_start == 'A1' else 2):
            ws.merge_cells(f'{title_cell_start}:{get_column_letter(last_col_idx)}1')

        header_row = 2
        data_row = 3
        if ws.max_row >= header_row:
            if sheet_name == 'MATRIZ_DORES':
                # AJUSTE DE COLUNAS GERAL (Compacto)
                ws.column_dimensions['A'].width = 25
                ws.column_dimensions['B'].width = 10
                # Gaps estreitos e sem bordas
                for col_idx in [4, 8, 12, 16, 20]:
                    ws.column_dimensions[get_column_letter(col_idx)].width = 2
                
                # Formatação cirúrgica da Legenda (Linhas 3-11)
                # Header Legenda
                apply_header_style(ws, 'A3:B3')
                # Pintar apenas B do merge para a borda aparecer? (Melhor borda manual)
                for r_idx in range(3, 12):
                    for c_idx in range(1, 16):
                        cell = ws.cell(row=r_idx, column=c_idx)
                        if c_idx == 1 or (c_idx >= 2 and c_idx <= 15):
                            # Estilos manuais para evitar leak
                            if r_idx == 3: # Header
                                cell.fill = PatternFill(start_color='5E45E8', end_color='5E45E8', fill_type='solid')
                                cell.font = Font(name='Calibri', size=11, bold=True, color='FFFFFF')
                            else:
                                cell.font = Font(name='Calibri', size=10)
                            
                            # Bordas apenas no contorno do merge e em A
                            if c_idx == 1:
                                cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                            elif c_idx == 2: # Início do merge
                                cell.border = Border(left=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                            elif c_idx == 15: # Fim do merge
                                cell.border = Border(right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                            elif c_idx > 2 and c_idx < 15:
                                cell.border = Border(top=Side(style='thin'), bottom=Side(style='thin'))

                # Formatação das Matrizes (Linha 12+)
                for r in ws.iter_rows(min_row=12):
                    for cell in r:
                        # Detectar Header de Sub-tabela (Dor)
                        if cell.value and str(cell.value).lower() in ['sistema', 'ocorrencias', 'críticas']:
                            col = cell.column
                            row = cell.row
                            apply_header_style(ws, f'{get_column_letter(col)}{row}:{get_column_letter(col+2)}{row}')
                            
                            # Título da Dor (acima)
                            if row > 12:
                                above = ws.cell(row=row-1, column=col)
                                if above.value and str(above.value).isupper():
                                    above.font = Font(name='Calibri', size=11, bold=True)
                                    above.alignment = Alignment(horizontal='center')
                                    ws.merge_cells(start_row=row-1, start_column=col, end_row=row-1, end_column=col+2)
                                    # Pintar header da dor
                                    for c_i in range(col, col+3):
                                        ws.cell(row=row-1, column=c_i).fill = PatternFill(start_color='E8EAF6', end_color='E8EAF6', fill_type='solid')

                            # Colunas compactas de métricas
                            if str(cell.value).lower() in ['ocorrencias', 'críticas']:
                                ws.column_dimensions[get_column_letter(col)].width = 10

                            # Dados ABAIXO (Apenas as 3 colunas)
                            data_r = row + 1
                            while ws.cell(row=data_r, column=col).value is not None:
                                for c_idx in range(col, col + 3):
                                    d_cell = ws.cell(row=data_r, column=c_idx)
                                    d_cell.font = Font(name='Calibri', size=10)
                                    d_cell.border = Border(left=Side(style='thin'), right=Side(style='thin'), top=Side(style='thin'), bottom=Side(style='thin'))
                                    d_cell.alignment = Alignment(horizontal='left')
                                
                                crit_cell = ws.cell(row=data_r, column=col+2)
                                if crit_cell.value and isinstance(crit_cell.value, (int, float)) and crit_cell.value > 0:
                                    crit_cell.fill = PatternFill(start_color='FFCDD2', end_color='FFCDD2', fill_type='solid')
                                data_r += 1

                        # Título da Etapa
                        if cell.value and cell.column == 1 and str(cell.value)[0].isdigit() and '. ' in str(cell.value):
                            cell.font = Font(name='Calibri', size=14, bold=True, color='5E45E8')
                            # Sem bordas aqui
                            cell.border = Border()
                            # Merge cauteloso (não aplica bordas extras)
                            ws.merge_cells(start_row=cell.row, start_column=1, end_row=cell.row, end_column=20)

            else:
                apply_header_style(ws, f'A{header_row}:{get_column_letter(ws.max_column)}{header_row}')
                apply_data_style(ws, data_row)
                auto_adjust_columns(ws)
                ws.freeze_panes = f'A{data_row}'
                for col in range(1, ws.max_column + 1):
                    cell_value = ws.cell(row=header_row, column=col).value
                    if cell_value and any(k in str(cell_value).lower() for k in ['severidade', 'impacto', 'altas', 'críticas']):
                        apply_severity_colors(ws, get_column_letter(col), data_row)
                apply_header_style(ws, f'A{header_row}:{get_column_letter(ws.max_column)}{header_row}')
                apply_data_style(ws, data_row)
                auto_adjust_columns(ws)
                ws.freeze_panes = f'A{data_row}'
                for col in range(1, ws.max_column + 1):
                    cell_value = ws.cell(row=header_row, column=col).value
                    if cell_value and any(k in str(cell_value).lower() for k in ['severidade', 'impacto', 'altas', 'críticas']):
                        apply_severity_colors(ws, get_column_letter(col), data_row)

    wb.save(output_path)
    conn.close()
    print(f"\n[DONE] Excel gerado: {output_path}")
    return str(output_path)


def main():
    generate_excel_report()


if __name__ == "__main__":
    main()
