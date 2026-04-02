import os
import sqlite3
import json
import time
from abc import ABC, abstractmethod
from typing import Dict, Any, Type, List
from pydantic import BaseModel, Field
import google.generativeai as genai

from src.config import DB_PATH
import dotenv

# =====================================================================
# MODELOS DE DADOS (Pydantic / Structured Outputs)
# =====================================================================

class SystemUsage(BaseModel):
    sistema: str = Field(description="Nome do sistema / ferramenta")
    como_usa: str = Field(description="Como a pessoa utiliza na rotina")
    etapa_cadeia: str = Field(description="Etapa dentre as 7 da cadeia de valor (ex: '4. Contratação & Execução')")
    satisfacao: str = Field(description="Positivo, Neutro ou Negativo")
    workaround: str = Field(description="Descreva algum 'ETL Humano' ou processo manual associado")

class InsightIA(BaseModel):
    etapa_cadeia_valor: str = Field(description="Qual das 7 etapas está impactada")
    categoria: str = Field(description="'Dor', 'Processo', 'ETL Humano', 'Ferramenta' ou 'Insight Entrelinhas'")
    subcategoria: str = Field(description="Detalhe da categoria")
    descricao: str = Field(description="Descrição detalhada do problema/ponto")
    citacao_direta: str = Field(description="Um trecho exato e aspas confirmando o problema")
    sistemas_envolvidos: list[str] = Field(description="Sistemas impactados/citados")
    severidade: str = Field(description="'Alta', 'Media', 'Baixa'")

class Relation(BaseModel):
    tipo: str = Field(description="'responde_a', 'se_relaciona_com' ou 'depende_de'")
    pessoa_ou_area: str = Field(description="Nome do stakeholder ou área")
    contexto: str = Field(description="Por que se comunicam?")

class AnalysisSchema(BaseModel):
    resumo_executivo: str = Field(description="Resumo de 3 a 5 frases identificando gargalos e macro-visão do entrevistado.")
    sistemas_uso: list[SystemUsage]
    insights_ia: list[InsightIA]
    relacoes: list[Relation]

# =====================================================================
# INTERFACES E PROVIDERS (SOLID)
# =====================================================================

class IAIProvider(ABC):
    @abstractmethod
    def analyze(self, system_prompt: str, user_content: str, schema: Type[BaseModel]) -> Dict[str, Any]:
        pass

class GeminiProvider(IAIProvider):
    def __init__(self, api_key: str, model_name: str = "gemini-2.5-flash"):
        genai.configure(api_key=api_key)
        self.model = genai.GenerativeModel(model_name)

    def analyze(self, system_prompt: str, user_content: str, schema: Type[BaseModel]) -> Dict[str, Any]:
        # Para Gemini com SDK usando Structured Outputs (response_schema)
        prompt = f"{system_prompt}\n\nCONTEXTO DO USUÁRIO:\n{user_content}"
        
        try:
            response = self.model.generate_content(
                prompt,
                generation_config=genai.GenerationConfig(
                    response_mime_type="application/json",
                    response_schema=schema,
                    temperature=0.2
                )
            )
            return json.loads(response.text)
        except Exception as e:
            print(f"[ERRO] Falha ao processar com Gemini SDK: {e}")
            raise e

# =====================================================================
# SERVIÇOS DE BD E PIPELINE
# =====================================================================

