import cv2
import numpy as np
import pytesseract

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def analizar_imagen(imagen):
    try:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        texto = pytesseract.image_to_string(gris, lang='eng').strip()
        porcentaje_negro = np.sum(gris < 20) / gris.size

        if porcentaje_negro > 0.95:
            return (
                "Pantalla negra, no se encontró el error. Pase a la fase de preguntas.",
                "Pantalla negra|No se encontró el error. Pase a la fase de preguntas."
            )

        if not texto:
            return (
                "No se detectó texto en la imagen. Asegúrese de subir una imagen válida o pase a la fase de preguntas.",
                "Sin texto|No se detectó texto en la imagen."
            )

        texto = texto.upper()
        errores = {
            "INACCESSIBLE_BOOT_DEVICE": "Verifica la conexión del disco y drivers de almacenamiento.",
            "PAGE_FAULT_IN_NONPAGED_AREA": "Fallo de página en área no pagada. Posible RAM defectuosa o controlador dañado.",
            "IRQL_NOT_LESS_OR_EQUAL": "Conflicto de drivers. Prueba arrancar en modo seguro y reinstalar controladores.",
            "0X0000000A": "Incompatibilidad de controlador o hardware.",
            "0X0000003B": "Conflictos entre drivers o antivirus.",
            "0X0000001E": "Error grave del kernel; revisa hardware y drivers.",
            "0X000000EF": "Proceso esencial del sistema falló. Intenta reparar Windows.",
            "0X0000001A": "Posible daño en RAM o errores de disco.",
            "0X000000D1": "Controlador mal instalado o dañado.",
            "0X00000116": "Falla del driver de video. Actualiza tu tarjeta gráfica.",
            "0X0000007B": "Disco no detectado o sistema corrupto.",
            "0X00000019": "Error de gestión de memoria del sistema.",
            "0X0000007E": "Error de driver o hardware.",
            "0X00000074": "Archivos de configuración dañados.",
            "0X00000124": "Falla de hardware; revisa ventilación, CPU, RAM.",
            "0X000000ED": "Error de disco; intenta reparar con comandos CHKDSK.",
            "0X0000009C": "Fallo de hardware crítico; revisa fuentes y temperatura.",
            "0X00000133": "Problemas con drivers o SSD; actualiza el firmware."
        }

        for clave, solucion in errores.items():
            if clave in texto:
                return (
                    f"Error detectado: {clave}\nDiagnostico: {solucion}",
                    f"{clave}|{solucion}"
                )

        return (
            "Pantalla azul detectada, pero el error no fue reconocido. Revisa el texto manualmente.",
            "Pantalla azul|No se reconoció el error."
        )

    except Exception as e:
        return (
            f"Error al analizar la pantalla azul: {e}",
            f"Error|Error al analizar la pantalla azul: {e}"
        )
