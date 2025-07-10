from experta import *

class Sintomas(Fact):
    pass

class DiagnosticoPC(KnowledgeEngine):
    @Rule(Sintomas(enciende="no"))
    def fuente_poder(self):
        print("Diagnóstico: La computadora no enciende.")
        print("Revisa la fuente de poder o el cable de energía.")

    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="si"), Sintomas(pantalla="no"))
    def problema_video_o_ram(self):
        print("Diagnóstico: Pitidos sin imagen.")
        print("Posible problema con la tarjeta gráfica o la memoria RAM.")
    
    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="si"), Sintomas(pantalla="si"))
    def problema_tarjeta_grafica(self):
        print("Diagnóstico: Pitidos y pantalla encendida.")
        print("Posible problema con la tarjeta gráfica o configuración de BIOS.")

    @Rule(Sintomas(enciende="si"), Sintomas(pitidos="no"), Sintomas(pantalla="no"))
    def placa_o_ram(self):
        print("Diagnóstico: No hay pitidos ni imagen.")
        print("Posible falla en la placa madre o la memoria RAM.")

    @Rule(Sintomas(enciende="si"), Sintomas(pantalla="si"), Sintomas(se_apaga="si"))
    def sobrecalentamiento(self):
        print("Diagnóstico: Se apaga sola.")
        print("Posible sobrecalentamiento o fuente inestable.")

    @Rule(Sintomas(enciende="si"), Sintomas(pantalla="si"), Sintomas(se_apaga="no"))
    def sin_fallas_graves(self):
        print("Diagnóstico: Sin fallas graves detectadas.")
        print("El sistema parece funcionar normalmente o tiene fallas menores (software).")

    @Rule(Sintomas(color_pantalla="azul"))
    def pantalla_azul(self):
        print("Diagnóstico visual: Pantalla azul detectada.")
        print("Posible fallo crítico de sistema operativo (BSOD).")

    @Rule(Sintomas(color_pantalla="negra"))
    def pantalla_negra(self):
        print("Diagnóstico visual: Pantalla negra detectada.")
        print("Posible problema de señal, tarjeta gráfica o sistema apagado.")
    
