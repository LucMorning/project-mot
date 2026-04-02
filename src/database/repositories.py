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
        params = (
            dados.get('nome'),
            dados.get('cargo'),
            dados.get('diretoria'),
            dados.get('plataforma'),
            dados.get('area'),
            dados.get('nivel'),
            dados.get('dt_entrevista'),
            dados.get('tipo_entrevista'),
            dados.get('arquivo_transcricao'),
            dados.get('arquivo_cargo_pdf'),
            dados.get('status_revisao', 'pendente')
        )
        return self._execute(query, params)

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

# ─────────────────────────────────────────────────────────────
# TRANSCRICOES REPOSITORY
# ─────────────────────────────────────────────────────────────

class TranscricoesRepository(BaseRepository):
    """Repository para tabela transcricoes."""

    def delete_all(self) -> int:
        """Remove todas as transcrições."""
        return self._execute("DELETE FROM transcricoes")

    def insert(self, dados: Dict) -> int:
        """
        Insere uma transcrição.
        """
        query = """
            INSERT INTO transcricoes (
                id_entrevistado, texto_completo, texto_limpo,
                dt_gravacao, arquivo_origem
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('texto_completo'),
            dados.get('texto_limpo'),
            dados.get('dt_gravacao'),
            dados.get('arquivo_origem')
        )
        return self._execute(query, params)

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
        params = (
            dados.get('titulo_cargo'),
            dados.get('arquivo_pdf'),
            dados.get('texto_extraido'),
            dados.get('negocio_plataforma'),
            dados.get('diretoria'),
            dados.get('area_atuacao'),
            dados.get('missao'),
            dados.get('desafios'),
            dados.get('responsabilidades'),
            dados.get('formacao'),
            dados.get('idiomas'),
            dados.get('experiencia')
        )
        return self._execute(query, params)

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
        """Insere um insight."""
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
        """Insiste registro de uso de sistema."""
        query = """
            INSERT INTO sistemas_uso (
                id_entrevistado, id_bloco, sistema, como_usa, etapa_cadeia,
                satisfacao, workaround
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            dados.get('sistema'),
            dados.get('como_usa'),
            dados.get('etapa_cadeia'),
            dados.get('satisfacao'),
            dados.get('workaround')
        )
        return self._execute(query, params)

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
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            dados.get('tipo'),
            dados.get('pessoa_citada'),
            dados.get('area_citada'),
            dados.get('contexto')
        )
        return self._execute(query, params)

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
