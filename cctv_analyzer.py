import os
import requests
from dotenv import load_dotenv

load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")

def analizar_archivo_logs(ruta_archivo):
    """
    Abre un archivo .txt con logs de un DVR, lee todo el contenido 
    y se lo manda a la IA para hacer un triaje diario.
    """
    # 1. Leer el archivo .txt
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido_logs = archivo.read()
    except FileNotFoundError:
        return f"Error: No se encontró el archivo '{ruta_archivo}'. Verifica que esté en la misma carpeta."

    # 2. Conectar a la API
    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    # 3. El Prompt Inteligente (La magia del negocio)
    prompt = f"""
    Eres el operador en jefe de un centro de monitoreo CCTV. 
    A continuación te paso el registro de eventos de un día completo. 
    Tu trabajo es:
    1. Ignorar los eventos de rutina (System Startup, Normal activity, etc).
    2. Identificar ÚNICAMENTE las amenazas reales (Riesgo Medio o Alto).
    3. Redactar un reporte ejecutivo directo y profesional para el dueño del negocio indicando qué pasó y a qué hora.
    
    Aquí están los logs del día:
    {contenido_logs}
    """
    
    payload = {
        "contents": [{"parts": [{"text": prompt}]}]
    }
    
    try:
        response = requests.post(url, headers=headers, json=payload)
        
        if response.status_code == 200:
            datos = response.json()
            return datos['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error HTTP {response.status_code}: {response.text}"
            
    except Exception as e:
        return f"Error ejecutando el script: {e}"

# --- PRUEBA DEL SCRIPT ---
if __name__ == "__main__":
    nombre_archivo = "logs_dahua.txt"
    
    print(f"Leyendo archivo '{nombre_archivo}' y generando reporte diario...\n")
    reporte_final = analizar_archivo_logs(nombre_archivo)
    
    print("=== REPORTE EJECUTIVO DIARIO ===")
    print(reporte_final)
