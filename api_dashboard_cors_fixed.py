# api_dashboard_cors_fixed.py
# API REST con CORS corregido para servir datos del análisis de sentimientos al dashboard

from fastapi import FastAPI, HTTPException, Body, Request
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, validator
from pyairtable import Api
from dotenv import load_dotenv
import os
from datetime import datetime
from typing import List, Dict, Any, Optional
import uvicorn

# ---- Utils propios ----
# Ajusta el import según tu estructura real
# (si el archivo está en el mismo directorio, funciona tal cual; si no, corrige la ruta)
from airtable_utils import create_or_update_report
from analyze_sentiment_airtable import analizar_conversaciones

# Cargar variables de entorno
load_dotenv()

app = FastAPI(title="Dashboard Bienestar API", version="1.0.0")

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # desarrollo
    allow_credentials=False,
    allow_methods=["GET", "POST", "PUT", "DELETE", "OPTIONS"],
    allow_headers=["*"],
)

# -----------------------------
# Configuración de Airtable
# -----------------------------
AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN") or os.getenv("AIRTABLE_API_KEY")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Conversaciones"  # Asegúrate que coincida EXACTAMENTE con tu tabla

if not AIRTABLE_TOKEN or not BASE_ID:
    raise RuntimeError("Faltan AIRTABLE_TOKEN/AIRTABLE_API_KEY o AIRTABLE_BASE_ID en el .env")

api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)


def normalize_date(date_str: str) -> str:
    """Recibe fechas '2025-07-18' o '18/07/2025' y devuelve 'YYYY-MM-DD' para Airtable."""
    if not date_str:
        return datetime.utcnow().strftime("%Y-%m-%d")
    try:
        # ISO
        return datetime.fromisoformat(date_str).strftime("%Y-%m-%d")
    except Exception:
        # intente formatos comunes
        for fmt in ("%d/%m/%Y", "%m/%d/%Y", "%d-%m-%Y", "%m-%d-%Y"):
            try:
                return datetime.strptime(date_str, fmt).strftime("%Y-%m-%d")
            except Exception:
                pass
    # si nada funciona, lo devolvemos tal cual
    return date_str


# -----------------------------
# MODELOS Pydantic
# -----------------------------
class ConversacionCreate(BaseModel):
    id_conversacion: str
    fecha: str
    texto: str
    minutos_conectado: int
    elder_id: Optional[str] = None

    @validator("minutos_conectado")
    def minutos_min(cls, v):
        return max(1, v)

    @validator("fecha")
    def fecha_norm(cls, v):
        return normalize_date(v)

    @validator("texto")
    def texto_non_empty(cls, v):
        return v if v and v.strip() else "(sin texto)"


