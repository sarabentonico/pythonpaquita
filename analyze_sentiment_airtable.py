
# analyze_sentiment_airtable.py

import os
from pyairtable import Api
from transformers import pipeline
from datetime import datetime
from dotenv import load_dotenv

# Cargar variables de entorno
load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")

# BASE_ID debe tener el formato correcto de Airtable (empieza con "app")
# Reemplaza con tu BASE_ID real de Airtable
BASE_ID = os.getenv("AIRTABLE_BASE_ID", "appXXXXXXXXXXXXXX")  # Formato: appXXXXXXXXXXXXXX
TABLE_NAME = "Conversaciones"

# Inicializar API y tabla usando el nuevo método
api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)


# Inicializar modelo de Hugging Face
classifier = pipeline("sentiment-analysis", model="finiteautomata/beto-sentiment-analysis")

def convertir_a_termometro(label):
    if label == "NEG":
        return 1
    elif label == "NEU":
        return 3
    elif label == "POS":
        return 5

def generar_mensaje(label):
    if label == "POS":
        return ("Muy positivo, con buena disposición y contenido alegre.",
                "La herramienta fue de gran ayuda para estimular una conversación fluida y emotiva. ¡Excelente!")
    elif label == "NEU":
        return ("Tono neutro, conversación estable sin grandes altibajos.",
                "Podría beneficiarse de más interacción emocional o contenido personal.")
    elif label == "NEG":
        return ("Tono negativo o apagado, poca emoción positiva detectada.",
                "Sería útil acompañar con más estímulos positivos o preguntas abiertas.")

def analizar_conversaciones():
    records = table.all()
    for record in records:
        fields = record["fields"]
        if "termometro_felicidad" in fields:
            continue  # Ya procesado

        texto = fields.get("texto", "")
        minutos = fields.get("minutos_conectado", None)
        if not texto or not minutos:
            continue

        resultado = classifier(texto[:512])[0]  # Analiza solo primeros 512 tokens
        label = resultado["label"]
        termometro = convertir_a_termometro(label)
        resumen, recomendacion = generar_mensaje(label)

        table.update(record["id"], {
            "termometro_felicidad": termometro,
            "resumen_emocional": resumen,
            "recomendacion": recomendacion,
            "estado_emotivo": "😊" if label == "POS" else ("😐" if label == "NEU" else "😔"),
            "fecha_analisis": datetime.now().strftime("%Y-%m-%d")
        })

if __name__ == "__main__":
    analizar_conversaciones()
