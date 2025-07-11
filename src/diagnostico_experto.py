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

    @Rule(Sintomas(color_pantalla="negra"), Sintomas(enciende="no"))
    def pantalla_negra_no_enciende(self):
        self.diagnostico_final = (
            "Pantalla negra y no enciende. Revisa la fuente de poder, el cableado, o la placa base. "
            "Prueba con otra fuente o en otra toma eléctrica."
        )

    @Rule(Sintomas(color_pantalla="negra"), Sintomas(enciende="si"), Sintomas(pitidos="si"))
    def pantalla_negra_con_pitidos(self):
        self.diagnostico_final = (
            "Pantalla negra con pitidos. Puede ser un error de memoria RAM o tarjeta gráfica. "
            "Revisa el patrón de los pitidos: \n"
            "- 1 largo y 2 cortos: error en la tarjeta de video.\n"
            "- Pitidos continuos: posible RAM defectuosa.\n"
            "- Sin pitidos: problema más grave en CPU o placa."
        )

    @Rule(Sintomas(color_pantalla="negra"), Sintomas(enciende="si"), Sintomas(pitidos="no"))
    def pantalla_negra_sin_pitidos(self):
        self.diagnostico_final = (
            "Pantalla negra pero enciende sin pitidos. Es posible que la BIOS no esté funcionando correctamente, "
            "o que haya un daño en el procesador o placa madre. También puede ser que no haya señal de video al monitor."
        )