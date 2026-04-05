import sqlite3
import json
from typing import List, Dict, Optional, Any
from pathlib import Path

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
    """Repository para tabela entrevistados (Atores)."""

    def insert(self, dados: Dict) -> int:
        """Insere um novo ator e retorna o ID."""
        query = """
            INSERT INTO entrevistados (
                nome, cargo, diretoria, plataforma, area, nivel,
                dt_entrevista, tipo_entrevista, arquivo_transcricao,
                arquivo_cargo_pdf, status_revisao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        fields = [
            'nome', 'cargo', 'diretoria', 'plataforma', 'area', 'nivel',
            'dt_entrevista', 'tipo_entrevista', 'arquivo_transcricao',
            'arquivo_cargo_pdf', 'status_revisao',
        ]
        return self._execute(query, self._extract_params(dados, fields, {'status_revisao': 'pendente'}))

    def get_pending(self, limit: int = 100) -> List[Dict]:
        """Retorna lista de entrevistados com análise pendente."""
        query = """
            SELECT e.id, e.nome, e.cargo, e.plataforma, e.dt_entrevista, t.texto_limpo, e.arquivo_cargo_pdf
            FROM entrevistados e
            JOIN transcricoes t ON e.id = t.id_entrevistado
            WHERE e.status_revisao = 'pendente'
            LIMIT ?
        """
        rows = self._execute(query, (limit,), fetch=True)
        return [
            {
                'id': r[0], 'nome': r[1], 'cargo': r[2], 
                'plataforma': r[3], 'dt_entrevista': r[4], 
                'texto': r[5], 'arquivo_cargo_pdf': r[6]
            } for r in rows
        ]

    def update_status(self, entrevistado_id: int, status: str):
        """Atualiza o status de análise de um entrevistado."""
        self._execute(
            "UPDATE entrevistados SET status_revisao = ? WHERE id = ?",
            (status, entrevistado_id)
        )

    def get_all_with_transcricao(self) -> list:
        """Retorna todos os entrevistados que possuem arquivo de transcrição vinculado."""
        rows = self._execute(
            "SELECT id, arquivo_transcricao FROM entrevistados WHERE arquivo_transcricao IS NOT NULL",
            fetch=True
        )
        return [{'id': r[0], 'arquivo_transcricao': r[1]} for r in rows]

# ─────────────────────────────────────────────────────────────
# TRANSCRICOES REPOSITORY
# ─────────────────────────────────────────────────────────────

class TranscricoesRepository(BaseRepository):
    """Repository para tabela transcricoes."""

    def delete_all(self) -> int:
        """Remove todas as transcrições (com CASCADE para chunks)."""
        # Primeiro deleta chunks (dependentes)
        self._execute("DELETE FROM transcricao_chunks")
        # Depois deleta transcrições
        return self._execute("DELETE FROM transcricoes")

    def insert(self, dados: Dict) -> int:
        """Insere uma transcrição."""
        query = """
            INSERT INTO transcricoes (
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
    """Repository para tabela cargos."""

    def delete_all(self) -> int:
        """Remove todos os cargos."""
        return self._execute("DELETE FROM cargos")

    def insert(self, dados: Dict) -> int:
        """Insere um cargo."""
        query = """
            INSERT INTO cargos (
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
    """Repository para tabela insights_ia."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove insights de um entrevistado."""
        return self._execute(
            "DELETE FROM insights_ia WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """
        Insere um insight.

        Nota: usa params explícitos em vez de _extract_params pois
        sistemas_envolvidos requer json.dumps() e confianca tem default 0.9.
        """
        query = """
            INSERT INTO insights_ia (
                id_entrevistado, id_bloco, etapa_cadeia, categoria, subcategoria,
                descricao, citacao_direta, sistemas_envolvidos, severidade,
                confianca, modelo_ia
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            dados.get('etapa_cadeia'),
            dados.get('categoria'),
            dados.get('subcategoria'),
            dados.get('descricao'),
            dados.get('citacao_direta'),
            json.dumps(dados.get('sistemas_envolvidos', []), ensure_ascii=False),
            dados.get('severidade'),
            dados.get('confianca', 0.9),
            dados.get('modelo_ia')
        )
        return self._execute(query, params)

    def get_context_insights(self, limit: int = 20) -> List[Dict]:
        """Retorna insights de entrevistas JÁ PROCESSADAS."""
        query = """
            SELECT i.categoria, i.subcategoria, i.descricao, i.severidade,
                   e.nome, e.cargo, e.area, i.etapa_cadeia
            FROM insights_ia i
            JOIN entrevistados e ON e.id = i.id_entrevistado
            WHERE e.status_revisao = 'concluida'
            ORDER BY
                CASE i.severidade
                    WHEN 'Alta' THEN 1
                    WHEN 'Media' THEN 2
                    WHEN 'Baixa' THEN 3
                END,
                i.dt_registro DESC
            LIMIT ?
        """
        rows = self._execute(query, (limit,), fetch=True)
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
    """Repository para tabela sistemas_uso."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove sistemas de um entrevistado."""
        return self._execute(
            "DELETE FROM sistemas_uso WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """Insere registro de uso de sistema."""
        query = """
            INSERT INTO sistemas_uso (
                id_entrevistado, id_bloco, sistema, como_usa, etapa_cadeia,
                satisfacao, workaround
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        fields = ['id_entrevistado', 'id_bloco', 'sistema', 'como_usa', 'etapa_cadeia', 'satisfacao', 'workaround']
        return self._execute(query, self._extract_params(dados, fields))

    def upsert(self, dados: Dict) -> int:
        """
        Insere ou atualiza sistema (consolida por entrevistado + sistema).

        Se já existe, adiciona o novo contexto ao existente.
        """
        sistema = dados.get('sistema')
        entrevistado_id = dados.get('id_entrevistado')
        novo_contexto = dados.get('como_usa', '')
        nova_etapa = dados.get('etapa_cadeia', '')

        # Verifica se já existe
        check_query = """
            SELECT id, como_usa, etapa_cadeia, workaround
            FROM sistemas_uso
            WHERE id_entrevistado = ? AND LOWER(sistema) = LOWER(?)
        """
        rows = self._execute(check_query, (entrevistado_id, sistema), fetch=True)

        if rows:
            # Já existe - atualiza consolidando informações
            existing_id, como_usa, etapa_cadeia, workaround = rows[0]

            # Consolida etapas (sem duplicar)
            etapas = set(etapa_cadeia.split(', ')) if etapa_cadeia else set()
            etapas.update(nova_etapa.split(', ')) if nova_etapa else None
            etapas.discard('')
            etapa_consolidada = ', '.join(sorted(etapas))

            # Consolida workaround se não tiver
            workaround_consolidado = workaround or dados.get('workaround', '')

            update_query = """
                UPDATE sistemas_uso
                SET como_usa = ?,
                    etapa_cadeia = ?,
                    workaround = ?
                WHERE id = ?
            """
            self._execute(update_query, (novo_contexto, etapa_consolidada, workaround_consolidado, existing_id))
            return existing_id
        else:
            # Não existe - insere novo
            return self.insert(dados)

# ─────────────────────────────────────────────────────────────
# RELACOES REPOSITORY
# ─────────────────────────────────────────────────────────────

class RelacoesRepository(BaseRepository):
    """Repository para tabela relacoes."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove relações de um entrevistado."""
        return self._execute(
            "DELETE FROM relacoes WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """Insere uma relação."""
        query = """
            INSERT INTO relacoes (
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
            FROM relacoes
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
                UPDATE relacoes
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
            FROM relacoes
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
    """Repository para tabela transcricao_chunks."""

    def mark_done(self, chunk_id: int):
        """Marca um chunk como analisado/concluiío."""
        self._execute(
            "UPDATE transcricao_chunks SET status_analise = 'concluido' WHERE id = ?",
            (chunk_id,)
        )
