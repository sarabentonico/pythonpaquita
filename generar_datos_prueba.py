# generar_datos_prueba.py
# Script para generar datos de prueba variados en Airtable

import os
from pyairtable import Api
from dotenv import load_dotenv
from datetime import datetime, timedelta
import random

# Cargar variables de entorno
load_dotenv()

AIRTABLE_TOKEN = os.getenv("AIRTABLE_TOKEN")
BASE_ID = os.getenv("AIRTABLE_BASE_ID")
TABLE_NAME = "Conversaciones"

# Inicializar API de Airtable
api = Api(AIRTABLE_TOKEN)
table = api.table(BASE_ID, TABLE_NAME)

# Datos de prueba variados para diferentes estados de ánimo
datos_conversaciones = [
    # Conversaciones POSITIVAS
    {
        "texto": "¡Qué día tan maravilloso! Hoy mi nieta me visitó y jugamos juntos en el jardín. Me siento lleno de alegría y energía.",
        "minutos_conectado": 45,
        "fecha": "2025-07-16",
        "id_conversacion": "CONV_001"
    },
    {
        "texto": "Esta mañana salí a caminar por el parque y me encontré con mi viejo amigo Carlos. Conversamos por horas recordando los buenos tiempos. Me siento muy acompañado.",
        "minutos_conectado": 60,
        "fecha": "2025-07-15",
        "id_conversacion": "CONV_002"
    },
    {
        "texto": "Hoy terminé de leer un libro muy inspirador. Me encanta aprender cosas nuevas y mantener mi mente activa. Me siento realizado y feliz.",
        "minutos_conectado": 30,
        "fecha": "2025-07-14",
        "id_conversacion": "CONV_003"
    },
    {
        "texto": "Mi familia me organizó una videollamada sorpresa para mi cumpleaños. Ver a todos juntos, aunque sea virtualmente, me llenó el corazón de felicidad.",
        "minutos_conectado": 90,
        "fecha": "2025-07-13",
        "id_conversacion": "CONV_004"
    },
    {
        "texto": "Hoy cociné mi receta favorita de galletas y las compartí con mis vecinos. Me encanta poder dar alegría a otros. Me siento útil y contento.",
        "minutos_conectado": 40,
        "fecha": "2025-07-12",
        "id_conversacion": "CONV_005"
    },
    
    # Conversaciones NEUTRAS
    {
        "texto": "Hoy fue un día tranquilo. Hice mis actividades habituales, vi un poco de televisión y descansé. Todo normal, sin novedades particulares.",
        "minutos_conectado": 25,
        "fecha": "2025-07-11",
        "id_conversacion": "CONV_006"
    },
    {
        "texto": "Fui al supermercado a hacer las compras de la semana. Todo estuvo bien, encontré lo que necesitaba. Una rutina más del día a día.",
        "minutos_conectado": 20,
        "fecha": "2025-07-10",
        "id_conversacion": "CONV_007"
    },
    {
        "texto": "Hoy me dediqué a organizar algunos papeles y documentos. No fue emocionante, pero es necesario mantener todo en orden.",
        "minutos_conectado": 35,
        "fecha": "2025-07-09",
        "id_conversacion": "CONV_008"
    },
    {
        "texto": "Tuve una conversación telefónica rutinaria con mi médico para revisar mis medicamentos. Todo está estable y bajo control.",
        "minutos_conectado": 15,
        "fecha": "2025-07-08",
        "id_conversacion": "CONV_009"
    },
    
    # Conversaciones NEGATIVAS
    {
        "texto": "Hoy me siento muy solo. Nadie me ha llamado en días y la casa se siente muy silenciosa. Echo de menos tener más compañía.",
        "minutos_conectado": 10,
        "fecha": "2025-07-07",
        "id_conversacion": "CONV_010"
    },
    {
        "texto": "Me desperté con dolores en las articulaciones y me costó mucho trabajo hacer mis actividades normales. Me siento frustrado y cansado.",
        "minutos_conectado": 12,
        "fecha": "2025-07-06",
        "id_conversacion": "CONV_011"
    },
    {
        "texto": "Hoy recibí noticias de que un viejo amigo falleció. Me tiene muy triste recordar que cada vez somos menos los de mi generación.",
        "minutos_conectado": 8,
        "fecha": "2025-07-05",
        "id_conversacion": "CONV_012"
    },
    {
        "texto": "Me siento preocupado por mi salud. Tengo que ir al médico la próxima semana y siempre me pone nervioso. No me gusta ir solo.",
        "minutos_conectado": 18,
        "fecha": "2025-07-04",
        "id_conversacion": "CONV_013"
    },
    {
        "texto": "Hoy intenté usar la nueva aplicación en mi teléfono pero no pude entenderla. Me siento desconectado de la tecnología y eso me frustra.",
        "minutos_conectado": 22,
        "fecha": "2025-07-03",
        "id_conversacion": "CONV_014"
    },
    
    # Conversaciones MIXTAS (cambios de estado)
    {
        "texto": "Empecé el día sintiéndome triste, pero luego mi hija me llamó y me contó buenas noticias sobre su trabajo. Me alegró mucho escucharla tan feliz.",
        "minutos_conectado": 38,
        "fecha": "2025-07-02",
        "id_conversacion": "CONV_015"
    },
    {
        "texto": "Aunque me costó trabajo levantarme esta mañana, decidí salir a tomar aire fresco y me encontré con un hermoso atardecer. La naturaleza siempre me da paz.",
        "minutos_conectado": 42,
        "fecha": "2025-07-01",
        "id_conversacion": "CONV_016"
    },
    {
        "texto": "Hoy me sentía un poco desanimado, pero recordé los consejos de mi terapeuta y decidí hacer algunas actividades que me gustan. Me ayudó a sentirme mejor.",
        "minutos_conectado": 50,
        "fecha": "2025-06-30",
        "id_conversacion": "CONV_017"
    },
    {
        "texto": "Tuve un momento difícil pensando en el pasado, pero luego me concentré en las cosas buenas del presente. Logré cambiar mi perspectiva.",
        "minutos_conectado": 33,
        "fecha": "2025-06-29",
        "id_conversacion": "CONV_018"
    },
    
    # Conversaciones de DIFERENTES USUARIOS (simulando múltiples personas)
    {
        "texto": "¡Hoy fue mi primer día usando esta herramienta! Me encanta poder expresar cómo me siento. Espero que me ayude a sentirme más conectada.",
        "minutos_conectado": 28,
        "fecha": "2025-06-28",
        "id_conversacion": "CONV_019"
    },
    {
        "texto": "Como usuario nuevo, estoy explorando todas las funciones. Me parece muy útil tener un espacio para reflexionar sobre mi día.",
        "minutos_conectado": 31,
        "fecha": "2025-06-27",
        "id_conversacion": "CONV_020"
    }
]

