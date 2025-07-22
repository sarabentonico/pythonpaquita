import os
import requests
from datetime import datetime

AIRTABLE_API_KEY = os.getenv("AIRTABLE_API_KEY")
AIRTABLE_BASE_ID = os.getenv("AIRTABLE_BASE_ID")
CONVERSATIONS_TABLE = "conversations"
REPORTS_TABLE = "reports"

HEADERS = {
    "Authorization": f"Bearer {AIRTABLE_API_KEY}",
    "Content-Type": "application/json"
}

def save_conversation_to_airtable(conversation):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{CONVERSATIONS_TABLE}"
    data = {"fields": conversation}
    r = requests.post(url, headers=HEADERS, json=data)
    r.raise_for_status()
    return r.json()

def get_report_for_elder_and_date(elder_id, date):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{REPORTS_TABLE}"
    params = {
        "filterByFormula": f"AND(elder_id='{elder_id}', fecha='{date}')"
    }
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    records = r.json().get("records", [])
    return records[0] if records else None

def create_or_update_report(elder_id, date, conversation_text, minutos_conectado):
    report = get_report_for_elder_and_date(elder_id, date)
    if report:
        # Update existing report
        report_id = report["id"]
        fields = report["fields"]
        # Concatenate conversation text and sum minutes
        new_text = (fields.get("resumen_conversaciones", "") + "\n" + conversation_text).strip()
        new_minutes = fields.get("minutos_conectados", 0) + minutos_conectado
        data = {
            "fields": {
                "resumen_conversaciones": new_text,
                "minutos_conectados": new_minutes
            }
        }
        url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{REPORTS_TABLE}/{report_id}"
        r = requests.patch(url, headers=HEADERS, json=data)
        r.raise_for_status()
        return r.json()
    else:
        # Create new report
        data = {
            "fields": {
                "elder_id": elder_id,
                "fecha": date,
                "resumen_conversaciones": conversation_text,
                "minutos_conectados": minutos_conectado
            }
        }
        url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{REPORTS_TABLE}"
        r = requests.post(url, headers=HEADERS, json=data)
        r.raise_for_status()
        return r.json()

def get_reports_for_elder(elder_id):
    url = f"https://api.airtable.com/v0/{AIRTABLE_BASE_ID}/{REPORTS_TABLE}"
    params = {
        "filterByFormula": f"elder_id='{elder_id}'"
    }
    r = requests.get(url, headers=HEADERS, params=params)
    r.raise_for_status()
    return r.json().get("records", [])
