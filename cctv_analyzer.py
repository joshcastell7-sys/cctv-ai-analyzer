import os
import requests
from dotenv import load_dotenv

# 1. Cargar las llaves secretas de forma segura
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analizar_alerta_cctv(log_evento):
    """
    Toma un log técnico de una cámara de seguridad y usa la API REST 
    para generar un reporte inteligente.
    """
    # El Endpoint corregido con el modelo exacto (ahora sí)
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # El "Prompt" donde le damos instrucciones al cerebro de la IA
    prompt = f"Eres un analista de seguridad electrónica. Lee este log de un DVR, clasifica su nivel de riesgo (Bajo, Medio, Alto) y haz un resumen de 2 líneas: '{log_evento}'"
    
    # La estructura JSON que requiere la API
    payload = {
        "contents": [{
            "parts": [{"text": prompt}]
        }]
    }
    
    try:
        # Hacemos la petición POST al servidor
        response = requests.post(url, headers=headers, json=payload)
        
        # Validamos que el servidor nos haya respondido bien (Código 200)
        if response.status_code == 200:
            datos = response.json()
            # Navegamos el JSON para extraer solo el texto útil
            return datos['candidates'][0]['content']['parts'][0]['text']
        else:
            # IMPRIMIMOS EL ERROR DETALLADO DEL SERVIDOR
            return f"Error HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error ejecutando el script: {e}"

# --- PRUEBA DEL SCRIPT ---
if __name__ == "__main__":
    # Simulamos un log rústico que sacaría una cámara en campo
    log_prueba = "[SYS_ALARM] CH04_Perimetro_Norte | Motion_Detection | Line_Cross_Rule_01 | Obj: Unknown | Time: 03:15:22"
    
    print("Conectando con la API y analizando el log de seguridad...\n")
    reporte_final = analizar_alerta_cctv(log_prueba)
    
    print("=== REPORTE GENERADO POR IA ===")
    print(reporte_final)
    