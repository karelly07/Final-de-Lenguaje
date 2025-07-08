from fpdf import FPDF
from datetime import datetime

def generar_reporte(respuestas, diagnosticos):
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
    for clave, valor in respuestas.items():
        pdf.cell(0, 10, f"{clave.capitalize()}: {valor}", ln=True)

    pdf.ln(5)
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Diagnóstico del sistema experto:", ln=True)
    pdf.set_font("Arial", size=12)
    for diag in diagnosticos:
        pdf.multi_cell(0, 10, f"• {diag}")

    pdf.output("reporte_diagnostico.pdf")
    print("Reporte generado como 'reporte_diagnostico.pdf'")
