from experta import *

class Sintomas(Fact):
    """Hechos que representan los síntomas observados en el PC"""
    enciende = Field(str, default="no")
    pitidos = Field(str, default="no")
    tipo_pitido = Field(str, default="")
    pantalla = Field(str, default="no")
    se_apaga = Field(str, default="no")  # Se puede usar si se implementa en main.py
    color_pantalla = Field(str, default="")

class DiagnosticoPC(KnowledgeEngine):
    def __init__(self):
        super().__init__()
        self.diagnostico_final = ""

    @Rule(Sintomas(enciende="no"))
    def fuente_poder(self):
        self.diagnostico_final = "La computadora no enciende. Revisa la fuente de poder o el cable de energía."

    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="si"), Sintomas(pantalla="no"))
    def problema_video_o_ram(self):
        self.diagnostico_final = "Pitidos sin imagen. Posible problema con la tarjeta gráfica o la memoria RAM."
    
    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="si"), Sintomas(pantalla="si"))
    def problema_tarjeta_grafica(self):
        self.diagnostico_final = "Pitidos y pantalla encendida. Posible problema con la tarjeta gráfica o configuración de BIOS."

    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="no"), Sintomas(pantalla="no"))
    def placa_o_ram(self):
        self.diagnostico_final = "No hay pitidos ni imagen. Posible falla en la placa madre o la memoria RAM."

    @Rule(Sintomas(enciende="si"), Sintomas(pantalla="si"), Sintomas(se_apaga="si"))
    def sobrecalentamiento(self):
        self.diagnostico_final = "Se apaga sola. Posible sobrecalentamiento o fuente inestable."

    @Rule(Sintomas(enciende="si"), Sintomas(pantalla="si"), Sintomas(se_apaga="no"))
    def sin_fallas_graves(self):
        self.diagnostico_final = "Sin fallas graves detectadas. El sistema parece funcionar normalmente o tiene fallas menores (software)."

    @Rule(Sintomas(color_pantalla="azul"))
    def pantalla_azul(self):
        self.diagnostico_final = "Pantalla azul detectada. Posible fallo crítico del sistema operativo (BSOD)."

    @Rule(Sintomas(color_pantalla="negra"))
    def pantalla_negra(self):
        self.diagnostico_final = "Pantalla negra detectada. Posible problema de señal, tarjeta gráfica o sistema apagado."
