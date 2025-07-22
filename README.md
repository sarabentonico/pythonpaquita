# 🎯 Sistema de Análisis de Sentimientos - SIMPLIFICADO

## 📁 Archivos Esenciales

### ✅ **4 archivos principales:**

1. **`analyze_sentiment_airtable.py`** - Análisis de sentimientos con IA
2. **`api_dashboard_cors_fixed.py`** - API REST para el dashboard
3. **`dashboard-preview.html`** - Dashboard interactivo
4. **`generar_datos_prueba.py`** - Generador de datos de prueba
5. **`.env`** - Configuración (tokens y keys)

## 🚀 Uso Simple

### 1. Generar datos de prueba (si necesitas)

```bash
python generar_datos_prueba.py
```

### 2. Ejecutar análisis de sentimientos

```bash
python analyze_sentiment_airtable.py
```

### 3. Iniciar API para dashboard

```bash
python api_dashboard_cors_fixed.py
```

### 4. Abrir dashboard

- Doble clic en `dashboard-preview.html`
- O arrastra el archivo al navegador

## 📊 Flujo Completo

1. **Datos** → Airtable tiene las conversaciones
2. **Análisis** → `analyze_sentiment_airtable.py` procesa con IA
3. **API** → `api_dashboard_cors_fixed.py` sirve los datos
4. **Dashboard** → `dashboard-preview.html` muestra resultados

## 🔧 Configuración

Solo necesitas verificar que tu `.env` tenga:

```
AIRTABLE_TOKEN=tu_token
AIRTABLE_BASE_ID=tu_base_id
```

¡Eso es todo! Sistema completamente simplificado. 🎉