class DatabaseService:
    def __init__(self, db_path: str):
        self.db_path = db_path

    def _get_conn(self):
        return sqlite3.connect(self.db_path)

    def get_pending_transcripts(self) -> List[tuple]:
        """Traz todos os (id, texto, nome, cargo, arquivo_cargo_pdf) pendentes."""
        conn = self._get_conn()
        cursor = conn.cursor()
        query = """
            SELECT e.id, t.texto_completo, e.nome, e.cargo, c.texto_extraido 
            FROM entrevistados e
            JOIN transcricoes t ON t.entrevistado_id = e.id
            LEFT JOIN cargos c ON c.arquivo_pdf = e.arquivo_cargo_pdf
            WHERE e.status_revisao = 'em_progresso' OR e.status_revisao = 'pendente'
            LIMIT 5 -- Lote parametrizado para nao travar tudo
        """
        cursor.execute(query)
        data = cursor.fetchall()
        conn.close()
        return data

    def save_analysis(self, entrevistado_id: int, data: Dict[str, Any], model_name: str):
        conn = self._get_conn()
        cursor = conn.cursor()
        try:
            # Insights
            for i in data.get("insights_ia", []):
                cursor.execute("""
                    INSERT INTO insights_ia (entrevistado_id, etapa_cadeia_valor, categoria, subcategoria, 
                    descricao, citacao_direta, sistemas_envolvidos, severidade, confianca, modelo_ia)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                """, (entrevistado_id, i.get("etapa_cadeia_valor"), i.get("categoria"), i.get("subcategoria"),
                      i.get("descricao"), i.get("citacao_direta"), json.dumps(i.get("sistemas_envolvidos", [])),
                      i.get("severidade"), 1.0, model_name))

            # Sistemas
            for s in data.get("sistemas_uso", []):
                cursor.execute("""
                    INSERT INTO sistemas_uso (entrevistado_id, sistema, como_usa, etapa_cadeia, satisfacao, workaround)
                    VALUES (?, ?, ?, ?, ?, ?)
                """, (entrevistado_id, s.get("sistema"), s.get("como_usa"), s.get("etapa_cadeia"), 
                      s.get("satisfacao"), s.get("workaround")))

            # Relações
            for r in data.get("relacoes", []):
                cursor.execute("""
                    INSERT INTO relacoes (entrevistado_id, tipo, pessoa_ou_area, contexto)
                    VALUES (?, ?, ?, ?)
                """, (entrevistado_id, r.get("tipo"), r.get("pessoa_ou_area"), r.get("contexto")))
                
            # Update Status
            cursor.execute("UPDATE entrevistados SET status_revisao = 'concluida', data_revisao = CURRENT_TIMESTAMP WHERE id = ?", (entrevistado_id,))
            
            conn.commit()
        except Exception as e:
            conn.rollback()
            cursor.execute("UPDATE entrevistados SET status_revisao = 'erro', notas_revisor = ? WHERE id = ?", (str(e), entrevistado_id))
            conn.commit()
            print(f"[BD ERRO] ID {entrevistado_id}: {e}")
        finally:
            conn.close()

class AIAnalysisPipeline:
    def __init__(self, ai_provider: IAIProvider, db_service: DatabaseService, model_name: str):
        self.ai = ai_provider
        self.db = db_service
        self.model_name = model_name

    def build_system_prompt(self) -> str:
        return (
            "Você é um Data Engineer Sênior focado em governança e CAPEX corporativo.\n"
            "Mapeie EXATAMENTE a transcrição para a Cadeia de Valor de TI (7 etapas). Foco em 'ETLs Humanos' e planilhas sombra.\n"
            "Preencha o JSON estritamente de acordo com o Schema."
        )

    def run(self):
        print(f"[PIPELINE] Iniciando processamento com modelo: {self.model_name}")
        pendings = self.db.get_pending_transcripts()
        
        if not pendings:
            print("[PIPELINE] Nenhuma transcrição pendente.")
            return

        for row in pendings:
            e_id, texto_t, nome, cargo, texto_cargo = row
            print(f"> Processando Entrevistado ID {e_id}: {nome}...")
            
            contexto = f"NOME: {nome}\nCARGO OFICIAL DESCRIÇÃO (PDF): {texto_cargo}\n---\nTRANSCRIÇÃO:\n{texto_t}"
            
            try:
                result_json = self.ai.analyze(
                    system_prompt=self.build_system_prompt(),
                    user_content=contexto,
                    schema=AnalysisSchema
                )
                self.db.save_analysis(e_id, result_json, self.model_name)
                print(f"✅ Sucesso ID {e_id}")
            except Exception as e:
                print(f"❌ Erro na IA para ID {e_id}: {e}")
            
            # Rate limit básico
            time.sleep(2)

if __name__ == "__main__":
    dotenv.load_dotenv()
    # Usando API KEY configurada globalmente nas variáveis de ambiente (.env)
    API_KEY = os.getenv("GEMINI_API_KEY") 
    
    if not API_KEY:
        print("[AVISO] Configure GEMINI_API_KEY no .env para iniciar o Pipeline de IA.")
    else:
        provider = GeminiProvider(api_key=API_KEY)
        db = DatabaseService(DB_PATH)
        
        pipeline = AIAnalysisPipeline(ai_provider=provider, db_service=db, model_name="gemini-2.5-flash")
        pipeline.run()
