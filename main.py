from diagnostico_experto import DiagnosticoPC, Sintomas
from subir_imagen import subir_imagen
from analizar_imagen import analizar_imagen
from generar_reporte import generar_reporte

import io
import sys

import subir_imagen

def ejecutar_diagnostico():
    print("\n=== DiagnoPC: Sistema Experto de Fallas en Computadoras ===\n")

    usar_imagen = input("¿Deseas subir imagen del equipo para analizar la pantalla? (si/no): ").strip().lower()
    color_detectado = "desconocido"

    if usar_imagen == "si":
        ruta = subir_imagen()
        if ruta:
            color_detectado = analizar_imagen(ruta)
            print(f"\n  Color de pantalla detectado: {color_detectado}")
        else:
            print("No se seleccionó ninguna imagen.")

    print("\nResponde las siguientes preguntas con 'si' o 'no':")
    enciende = input("¿La computadora enciende? (si/no): ").strip().lower()
    emite_pitidos = input("¿Emite pitidos al arrancar? : ").strip().lower()

    pitido_tipo = "ninguno"
    if emite_pitidos == "si":
        print("\nEjemplos válidos: '1 corto', '3 cortos', '1 largo y 2 cortos'")
        pitido_tipo = input("Describe el tipo de pitido: ").strip().lower()
    pantalla = input("¿Muestra algo en la pantalla? (si/no): ").strip().lower()
    se_apaga = input("¿Se apaga sola después de un rato? (si/no): ").strip().lower()

    engine = DiagnosticoPC()
    engine.reset()
    engine.declare(Sintomas(
        enciende=enciende,
        pitidos=pitido_tipo,
        pantalla=pantalla,
        se_apaga=se_apaga,
        color_pantalla=color_detectado
    ))

    buffer = io.StringIO()
    sys.stdout = buffer
    engine.run()
    sys.stdout = sys.__stdout__
    diagnosticos = buffer.getvalue().strip().split("\n\n")

    respuestas = {
        "enciende": enciende,
        "pitidos": pitido_tipo,
        "pantalla": pantalla,
        "se_apaga": se_apaga,
        "color_pantalla": color_detectado
    }

    print("\n Diagnóstico generado por el sistema experto:")
    for diag in diagnosticos:
        print(f"→ {diag}")
        
    generar_reporte(respuestas, diagnosticos)

if __name__ == "__main__":
    ejecutar_diagnostico()