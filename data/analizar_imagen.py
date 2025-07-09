import cv2
import pytesseract

def analizar_pantalla_azul(imagen):
    try:
        gris = cv2.cvtColor(imagen, cv2.COLOR_BGR2GRAY)
        texto = pytesseract.image_to_string(gris, lang='spa') 

        texto = texto.upper() 
        print("\nTexto detectado en pantalla azul:\n", texto)

        errores = {
            "INACCESSIBLE_BOOT_DEVICE": "Verifica la conexión del disco y drivers de almacenamiento.",
            "0X00000050": "FALLO DE PÁGINA EN ÁREA NO PAGADA. Posible RAM defectuosa o controlador dañado.",
            "IRQL_NOT_LESS_OR_EQUAL": "Conflicto de drivers. Prueba arrancar en modo seguro y reinstalar controladores.",
            "0X0000000A": "IRQL_NOT_LESS_OR_EQUAL. Incompatibilidad de controlador o hardware.",
            "0X0000003B": "EXCEPCIÓN DE SERVICIO DEL SISTEMA. Conflictos entre drivers o antivirus.",
            "0X0000001E": "KMODE_EXCEPTION_NOT_HANDLED. Error grave del kernel; revisa hardware y drivers.",
            "0X000000EF": "CRITICAL_PROCESS_DIED. Proceso esencial del sistema falló. Intenta reparar Windows.",
            "0X0000001A": "GESTIÓN DE MEMORIA. Posible daño en RAM o errores de disco.",
            "0X000000D1": "DRIVER_IRQL_NOT_LESS_OR_EQUAL. Controlador mal instalado o dañado.",
            "0X00000116": "VIDEO_TDR_FAILURE. Falla del driver de video. Actualiza tu tarjeta gráfica.",
            "0X0000007B": "DISPOSITIVO DE ARRANQUE INACCESIBLE. Disco no detectado o sistema corrupto.",
            "0X00000019": "BAD_POOL_HEADER. Error de gestión de memoria del sistema.",
            "0X0000007E": "EXCEPCIÓN DE SUBPROCESO DEL SISTEMA NO CONTROLADA. Error de driver o hardware.",
            "0X00000074": "BAD_SYSTEM_CONFIG_INFO. Archivos de configuración dañados.",
            "0X00000124": "WHEA_UNCORRECTABLE_ERROR. Falla de hardware; revisa ventilación, CPU, RAM.",
            "0X000000ED": "VOLUMEN DE ARRANQUE NO MONTABLE. Error de disco; intenta reparar con comandos CHKDSK.",
            "0X0000009C": "MACHINE_CHECK_EXCEPTION. Fallo de hardware crítico; revisa fuentes y temperatura.",
            "0X00000133": "DPC_WATCHDOG_VIOLATION. Problemas con drivers o SSD; actualiza el firmware."
        }

        
        for clave, solucion in errores.items():
            if clave in texto:
                return f"🧾 Error detectado: {clave}\n💡 Solución: {solucion}"

        return "Pantalla azul detectada, pero el error no fue reconocido. Revisa el texto manualmente."

    except Exception as e:
        return f"Error al analizar la pantalla azul: {e}"
