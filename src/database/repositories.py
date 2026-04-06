import sqlite3
import json
from typing import List, Dict, Optional, Any
from pathlib import Path

from src.config import IntervieweeStatus

class BaseRepository:
    """Classe base para repositórios SQLite."""
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _execute(self, query: str, params: tuple = (), fetch: bool = False) -> Any:
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute(query, params)
            if fetch:
                result = cursor.fetchall()
                conn.close()
                return result
            conn.commit()
            last_id = cursor.lastrowid
            conn.close()
            return last_id
        except Exception as e:
            conn.close()
            print(f"[DATABASE ERROR] {str(e)}")
            print(f"Query: {query}")
            print(f"Params: {params}")
            raise e

    def _extract_params(self, dados: Dict, fields: list, defaults: dict = None) -> tuple:
        """
        Extrai tupla de params de um dict para uso em INSERT/UPDATE.

        Elimina o boilerplate de dados.get('campo') repetido em cada insert().

        Args:
            dados: Dicionário de dados de entrada
            fields: Lista de chaves a extrair, em ordem dos placeholders (?)
            defaults: Valores padrão opcionais {campo: valor_default}
        """
        _defaults = defaults or {}
        return tuple(dados.get(field, _defaults.get(field)) for field in fields)

# ─────────────────────────────────────────────────────────────
# ENTREVISTADOS REPOSITORY
# ─────────────────────────────────────────────────────────────