# -----------------------------
# RUTAS
# -----------------------------
@app.post("/analizar_conversaciones")
async def analizar_conversaciones_endpoint():
    """
    Ejecuta el análisis de sentimientos sobre las conversaciones en Airtable y actualiza las columnas.
    """
    try:
        analizar_conversaciones()
        return {"success": True, "message": "Análisis completado y columnas actualizadas."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al analizar conversaciones: {str(e)}")
@app.get("/")
async def root():
    return {
        "message": "API Dashboard Bienestar - CORS CORREGIDO",
        "status": "active",
        "port": 8002,
    }


@app.get("/termometro")
async def get_termometro_felicidad():
    """Obtiene el nivel actual del termómetro de felicidad"""
    try:
        records = table.all(max_records=10, sort=["-fecha"])
        if not records:
            return {
                "termometro_emocional": 50,
                "emoji": "😐",
                "mensaje_bienestar": "No hay datos disponibles",
            }

        latest_record = next(
            (r for r in records if "termometro_felicidad" in r["fields"]), None
        )

        if not latest_record:
            return {
                "termometro_emocional": 50,
                "emoji": "😐",
                "mensaje_bienestar": "No hay análisis disponible",
            }

        termometro = latest_record["fields"].get("termometro_felicidad", 3)
        termometro_100 = int((termometro / 5) * 100)

        return {
            "termometro_emocional": termometro_100,
            "emoji": latest_record["fields"].get("estado_emotivo", "😐"),
            "mensaje_bienestar": latest_record["fields"].get("resumen_emocional", ""),
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener datos: {str(e)}")


@app.get("/resumen")
async def get_resumen_actividad():
    """Obtiene el resumen de actividad del último mes"""
    try:
        records = table.all()
        total_minutos = sum(
            record["fields"].get("minutos_conectado", 0) for record in records
        )

        estados_animo = []
        for record in records:
            if "termometro_felicidad" in record["fields"]:
                estados_animo.append(record["fields"]["termometro_felicidad"])

        if estados_animo:
            promedio = sum(estados_animo) / len(estados_animo)
            if promedio >= 4:
                estado_general = "Positivo"
            elif promedio >= 3:
                estado_general = "Neutral"
            else:
                estado_general = "Negativo"
        else:
            estado_general = "Sin datos"

        return {"minutos_conectado_total": total_minutos, "estado_general": estado_general}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener resumen: {str(e)}")


@app.get("/frase_destacada")
async def get_frase_destacada():
    """Obtiene la frase más positiva reciente"""
    try:
        records = table.all(sort=["-fecha"])

        frase_destacada = None
        max_score = 0

        for record in records:
            termometro = record["fields"].get("termometro_felicidad", 0)
            texto = record["fields"].get("texto", "")
            if termometro >= max_score and texto:
                max_score = termometro
                frase_destacada = {
                    "frase": texto,
                    "termometro": termometro,
                    "fecha": record["fields"].get("fecha", ""),
                    "emoji": record["fields"].get("estado_emotivo", "😊"),
                }

        if not frase_destacada:
            return {
                "frase": "¡Esperando momentos felices!",
                "fecha": "",
                "emoji": "😊",
            }

        return frase_destacada

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error al obtener frase: {str(e)}")


@app.get("/estadisticas_completas")
async def get_estadisticas_completas():
    """Obtiene todas las estadísticas para el dashboard"""
    try:
        records = table.all()
        conversaciones = []
        for record in records:
            f = record["fields"]
            conversaciones.append(
                {
                    "id_conversacion": f.get("id_conversacion", ""),
                    "fecha": f.get("fecha", ""),
                    "texto": f.get("texto", ""),
                    "minutos_conectado": f.get("minutos_conectado", 0),
                    "termometro_felicidad": f.get("termometro_felicidad", 3),
                    "resumen_emocional": f.get("resumen_emocional", ""),
                    "recomendacion": f.get("recomendacion", ""),
                    "estado_emotivo": f.get("estado_emotivo", "😐"),
                    "fecha_analisis": f.get("fecha_analisis", ""),
                    # compatibilidad dashboard
                    "sentimiento": f.get("resumen_emocional", "Neutral"),
                    "emoji": f.get("estado_emotivo", "😐"),
                    "termometro_emocional": f.get("termometro_felicidad", 3),
                    "mensaje_bienestar": f.get("resumen_emocional", ""),
                }
            )
        return {"conversaciones": conversaciones}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al obtener estadísticas: {str(e)}"
        )


@app.post("/conversaciones")
async def crear_conversacion(
    request: Request, payload: ConversacionCreate = Body(...)
):
    """
    Crea un nuevo registro en Airtable:
    - id_conversacion
    - fecha (string)
    - texto (transcripción)
    - minutos_conectado
    - elder_id (opcional)
    Además, actualiza/crea el reporte diario.
    """
    try:
        # Log debug: lo que realmente viene del cliente
        raw_body = await request.body()
        print("📥 RAW BODY:", raw_body.decode("utf-8", errors="ignore"))
        print("✅ Payload validado:", payload.dict())

        fields = {
            "id_conversacion": payload.id_conversacion,
            "fecha": payload.fecha,
            "texto": payload.texto,
            "minutos_conectado": payload.minutos_conectado,
        }
        if payload.elder_id:
            fields["elder_id"] = payload.elder_id

        record = table.create(fields)
        print("✔ Registro creado en Airtable:", record["id"])

        # Actualizar/crear reporte diario si tenemos elder_id
        if payload.elder_id:
            create_or_update_report(
                elder_id=payload.elder_id,
                date=payload.fecha,
                conversation_text=payload.texto,
                minutos_conectado=payload.minutos_conectado,
            )

        return {"success": True, "record": record}

    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error al crear conversación: {e}"
        )


if __name__ == "__main__":
    print("🚀 Iniciando API Dashboard Bienestar - CORS CORREGIDO...")
    print("📊 Dashboard disponible en: http://localhost:8002")
    print("📚 Documentación en: http://localhost:8002/docs")
    uvicorn.run(app, host="0.0.0.0", port=8002)
