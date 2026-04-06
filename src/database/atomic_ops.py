"""
Atomic Operations - Orquestrador de atomicidade para o banco.

Garante write_truncate para tabelas geradas por IA e evita duplicações.
Segue SOLID principles:
- Single Responsibility: Cada método faz uma coisa só
- Open/Closed: Aberto para extensão, fechado para modificação
"""
import sqlite3
import hashlib
from pathlib import Path
from typing import Optional

from src.config import IntervieweeStatus


class AtomicWriter:
    """
    Gerencia operações atômicas no banco.

    Responsabilidade: Garantir que reprocessamentos não criem dados duplicados.
    """

    def __init__(self, db_path: str | Path):
        self.db_path = str(db_path)

    def _get_conn(self):
        """Retorna nova conexão."""
        return sqlite3.connect(self.db_path)

    # ─────────────────────────────────────────────────────────────
    # LIMPEZA POR ENTREVISTADO_ID (Write Truncate)
    # ─────────────────────────────────────────────────────────────

    def clean_entrevistado_ai_data(self, entrevistado_id: int) -> int:
        """
        Remove TODOS os dados gerados por IA para um entrevistado.

        Ordem reversa das FKs para evitar errors.
        Usado antes de reprocessar para evitar duplicações.

        Args:
            entrevistado_id: ID do entrevistado

        Returns:
            Número de linhas afetadas
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            affected = 0

            # 1. Validação cruzada (Etapa 3)
            cursor.execute("DELETE FROM cross_validation WHERE entrevistado_id = ?", (entrevistado_id,))
            affected += cursor.rowcount

            # 2. Relações
            cursor.execute("DELETE FROM relacoes WHERE entrevistado_id = ?", (entrevistado_id,))
            affected += cursor.rowcount

            # 3. Sistemas uso
            cursor.execute("DELETE FROM fato_sistemas_uso WHERE entrevistado_id = ?", (entrevistado_id,))
            affected += cursor.rowcount

            # 4. Insights IA (inclui Dores e Processos)
            cursor.execute("DELETE FROM insights_ia WHERE entrevistado_id = ?", (entrevistado_id,))
            affected += cursor.rowcount

            # 5. Reseta status
            cursor.execute(
                f"UPDATE stg_entrevistados SET status_revisao = '{IntervieweeStatus.PENDING}', data_revisao = NULL, notas_revisor = NULL WHERE id = ?",
                (entrevistado_id,)
            )
            affected += cursor.rowcount

            conn.commit()
            return affected
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def clean_transcricao(self, entrevistado_id: int) -> int:
        """Remove transcrição de um entrevistado."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("DELETE FROM stg_transcricoes WHERE entrevistado_id = ?", (entrevistado_id,))
            affected = cursor.rowcount
            conn.commit()
            return affected
        finally:
            conn.close()

    # ─────────────────────────────────────────────────────────────
    # LIMPEZA GLOBAL (Truncate Tables)
    # ─────────────────────────────────────────────────────────────

    def truncate_all_ai_data(self) -> dict:
        """
        Remove TODOS os dados gerados por IA do banco.

        Returns:
            Dict com contagem de linhas removidas por tabela
        """
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            counts = {}

            tables = ["cross_validation", "relacoes", "fato_sistemas_uso", "insights_ia"]

            for table in tables:
                cursor.execute(f"SELECT COUNT(*) FROM {table}")
                before = cursor.fetchone()[0]
                cursor.execute(f"DELETE FROM {table}")
                counts[table] = before

            # Reseta status de todos
            cursor.execute(
                f"UPDATE stg_entrevistados SET status_revisao = '{IntervieweeStatus.PENDING}', data_revisao = NULL, notas_revisor = NULL"
            )

            conn.commit()
            return counts
        except Exception as e:
            conn.rollback()
            raise e
        finally:
            conn.close()

    def truncate_stg_transcricoes(self) -> int:
        """Remove todas as transcrições."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM stg_transcricoes")
            before = cursor.fetchone()[0]
            cursor.execute("DELETE FROM stg_transcricoes")
            conn.commit()
            return before
        finally:
            conn.close()

    def truncate_cargos(self) -> int:
        """Remove todos os cargos."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM cargos")
            before = cursor.fetchone()[0]
            cursor.execute("DELETE FROM cargos")
            conn.commit()
            return before
        finally:
            conn.close()

    def truncate_entrevistados(self) -> int:
        """Remove todos os entrevistados (CUIDADO: FK cascade)."""
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            cursor.execute("SELECT COUNT(*) FROM stg_entrevistados")
            before = cursor.fetchone()[0]
            cursor.execute("DELETE FROM stg_entrevistados")
            conn.commit()
            return before
        finally:
            conn.close()

    # ─────────────────────────────────────────────────────────────
    # CHECKSUM (otimização para evitar re-extração)
    # ─────────────────────────────────────────────────────────────

    def file_checksum(self, file_path: str) -> str:
        """Calcula MD5 de um arquivo."""
        try:
            with open(file_path, 'rb') as f:
                return hashlib.md5(f.read()).hexdigest()
        except Exception:
            return ""


# ─────────────────────────────────────────────────────────────
# FUNÇÕES CONVENIÊNCIA
# ─────────────────────────────────────────────────────────────

def clean_before_reprocess(entrevistado_id: int, db_path: str | Path) -> int:
    """
    Limpa dados de IA antes de reprocessar um entrevistado.

    Args:
        entrevistado_id: ID do entrevistado
        db_path: Caminho do banco

    Returns:
        Número de linhas afetadas
    """
    writer = AtomicWriter(db_path)
    return writer.clean_entrevistado_ai_data(entrevistado_id)


if __name__ == "__main__":
    from src.config import DB_PATH

    writer = AtomicWriter(DB_PATH)
    print("=== Atomic Operations Test ===")
    print(f"clean_entrevistado_ai_data(999): {writer.clean_entrevistado_ai_data(999)} linhas")