class EntrevistadosRepository(BaseRepository):
    """Repository para tabela stg_entrevistados (Atores)."""

    def insert(self, dados: Dict) -> int:
        """Insere um novo ator e retorna o ID."""
        query = """
            INSERT INTO stg_entrevistados (
                nome, cargo, diretoria, unidade_negocio, area, nivel,
                dt_entrevista, tipo_entrevista, arquivo_transcricao,
                arquivo_cargo_pdf, status_revisao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        fields = [
            'nome', 'cargo', 'diretoria', 'unidade_negocio', 'area', 'nivel',
            'dt_entrevista', 'tipo_entrevista', 'arquivo_transcricao',
            'arquivo_cargo_pdf', 'status_revisao',
        ]
        return self._execute(query, self._extract_params(dados, fields, {'status_revisao': IntervieweeStatus.PENDING}))

    def get_pending(self, limit: int = 100) -> List[Dict]:
        """Retorna lista de stg_entrevistados com análise pendente."""
        query = """
            SELECT e.id, e.nome, e.cargo, e.unidade_negocio, e.dt_entrevista, t.texto_limpo, e.arquivo_cargo_pdf
            FROM stg_entrevistados e
            JOIN stg_arquivos_transcricao a ON a.id_entrevistado = e.id
            JOIN stg_transcricoes t ON t.id_arquivo_transcricao = a.id
            WHERE e.status_revisao = ?
            LIMIT ?
        """
        rows = self._execute(query, (IntervieweeStatus.PENDING, limit,), fetch=True)
        return [
            {
                'id': r[0], 'nome': r[1], 'cargo': r[2],
                'unidade_negocio': r[3], 'dt_entrevista': r[4],
                'texto': r[5], 'arquivo_cargo_pdf': r[6]
            } for r in rows
        ]

    def update_status(self, entrevistado_id: int, status: str):
        """Atualiza o status de análise de um entrevistado."""
        self._execute(
            "UPDATE stg_entrevistados SET status_revisao = ? WHERE id = ?",
            (status, entrevistado_id)
        )

    def get_all_with_transcricao(self) -> list:
        """Retorna todos os stg_entrevistados que possuem arquivo de transcrição vinculado."""
        rows = self._execute(
            "SELECT id, arquivo_transcricao FROM stg_entrevistados WHERE arquivo_transcricao IS NOT NULL",
            fetch=True
        )
        return [{'id': r[0], 'arquivo_transcricao': r[1]} for r in rows]

# ─────────────────────────────────────────────────────────────
# TRANSCRICOES REPOSITORY
# ─────────────────────────────────────────────────────────────

class TranscricoesRepository(BaseRepository):
    """Repository para tabela stg_transcricoes."""

    def delete_all(self) -> int:
        """Remove todas as transcrições (com CASCADE para chunks)."""
        # Primeiro deleta chunks (dependentes)
        self._execute("DELETE FROM stg_chunks")
        # Depois deleta transcrições
        return self._execute("DELETE FROM stg_transcricoes")

    def insert(self, dados: Dict) -> int:
        """Insere uma transcrição."""
        query = """
            INSERT INTO stg_transcricoes (
                id_entrevistado, texto_completo, texto_limpo,
                dt_gravacao, arquivo_origem
            ) VALUES (?, ?, ?, ?, ?)
        """
        fields = ['id_entrevistado', 'texto_completo', 'texto_limpo', 'dt_gravacao', 'arquivo_origem']
        return self._execute(query, self._extract_params(dados, fields))

# ─────────────────────────────────────────────────────────────
# CARGOS REPOSITORY
# ─────────────────────────────────────────────────────────────

class CargosRepository(BaseRepository):
    """Repository para tabela stg_cargos."""

    def delete_all(self) -> int:
        """Remove todos os stg_cargos."""
        return self._execute("DELETE FROM stg_cargos")

    def insert(self, dados: Dict) -> int:
        """Insere um cargo."""
        query = """
            INSERT INTO stg_cargos (
                titulo_cargo, arquivo_pdf, texto_extraido,
                negocio_plataforma, diretoria, area_atuacao,
                missao, desafios, responsabilidades,
                formacao, idiomas, experiencia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        fields = [
            'titulo_cargo', 'arquivo_pdf', 'texto_extraido',
            'negocio_plataforma', 'diretoria', 'area_atuacao',
            'missao', 'desafios', 'responsabilidades',
            'formacao', 'idiomas', 'experiencia',
        ]
        return self._execute(query, self._extract_params(dados, fields))

# ─────────────────────────────────────────────────────────────
# INSIGHTS IA REPOSITORY
# ─────────────────────────────────────────────────────────────

class InsightsRepository(BaseRepository):
    """Repository para tabela fato_insights."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove insights de um entrevistado."""
        return self._execute(
            "DELETE FROM fato_insights WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """
        Insere um insight.

        Nota: usa params explícitos em vez de _extract_params pois
        sistemas_envolvidos requer json.dumps() e confianca tem default 0.9.
        """
        query = """
            INSERT INTO fato_insights (
                id_entrevistado, id_bloco, id_etapa_cadeia, categoria, subcategoria,
                descricao, citacao_direta, severidade, linhagem_dados,
                risco_estimado, area_impactada, sistemas_envolvidos,
                confianca, modelo_ia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            dados.get('id_etapa_cadeia'),
            dados.get('categoria'),
            dados.get('subcategoria'),
            dados.get('descricao'),
            dados.get('citacao_direta'),
            dados.get('severidade'),
            dados.get('linhagem_dados'),
            dados.get('risco_estimado'),
            dados.get('area_impactada'),
            json.dumps(dados.get('sistemas_envolvidos', []), ensure_ascii=False),
            dados.get('confianca', 0.9),
            dados.get('modelo_ia')
        )
        return self._execute(query, params)

    def get_context_insights(self, limit: int = 20) -> List[Dict]:
        """Retorna insights de entrevistas JÁ PROCESSADAS."""
        query = """
            SELECT i.categoria, i.subcategoria, i.descricao, i.severidade,
                   e.nome, e.cargo, e.area, i.etapa_cadeia
            FROM fato_insights i
            JOIN stg_entrevistados e ON e.id = i.id_entrevistado
            WHERE e.status_revisao = ?
            ORDER BY
                CASE i.severidade
                    WHEN 'Alta' THEN 1
                    WHEN 'Media' THEN 2
                    WHEN 'Baixa' THEN 3
                END,
                i.dt_registro DESC
            LIMIT ?
        """
        rows = self._execute(query, (IntervieweeStatus.DONE, limit,), fetch=True)
        return [
            {
                "categoria": r[0], "subcategoria": r[1], "descricao": r[2],
                "severidade": r[3], "entrevistado": r[4], "cargo": r[5],
                "area": r[6], "etapa": r[7]
            }
            for r in rows
        ]

# ─────────────────────────────────────────────────────────────
# SISTEMAS USO REPOSITORY
# ─────────────────────────────────────────────────────────────

class SistemasUsoRepository(BaseRepository):
    """Repository para tabela fato_sistemas_uso."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove sistemas de um entrevistado."""
        return self._execute(
            "DELETE FROM fato_sistemas_uso WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """Insere registro de uso de sistema."""
        # Se veio "sistema" como string (nome), resolve para ID
        id_sistema = dados.get('id_sistema')
        if not id_sistema:
            dim_repo = DimSistemasRepository(self.db_path)
            id_sistema = dim_repo.get_or_create(dados.get('sistema'))
            
        query = """
            INSERT INTO fato_sistemas_uso (
                id_entrevistado, id_bloco, id_sistema, como_usa,
                satisfacao, workaround, entradas, saidas, is_excel_bridge
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            id_sistema,
            dados.get('como_usa'),
            dados.get('satisfacao'),
            dados.get('workaround'),
            dados.get('entradas'),
            dados.get('saidas'),
            dados.get('is_excel_bridge', 0)
        )
        return self._execute(query, params)

    def upsert(self, dados: Dict) -> int:
        """
        Insere ou atualiza sistema (consolida por entrevistado + sistema).

        Se já existe, adiciona o novo contexto ao existente.
        """
        sistema_nome = dados.get('sistema') # Nome vindo da IA
        entrevistado_id = dados.get('id_entrevistado')
        novo_contexto = dados.get('como_usa', '')

        # Resolve ID do sistema
        dim_repo = DimSistemasRepository(self.db_path)
        id_sistema = dim_repo.get_or_create(sistema_nome)

        # Verifica se já existe o uso deste sistema por este entrevistado
        check_query = """
            SELECT id, como_usa, workaround
            FROM fato_sistemas_uso
            WHERE id_entrevistado = ? AND id_sistema = ?
        """
        rows = self._execute(check_query, (entrevistado_id, id_sistema), fetch=True)

        if rows:
            # Já existe - atualiza consolidando informações
            existing_id, como_usa, workaround = rows[0]

            # Consolida workaround se não tiver
            workaround_consolidado = workaround or dados.get('workaround', '')

            # Consolida linhagem
            entradas_consolidado = dados.get('entradas', '')
            saidas_consolidado = dados.get('saidas', '')

            update_query = """
                UPDATE fato_sistemas_uso
                SET como_usa = ?,
                    workaround = ?,
                    entradas = ?,
                    saidas = ?,
                    is_excel_bridge = ?
                WHERE id = ?
            """
            self._execute(update_query, (
                novo_contexto, workaround_consolidado,
                entradas_consolidado, saidas_consolidado,
                dados.get('is_excel_bridge', 0),
                existing_id
            ))
            return existing_id
        else:
            # Não existe - insere novo (forçando ID resolvido)
            dados['id_sistema'] = id_sistema
            return self.insert(dados)

# ─────────────────────────────────────────────────────────────
# RELACOES REPOSITORY
# ─────────────────────────────────────────────────────────────

class RelacoesRepository(BaseRepository):
    """Repository para tabela fato_relacoes."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove relações de um entrevistado."""
        return self._execute(
            "DELETE FROM fato_relacoes WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """Insere uma relação."""
        query = """
            INSERT INTO fato_relacoes (
                id_entrevistado, id_bloco, tipo, pessoa_citada, area_citada, contexto
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        fields = ['id_entrevistado', 'id_bloco', 'tipo', 'pessoa_citada', 'area_citada', 'contexto']
        return self._execute(query, self._extract_params(dados, fields))

    def upsert(self, dados: Dict) -> int:
        """
        Insere ou atualiza relação (consolida por entrevistado + pessoa citada).
        """
        pessoa_citada = dados.get('pessoa_citada', '').strip()
        entrevistado_id = dados.get('id_entrevistado')

        novo_contexto = dados.get('contexto', '')
        area_citada = dados.get('area_citada', '')

        # Verifica se já existe (busca por nome aproximado)
        check_query = """
            SELECT id, contexto, area_citada
            FROM fato_relacoes
            WHERE id_entrevistado = ? AND LOWER(pessoa_citada) = LOWER(?)
        """
        rows = self._execute(check_query, (entrevistado_id, pessoa_citada), fetch=True)

        if rows:
            # Já existe - atualiza contexto
            existing_id, contexto, area = rows[0]

            # Consolida área se não tiver
            area_consolidada = area or area_citada

            # Adiciona novo contexto se for diferente
            contexto_consolidado = contexto
            if novo_contexto and novo_contexto not in (contexto or ''):
                contexto_consolidado = f"{contexto or ''} | {novo_contexto}"

            update_query = """
                UPDATE fato_relacoes
                SET area_citada = ?, contexto = ?
                WHERE id = ?
            """
            self._execute(update_query, (area_consolidada, contexto_consolidado, existing_id))
            return existing_id
        else:
            # Não existe - insere novo
            return self.insert(dados)

    def get_by_entrevistado(self, entrevistado_id: int) -> List[Dict]:
        """Retorna todas as relações de um entrevistado."""
        query = """
            SELECT tipo, pessoa_citada, area_citada, contexto
            FROM fato_relacoes
            WHERE id_entrevistado = ?
        """
        rows = self._execute(query, (entrevistado_id,), fetch=True)
        return [
            {
                'tipo': r[0], 'pessoa_citada': r[1], 'area_citada': r[2], 'contexto': r[3]
            }
            for r in rows
        ]


# ─────────────────────────────────────────────────────────────
# CHUNKS REPOSITORY
# ─────────────────────────────────────────────────────────────

class ChunksRepository(BaseRepository):
    """Repository para tabela stg_chunks."""

    def mark_done(self, chunk_id: int):
        """Marca um chunk como analisado/concluiío."""
        self._execute(
            "UPDATE stg_chunks SET status_analise = 'concluido' WHERE id = ?",
            (chunk_id,)
        )


# ─────────────────────────────────────────────────────────────
# ARQUIVOS REPOSITORY
# ─────────────────────────────────────────────────────────────

class ArquivosRepository(BaseRepository):
    """Repository para tabela stg_arquivos."""

    def insert(self, dados: Dict) -> int:
        """Insere um novo arquivo."""
        query = """
            INSERT INTO stg_arquivos (id_entrevistado, nome_arquivo, tipo_entrevista)
            VALUES (?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('nome_arquivo'),
            dados.get('tipo_entrevista')
        )
        return self._execute(query, params)

    def find_by_entrevistado_and_tipo(self, id_entrevistado: int, tipo: str) -> Optional[int]:
        """Busca arquivo por entrevistado e tipo. Retorna ID ou None."""
        query = """
            SELECT id FROM stg_arquivos
            WHERE id_entrevistado = ? AND tipo_entrevista = ?
        """
        rows = self._execute(query, (id_entrevistado, tipo), fetch=True)
        return rows[0][0] if rows else None

    def get_all_with_transcricao(self) -> List[Dict]:
        """Retorna todos os arquivos com suas transcrições."""
        query = """
            SELECT a.id, a.id_entrevistado, a.nome_arquivo, a.tipo_entrevista, t.texto_limpo
            FROM stg_arquivos a
            JOIN stg_transcricoes t ON a.id = t.id_arquivo
        """
        rows = self._execute(query, fetch=True)
        return [
            {
                'id': r[0], 'id_entrevistado': r[1], 'nome_arquivo': r[2],
                'tipo_entrevista': r[3], 'texto': r[4]
            }
            for r in rows
        ]

# ─────────────────────────────────────────────────────────────
# SISTEMAS REPOSITORY (Dimensões)
# ─────────────────────────────────────────────────────────────

class DimSistemasRepository(BaseRepository):
    """Repository para a tabela dim_sistemas."""

    def get_or_create(self, nome: str) -> int:
        """Busca ID do sistema pelo nome ou cria se não existir."""
        if not nome:
            return None
            
        nome = nome.strip()
        # Busca exata (case insensitive)
        row = self._execute("SELECT id FROM dim_sistemas WHERE LOWER(nome) = LOWER(?)", (nome,), fetch=True)
        if row:
            return row[0][0]
        
        # Cria novo se não existir — marcado como descoberto pela IA
        print(f"      [SISTEMAS] Novo sistema detectado pela IA: {nome}")
        return self._execute(
            "INSERT INTO dim_sistemas (nome, fonte) VALUES (?, 'ia_analise')",
            (nome,)
        )

    def get_by_entrevistado(self, entrevistado_id: int) -> List[Dict]:
        """Retorna lista de sistemas vinculados a um entrevistado com detalhes do catálogo."""
        query = """
            SELECT s.nome, su.como_usa, su.satisfacao, su.workaround, su.entradas, su.saidas, c.nome as etapa_cadeia
            FROM fato_sistemas_uso su
            JOIN dim_sistemas s ON su.id_sistema = s.id
            LEFT JOIN dim_cadeia_valor c ON s.id_etapa_cadeia = c.id
            WHERE su.id_entrevistado = ?
        """
        rows = self._execute(query, (entrevistado_id,), fetch=True)
        return [
            {
                'sistema': r[0], 'como_usa': r[1], 'satisfacao': r[2],
                'workaround': r[3], 'entradas': r[4], 'saidas': r[5],
                'etapa_cadeia': r[6]
            } for r in rows
        ]
