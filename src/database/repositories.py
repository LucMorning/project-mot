"""
Repository Pattern - Camada de abstração para acesso ao banco.

Aplica DRY: cada operação SQL aparece UMA vez só.
Separa lógica de negócio do acesso a dados.

Princípios:
- DRY: SQL não se repete
- SRP: Cada repository cuida de uma entidade
- OCP: Fácil adicionar novos métodos sem modificar existentes
"""
import sqlite3
import json
from typing import List, Dict, Optional, Any
from pathlib import Path


class BaseRepository:
    """Base class para todos os repositories."""

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def _execute(self, query: str, params: tuple = None, fetch: bool = False) -> Optional[Any]:
        """Executa query com tratamento de erro padrão."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)

            if fetch:
                result = cursor.fetchall()
                conn.close()
                return result

            conn.commit()
            return cursor.rowcount
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            if not fetch:
                conn.close()


# ─────────────────────────────────────────────────────────────
# ENTREVISTADOS REPOSITORY
# ─────────────────────────────────────────────────────────────

class EntrevistadosRepository(BaseRepository):
    """Repository para tabela entrevistados."""

    def delete_all(self) -> int:
        """Remove todos os entrevistados."""
        return self._execute("DELETE FROM entrevistados")

    def insert(self, dados: Dict) -> int:
        """
        Insere um entrevistado.

        Args:
            dados: Dict com campos (id, nome, cargo, area, nivel, etc)

        Returns:
            rowcount (deve ser 1)
        """
        query = """
            INSERT INTO entrevistados (
                id, nome, cargo, diretoria, plataforma, area, nivel,
                data_entrevista, tipo_entrevista, arquivo_transcricao,
                arquivo_cargo_pdf, status_revisao
            ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id'),
            dados.get('nome'),
            dados.get('cargo'),
            dados.get('diretoria'),
            dados.get('plataforma'),
            dados.get('area'),
            dados.get('nivel'),
            dados.get('data_entrevista'),
            dados.get('tipo_entrevista'),
            dados.get('arquivo_transcricao'),
            dados.get('arquivo_cargo_pdf'),
            dados.get('status_revisao', 'pendente')
        )
        return self._execute(query, params)

    def insert_batch(self, lista: List[Dict]) -> int:
        """Insere múltiplos entrevistados em batch."""
        count = 0
        for dados in lista:
            count += self.insert(dados)
        return count

    def get_pending(self, limit: int = 5) -> List[tuple]:
        """
        Busca entrevistados pendentes de processamento.

        Returns:
            Lista de tuples (id, texto_limpo, nome, cargo, area, nivel, diretoria,
                            responsabilidades, competencias, desafios)
        """
        query = """
            SELECT e.id, t.texto_limpo, e.nome, e.cargo, e.area, e.nivel, e.diretoria,
                   c.responsabilidades, c.competencias, c.desafios
            FROM entrevistados e
            JOIN transcricoes t ON t.id_entrevistado = e.id
            LEFT JOIN cargos c ON c.arquivo_pdf = e.arquivo_cargo_pdf
            WHERE e.status_revisao IN ('pendente', 'erro')
            ORDER BY e.id ASC
            LIMIT ?
        """
        return self._execute(query, (limit,), fetch=True)

    def get_by_id(self, entrevistado_id: int) -> Optional[Dict]:
        """Busca entrevistado por ID."""
        query = """
            SELECT e.id, e.nome, e.cargo, e.area, e.nivel, e.diretoria,
                   t.texto_limpo, c.responsabilidades, c.competencias, c.desafios
            FROM entrevistados e
            JOIN transcricoes t ON t.id_entrevistado = e.id
            LEFT JOIN cargos c ON c.arquivo_pdf = e.arquivo_cargo_pdf
            WHERE e.id = ?
        """
        rows = self._execute(query, (entrevistado_id,), fetch=True)
        if not rows:
            return None

        row = rows[0]
        resp, comp, desaf = row[7], row[8], row[9]

        # Monta texto do cargo limpo
        blocks = []
        if desaf: blocks.append(f"DESAFIOS:\n{desaf}")
        if resp: blocks.append(f"RESPONSABILIDADES:\n{resp}")
        if comp: blocks.append(f"COMPETENCIAS:\n{comp}")
        cargo_limpo = "\n\n".join(blocks) if blocks else None

        return {
            "id": row[0], "nome": row[1], "cargo": row[2], "area": row[3],
            "nivel": row[4], "diretoria": row[5], "texto_completo": row[6],
            "texto_cargo": cargo_limpo
        }

    def update_status(self, entrevistado_id: int, status: str, notas: str = None) -> int:
        """Atualiza status do processamento."""
        if notas:
            return self._execute(
                "UPDATE entrevistados SET status_revisao = ?, notas_revisor = ? WHERE id = ?",
                (status, notas, entrevistado_id)
            )
        return self._execute(
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

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove transcrição de um entrevistado."""
        return self._execute(
            "DELETE FROM transcricoes WHERE id_entrevistado = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """
        Insere uma transcrição.

        Args:
            dados: Dict com (id_entrevistado, texto_completo, texto_limpo,
                   data_gravacao, arquivo_fonte, num_paragrafos, num_caracteres)
        """
        query = """
            INSERT INTO transcricoes (
                id_entrevistado, texto_completo, texto_limpo,
                data_gravacao, arquivo_fonte, num_paragrafos, num_caracteres
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('texto_completo'),
            dados.get('texto_limpo'),
            dados.get('data_gravacao'),
            dados.get('arquivo_fonte'),
            dados.get('num_paragrafos', 0),
            dados.get('num_caracteres', 0)
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
        """
        Insere um cargo.

        Args:
            dados: Dict com (titulo_cargo, arquivo_pdf, texto_extraido,
                   responsabilidades, competencias, area_atuacao, desafios)
        """
        query = """
            INSERT INTO cargos (
                titulo_cargo, arquivo_pdf, texto_extraido,
                responsabilidades, competencias, area_atuacao, desafios
            ) VALUES (?, ?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('titulo_cargo'),
            dados.get('arquivo_pdf'),
            dados.get('texto_extraido'),
            dados.get('responsabilidades'),
            dados.get('competencias'),
            dados.get('area_atuacao'),
            dados.get('desafios')
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
        """
        Insere um insight (Dor, Processo, etc).

        Args:
            dados: Dict com todos os campos do insight
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
        """
        Retorna insights de entrevistas JÁ PROCESSADAS para contexto acumulado.

        Ordenado por severidade e data.
        """
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
                i.created_at DESC
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

    def get_summary(self) -> Dict[str, int]:
        """Retorna contagem de menções de sistemas."""
        query = """
            SELECT sistema, COUNT(*) as count
            FROM sistemas_uso
            GROUP BY sistema
            ORDER BY count DESC
        """
        rows = self._execute(query, fetch=True)
        return dict(rows)


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
                id_entrevistado, id_bloco, tipo, pessoa_ou_area, contexto
            ) VALUES (?, ?, ?, ?, ?)
        """
        params = (
            dados.get('id_entrevistado'),
            dados.get('id_bloco'),
            dados.get('tipo'),
            dados.get('pessoa_ou_area'),
            dados.get('contexto')
        )
        return self._execute(query, params)


# ─────────────────────────────────────────────────────────────
# CROSS VALIDATION REPOSITORY
# ─────────────────────────────────────────────────────────────

class CrossValidationRepository(BaseRepository):
    """Repository para tabela cross_validation."""

    def delete_by_entrevistado(self, entrevistado_id: int) -> int:
        """Remove validação cruzada de um entrevistado."""
        return self._execute(
            "DELETE FROM cross_validation WHERE entrevistado_id = ?",
            (entrevistado_id,)
        )

    def insert(self, dados: Dict) -> int:
        """
        Insere validação cruzada (Etapa 3).

        Args:
            dados: Dict com (entrevistado_id, padroes_confirmados, contradicoes,
                   novos_insights, severidade_ajustada, num_referencias)
        """
        query = """
            INSERT INTO cross_validation (
                entrevistado_id, padroes_confirmados, contradicoes,
                novos_insights, severidade_ajustada, num_referencias
            ) VALUES (?, ?, ?, ?, ?, ?)
        """
        params = (
            dados.get('entrevistado_id'),
            json.dumps(dados.get('padroes_confirmados', []), ensure_ascii=False),
            json.dumps(dados.get('contradicoes', []), ensure_ascii=False),
            json.dumps(dados.get('novos_insights', []), ensure_ascii=False),
            dados.get('severidade_ajustada', 'Media'),
            dados.get('num_referencias', 0)
        )
        return self._execute(query, params)


if __name__ == "__main__":
    from src.config import DB_PATH

    # Teste
    repo = EntrevistadosRepository(DB_PATH)
    pending = repo.get_pending(limit=3)
    print(f"Entrevistados pendentes: {len(pending)}")
