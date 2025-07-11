from diagnostico_experto import DiagnosticoPC, Sintomas
from subir_imagen import subir_imagen
from analizar_imagen import analizar_imagen
from generar_reporte import generar_reporte
from registro_consulta import registro_consulta

def ejecutar_diagnostico():
    print("\n=== DiagnoPC: Sistema Experto de Fallas en Computadoras ===\n")

    usar_imagen = input("¿Deseas subir imagen del equipo para analizar la pantalla? (si/no): ").strip().lower()
    color_detectado = "desconocido"

    if usar_imagen == "si":
        ruta = subir_imagen()
        if ruta:
            import cv2
            imagen = cv2.imread(ruta)
            color_detectado = analizar_imagen(imagen)
            print(f"\nResultado del análisis de pantalla: {color_detectado}")
        else:
            print("No se seleccionó ninguna imagen.")

    print("\nResponde las siguientes preguntas con 'si' o 'no':")
    enciende = input("¿La computadora enciende? (si/no): ").strip().lower()
    emite_pitidos = input("¿Emite pitidos al arrancar? (si/no): ").strip().lower()
    pitido_tipo = ""
    if emite_pitidos == "si":
        pitido_tipo = input("¿Qué tipo de pitido se escucha (corto, largo, continuo)?: ").strip().lower()
    pantalla = input("¿La pantalla muestra algo? (si/no): ").strip().lower()
    se_apaga = input("¿La computadora se apaga sola después de encender? (si/no): ").strip().lower()

    sintomas = Sintomas(
        enciende=enciende,
        pitidos=emite_pitidos,
        tipo_pitido=pitido_tipo,
        pantalla=pantalla,
        se_apaga=se_apaga,
        color_pantalla=color_detectado if color_detectado in ["azul", "negra"] else "desconocido"
    )

    experto = DiagnosticoPC()
    experto.reset()
    experto.declare(sintomas)
    experto.run()

    diagnostico = experto.diagnostico_final or "No se pudo determinar el problema."
    print("\nDiagnóstico final:", diagnostico)

    registro_consulta(str(sintomas), diagnostico)
    generar_reporte(sintomas, diagnostico)

if __name__ == "__main__":
    ejecutar_diagnostico()
