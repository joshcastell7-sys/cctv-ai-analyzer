import os
import requests
import smtplib
from email.message import EmailMessage
from dotenv import load_dotenv

# 1. Cargar Credenciales
load_dotenv()
api_key = os.getenv("GEMINI_API_KEY")
email_origen = os.getenv("EMAIL_USER")
email_password = os.getenv("EMAIL_PASS")

def analizar_archivo_logs(ruta_archivo):
    """Lee los logs del DVR y usa IA para generar el reporte."""
    try:
        with open(ruta_archivo, "r", encoding="utf-8") as archivo:
            contenido_logs = archivo.read()
    except FileNotFoundError:
        return "Error: No se encontró el archivo de logs."

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-flash-latest:generateContent?key={api_key}"
    headers = {'Content-Type': 'application/json'}
    
    prompt = f"""
    Eres el operador de un centro de monitoreo CCTV. 
    Ignora eventos de rutina. Identifica amenazas reales.
    Redacta un reporte ejecutivo indicando qué pasó y a qué hora.
    Logs del día:
    {contenido_logs}
    """
    
    payload = {"contents": [{"parts": [{"text": prompt}]}]}
    
    try:
        # Espera máximo 15 segundos
        response = requests.post(url, headers=headers, json=payload, timeout=15)
        if response.status_code == 200:
            return response.json()['candidates'][0]['content']['parts'][0]['text']
        else:
            return f"Error HTTP {response.status_code}: {response.text}"
    except Exception as e:
        return f"Error de conexión: {e}"

def enviar_correo_alerta(reporte_texto, email_cliente, archivo_clip):
    """Arma el correo electrónico con el reporte de la IA y adjunta el video."""
    msg = EmailMessage()
    msg['Subject'] = '🚨 ALERTA CCTV: Incidente de Seguridad Detectado'
    msg['From'] = email_origen
    msg['To'] = email_cliente
    
    # Cuerpo del correo
    cuerpo = f"{reporte_texto}\n\n---\n*Sistema Automatizado CASFER*\nSe adjunta el clip de video con la evidencia del incidente."
    msg.set_content(cuerpo)
    
    # Adjuntar la evidencia de video
    try:
        with open(archivo_clip, 'rb') as f:
            datos_video = f.read()
            msg.add_attachment(datos_video, maintype='video', subtype='mp4', filename=archivo_clip)
        print("✅ Evidencia de video adjuntada correctamente.")
    except FileNotFoundError:
        print(f"⚠️ Aviso: No se encontró el clip de evidencia '{archivo_clip}'.")

    # Enviar el correo
    try:
        print(f"Enviando correo a {email_cliente}...")
        with smtplib.SMTP_SSL('smtp.gmail.com', 465) as smtp:
            smtp.login(email_origen, email_password)
            smtp.send_message(msg)
        return "✅ ¡Correo enviado exitosamente al cliente con la evidencia!"
    except Exception as e:
        return f"❌ Error enviando correo: {e}"

# --- PRUEBA FINAL DEL SISTEMA ---
if __name__ == "__main__":
    archivo_logs = "logs_dahua.txt"
    clip_adjunto = "clip_evidencia.mp4"
    correo_del_cliente = "josreus11y@outlook.com"
    
    print("1. Analizando logs con Inteligencia Artificial...")
    reporte_ia = analizar_archivo_logs(archivo_logs)
    
    # FILTRO DE SEGURIDAD: Solo enviar si NO hay error
    if "Error HTTP" in reporte_ia or "Error de conexión" in reporte_ia:
        print(f"⚠️ La IA no está disponible en este momento. Se canceló el envío para no mandar errores al cliente.")
        print(f"Detalle: {reporte_ia}")
    else:
        print("Reporte generado.\n")
        print("2. Preparando envío de reporte y evidencia...")
        resultado_envio = enviar_correo_alerta(reporte_ia, correo_del_cliente, clip_adjunto)
        print(resultado_envio)
        