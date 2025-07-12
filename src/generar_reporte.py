from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_fill_color(30, 144, 255)
        self.set_text_color(255, 255, 255)
        self.set_font("Arial", 'B', 16)
        self.cell(0, 15, "Reporte de Diagnóstico - DiagnoPC", 0, 1, 'C', fill=True)
        self.set_draw_color(30, 144, 255)
        self.set_line_width(1)
        self.line(10, 25, 200, 25)
        self.ln(10)
        self.set_text_color(0, 0, 0)

    def footer(self):
        self.set_y(-15)
        self.set_font('Arial', 'I', 8)
        self.set_text_color(128, 128, 128)
        self.cell(0, 10, f'DiagnoPC | Generado: {datetime.now().strftime("%Y-%m-%d %H:%M:%S")}', 0, 0, 'C')

def generar_reporte(sintomas, diagnostico):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)

    # Fecha y hora
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Fecha y hora:")
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    pdf.ln(3)

    # Datos del reporte
    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Datos del reporte:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.set_fill_color(230, 240, 255)
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Arial", 'B', 11)
    campos_excluir = ["color_pantalla", "factid"]

    for k, v in sintomas.items():
        if k in campos_excluir:
            continue
        valor = str(v) if str(v).strip() not in ["", "None"] else "-"
        pdf.cell(65, 8, str(k).capitalize().replace('_', ' '), 1)
        pdf.cell(0, 8, valor, 1, 1)
    pdf.ln(5)

    # Diagnóstico
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(220, 240, 220)
    pdf.cell(0, 10, "Diagnóstico:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(255, 255, 240)
    pdf.multi_cell(0, 10, diagnostico, border=1, fill=True)

    fecha_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    nombre_archivo = f"reporte-diagnostico-{fecha_str}.pdf"
    ruta_carpeta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reportes"))
    os.makedirs(ruta_carpeta, exist_ok=True)
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)
    pdf.output(ruta_completa)
    print(f"Reporte generado como '{ruta_completa}'")