def insertar_datos_prueba():
    """Inserta los datos de prueba en Airtable"""
    print("🚀 Generando datos de prueba en Airtable...")
    print(f"📊 Se insertarán {len(datos_conversaciones)} conversaciones")
    print()
    
    registros_insertados = 0
    errores = 0
    
    for i, conversacion in enumerate(datos_conversaciones, 1):
        try:
            # Insertar el registro en Airtable
            record = table.create(conversacion)
            registros_insertados += 1
            
            # Mostrar progreso
            emoji = "✅" if i % 5 == 0 else "📝"
            print(f"{emoji} [{i:2d}/{len(datos_conversaciones)}] Insertado: {conversacion['id_conversacion']} - {conversacion['fecha']}")
            
        except Exception as e:
            errores += 1
            print(f"❌ Error insertando {conversacion['id_conversacion']}: {str(e)}")
    
    print()
    print("=" * 60)
    print("📊 RESUMEN DE INSERCIÓN:")
    print(f"✅ Registros insertados exitosamente: {registros_insertados}")
    print(f"❌ Errores: {errores}")
    print(f"📈 Total de registros: {registros_insertados + errores}")
    print()
    
    if registros_insertados > 0:
        print("🎯 PRÓXIMOS PASOS:")
        print("1. Ejecuta el análisis de sentimientos:")
        print("   python analyze_sentiment_airtable.py")
        print()
        print("2. Revisa tu dashboard para ver la variedad de datos:")
        print("   Abre dashboard-preview.html")
        print()
        print("3. Los nuevos datos incluyen:")
        print("   🟢 Conversaciones positivas (alegría, satisfacción)")
        print("   🟡 Conversaciones neutras (rutina, normalidad)")
        print("   🔴 Conversaciones negativas (tristeza, preocupación)")
        print("   🔄 Conversaciones mixtas (cambios de estado)")
        print()

def mostrar_estadisticas_datos():
    """Muestra estadísticas de los datos que se van a insertar"""
    positivas = sum(1 for conv in datos_conversaciones if any(palabra in conv['texto'].lower() 
                   for palabra in ['alegría', 'feliz', 'maravilloso', 'contento', 'encanta', 'realizado', 'inspirador']))
    
    negativas = sum(1 for conv in datos_conversaciones if any(palabra in conv['texto'].lower() 
                   for palabra in ['solo', 'triste', 'dolor', 'preocupado', 'frustrado', 'nervioso']))
    
    neutras = len(datos_conversaciones) - positivas - negativas
    
    minutos_total = sum(conv['minutos_conectado'] for conv in datos_conversaciones)
    minutos_promedio = minutos_total / len(datos_conversaciones)
    
    print("📊 ESTADÍSTICAS DE LOS DATOS DE PRUEBA:")
    print(f"📝 Total de conversaciones: {len(datos_conversaciones)}")
    print(f"🟢 Conversaciones positivas: {positivas}")
    print(f"🟡 Conversaciones neutras: {neutras}")
    print(f"🔴 Conversaciones negativas: {negativas}")
    print(f"⏱️  Minutos totales: {minutos_total}")
    print(f"📊 Promedio de minutos por sesión: {minutos_promedio:.1f}")
    print()

if __name__ == "__main__":
    print("🎭 GENERADOR DE DATOS DE PRUEBA PARA DASHBOARD DE BIENESTAR")
    print("=" * 60)
    print()
    
    # Mostrar estadísticas antes de insertar
    mostrar_estadisticas_datos()
    
    # Confirmar antes de proceder
    confirmacion = input("¿Deseas proceder con la inserción de datos? (s/n): ").lower().strip()
    
    if confirmacion in ['s', 'si', 'sí', 'y', 'yes']:
        print()
        insertar_datos_prueba()
    else:
        print("❌ Operación cancelada.")
        print("💡 Tip: Puedes ejecutar este script cuando quieras generar datos de prueba.")
