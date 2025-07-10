from fpdf import FPDF
from datetime import datetime

def generar_reporte(sintomas, diagnostico):
    pdf = FPDF()
    pdf.add_page()
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, "Reporte de Diagnóstico - DiagnoPC", ln=True, align='C')
    pdf.ln(10)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Fecha y hora:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.cell(0, 10, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    pdf.ln(5)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Respuestas del usuario:", ln=True)
    pdf.set_font("Arial", size=12)

    # Convertir el Fact a diccionario si no lo es
    respuestas_dict = dict(sintomas.items()) if hasattr(sintomas, 'items') else sintomas

    for clave, valor in respuestas_dict.items():
        pdf.cell(0, 10, f"{clave.replace('_', ' ').capitalize()}: {valor}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Diagnóstico del sistema experto:", ln=True)
    pdf.set_font("Arial", size=12)
    pdf.multi_cell(0, 10, f"- {diagnostico}")

    pdf.output("reporte_diagnostico.pdf")
    print(" Reporte generado como 'reporte_diagnostico.pdf'")
