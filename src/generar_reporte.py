from fpdf import FPDF
from datetime import datetime
import os

class PDF(FPDF):
    def header(self):
        self.set_fill_color(30, 144, 255)  # Azul
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

def generar_reporte(sintomas, diagnostico, codigo_error=None, solucion_error=None):
    pdf = PDF()
    pdf.add_page()
    pdf.set_font("Arial", '', 12)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(40, 10, "Fecha y hora:")
    pdf.set_font("Arial", '', 12)
    pdf.cell(0, 10, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), ln=True)
    pdf.ln(3)

    pdf.set_font("Arial", 'B', 12)
    pdf.cell(0, 10, "Respuestas del usuario:", ln=True)
    pdf.set_font("Arial", '', 11)
    pdf.set_fill_color(230, 240, 255)
    pdf.set_text_color(40, 40, 40)
    pdf.set_font("Arial", 'B', 11)
    pdf.cell(65, 8, "Pregunta", 1, 0, 'C', 1)
    pdf.cell(0, 8, "Respuesta", 1, 1, 'C', 1)
    pdf.set_font("Arial", '', 11)

    def get_val(clave):
        val = sintomas.get(clave, '-')
        return val if val not in [None, ''] else '-'

    pdf.cell(65, 8, "Enciende", 1)
    pdf.cell(0, 8, get_val('enciende'), 1, 1)
    pdf.cell(65, 8, "Pitidos", 1)
    pdf.cell(0, 8, get_val('pitidos'), 1, 1)
    pdf.cell(65, 8, "Tipo pitido", 1)
    pdf.cell(0, 8, get_val('tipo_pitido') if get_val('tipo_pitido') != "" else "-", 1, 1)
    pdf.cell(65, 8, "Pantalla", 1)
    pdf.cell(0, 8, get_val('pantalla'), 1, 1)
    pdf.cell(65, 8, "Se apaga", 1)
    pdf.cell(0, 8, get_val('se_apaga'), 1, 1)

    # Solo código de error de pantalla
    pdf.cell(65, 8, "Código de error de pantalla", 1)
    pdf.cell(0, 8, codigo_error if codigo_error else "-", 1, 1)

    pdf.ln(5)

    # Diagnóstico final (con posible solución de error)
    pdf.set_font("Arial", 'B', 12)
    pdf.set_fill_color(220, 240, 220)
    pdf.cell(0, 10, "Diagnóstico del sistema experto:", ln=True)
    pdf.set_font("Arial", '', 12)
    pdf.set_fill_color(255, 255, 240)
    texto_diag = f"{diagnostico}"
    if solucion_error:
        texto_diag += f"\n\nSolución sugerida para el código detectado:\n{solucion_error}"
    pdf.multi_cell(0, 10, texto_diag, border=1, fill=True)

    # -----------------------
    # Guardar en la carpeta /reportes con nombre personalizado
    # -----------------------
    fecha_str = datetime.now().strftime("%Y-%m-%d-%H-%M-%S")
    nombre_archivo = f"reporte-diagnostico-{fecha_str}.pdf"
    # Esta ruta apunta a /reportes (al lado de src)
    ruta_carpeta = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "reportes"))
    os.makedirs(ruta_carpeta, exist_ok=True)  # Si la carpeta no existe, la crea
    ruta_completa = os.path.join(ruta_carpeta, nombre_archivo)

    pdf.output(ruta_completa)
    print(f"Reporte generado como '{ruta_completa}'")
