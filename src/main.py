import customtkinter as ctk
from PIL import Image

from diagnostico_experto import DiagnosticoPC, Sintomas
from analizar_imagen import analizar_imagen
from generar_reporte import generar_reporte
from registro_consulta import registro_consulta
from subir_imagen import subir_imagen  # solo la función para seleccionar archivo

class DiagnoPCApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DiagnoPC - Sistema Experto")
        self.geometry("750x500")
        self.resizable(False, False)

        # --- Tabs
        self.tabs = ctk.CTkTabview(self, width=730, height=460)
        self.tabs.pack(padx=10, pady=10, expand=True)
        self.tab_img = self.tabs.add("Análisis de Imagen")
        self.tab_preg = self.tabs.add("Fase de Preguntas")

        # Variables
        self.imagen_ruta = ""
        self.nombre_imagen = ctk.StringVar(value="Ninguna imagen seleccionada")
        self.codigo_var = ctk.StringVar(value="No detectado")

        # TAB ANÁLISIS DE IMAGEN
        ctk.CTkLabel(self.tab_img, text="Sube una imagen del equipo (opcional):", font=("Arial", 14)).pack(pady=(38,8))
        ctk.CTkButton(self.tab_img, text="Subir imagen", command=self.subir_imagen_ui).pack()
        ctk.CTkLabel(self.tab_img, textvariable=self.nombre_imagen).pack(pady=(6, 0))
        
        # Vista previa
        self.img_preview_label = ctk.CTkLabel(self.tab_img, text="")
        self.img_preview_label.pack(pady=(8, 0))

        ctk.CTkLabel(self.tab_img, text="Código de error detectado:", font=("Arial", 13)).pack(pady=(25,0))
        ctk.CTkLabel(self.tab_img, textvariable=self.codigo_var, font=("Arial", 13, "bold")).pack()

        # TAB PREGUNTAS CENTRADAS
        frame = ctk.CTkFrame(self.tab_preg)
        frame.pack(expand=True, pady=15, padx=0)

        preguntas_frame = ctk.CTkFrame(frame, fg_color="transparent")
        preguntas_frame.pack(expand=True)

        for i in range(3):
            preguntas_frame.grid_rowconfigure(i, weight=1)
        preguntas_frame.grid_columnconfigure(0, weight=1)
        preguntas_frame.grid_columnconfigure(1, weight=1)

        # Pregunta 1
        self.enciende_var = ctk.StringVar(value="no")
        q1 = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        ctk.CTkLabel(q1, text="¿La computadora enciende?", font=("Arial", 13)).pack(anchor="w")
        fila1 = ctk.CTkFrame(q1, fg_color="transparent")
        fila1.pack(anchor="w", pady=(0, 10))
        ctk.CTkRadioButton(fila1, text="Sí", variable=self.enciende_var, value="si").pack(side="left", padx=(0,15))
        ctk.CTkRadioButton(fila1, text="No", variable=self.enciende_var, value="no").pack(side="left")
        q1.grid(row=0, column=0, sticky="ew", padx=30, pady=(0, 0))

        # Pregunta 2
        self.pitidos_var = ctk.StringVar(value="no")
        q2 = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        ctk.CTkLabel(q2, text="¿Emite pitidos al arrancar?", font=("Arial", 13)).pack(anchor="w")
        fila2 = ctk.CTkFrame(q2, fg_color="transparent")
        fila2.pack(anchor="w", pady=(0, 10))
        ctk.CTkRadioButton(fila2, text="Sí", variable=self.pitidos_var, value="si", command=self.toggle_pitido_tipo).pack(side="left", padx=(0,15))
        ctk.CTkRadioButton(fila2, text="No", variable=self.pitidos_var, value="no", command=self.toggle_pitido_tipo).pack(side="left")
        q2.grid(row=1, column=0, sticky="ew", padx=30, pady=(0, 0))

        # Pregunta 3
        self.pantalla_var = ctk.StringVar(value="no")
        q3 = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        ctk.CTkLabel(q3, text="¿La pantalla muestra algo?", font=("Arial", 13)).pack(anchor="w")
        fila3 = ctk.CTkFrame(q3, fg_color="transparent")
        fila3.pack(anchor="w", pady=(0, 10))
        ctk.CTkRadioButton(fila3, text="Sí", variable=self.pantalla_var, value="si").pack(side="left", padx=(0,15))
        ctk.CTkRadioButton(fila3, text="No", variable=self.pantalla_var, value="no").pack(side="left")
        q3.grid(row=0, column=1, sticky="ew", padx=30, pady=(0, 0))

        # Pregunta 4
        self.se_apaga_var = ctk.StringVar(value="no")
        q4 = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        ctk.CTkLabel(q4, text="¿La computadora se apaga sola después de encender?", font=("Arial", 13), wraplength=320, justify="left").pack(anchor="w")
        fila4 = ctk.CTkFrame(q4, fg_color="transparent")
        fila4.pack(anchor="w", pady=(0, 10))
        ctk.CTkRadioButton(fila4, text="Sí", variable=self.se_apaga_var, value="si").pack(side="left", padx=(0,15))
        ctk.CTkRadioButton(fila4, text="No", variable=self.se_apaga_var, value="no").pack(side="left")
        q4.grid(row=1, column=1, sticky="ew", padx=30, pady=(0, 0))

        # Pregunta tipo de pitido
        self.pitido_tipo_frame = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        self.pitido_tipo_label = ctk.CTkLabel(self.pitido_tipo_frame, text="¿Qué tipo de pitido se escucha?", font=("Arial", 13))
        self.pitido_tipo_select = ctk.CTkOptionMenu(self.pitido_tipo_frame, values=["Corto", "Largo", "Continuo"], width=180)
        self.pitido_tipo_frame.grid_remove()

        # Botones Diagnosticar y Generar Reporte
        ctk.CTkButton(frame, text="Diagnosticar", command=self.diagnosticar, width=170).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Generar Reporte", command=self.generar_reporte_pdf, width=170).pack(pady=(0, 15))

        self.resultado_label = ctk.CTkLabel(frame, text="", font=("Arial", 14, "bold"), wraplength=640, anchor="center", justify="center")
        self.resultado_label.pack(pady=(7, 0))

        self.img_tk = None  # Referencia para imagen preview

        # Para guardar estado actual
        self.ultimo_diagnostico = None
        self.ultimo_sintomas = None

    def subir_imagen_ui(self):
        ruta = subir_imagen()
        if ruta:
            import cv2
            imagen = cv2.imread(ruta)
            codigo = analizar_imagen(imagen) or "No detectado"
            self.imagen_ruta = ruta
            nombre = ruta.split("/")[-1] if "/" in ruta else ruta.split("\\")[-1]
            self.nombre_imagen.set(nombre)
            self.codigo_var.set(codigo)

            # Mostrar vista previa
            img_pil = Image.open(ruta)
            img_pil.thumbnail((200, 200))
            self.img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
            self.img_preview_label.configure(image=self.img_tk, text="")
        else:
            self.nombre_imagen.set("Ninguna imagen seleccionada")
            self.codigo_var.set("No detectado")
            self.img_preview_label.configure(image=None, text="")

    def toggle_pitido_tipo(self):
        if self.pitidos_var.get() == "si":
            self.pitido_tipo_frame.grid(row=2, column=0, columnspan=2, sticky="ew", pady=(10, 5))
            self.pitido_tipo_label.pack(anchor="center", pady=(0, 2))
            self.pitido_tipo_select.pack(anchor="center")
        else:
            self.pitido_tipo_frame.grid_remove()
            self.pitido_tipo_select.set("Corto")

    def diagnosticar(self):
        enciende = self.enciende_var.get()
        pitidos = self.pitidos_var.get()
        tipo_pitido = self.pitido_tipo_select.get() if pitidos == "si" else ""
        pantalla = self.pantalla_var.get()
        se_apaga = self.se_apaga_var.get()
        codigo = self.codigo_var.get()
        color_pantalla = codigo if codigo in ["azul", "negra"] else "desconocido"


        color_pantalla = codigo if codigo != "No detectado" else "desconocido"

        sintomas = Sintomas(
            enciende=enciende,
            pitidos=pitidos,
            tipo_pitido=tipo_pitido,
            pantalla=pantalla,
            se_apaga=se_apaga,
            color_pantalla=color_pantalla
        )

        experto = DiagnosticoPC()
        experto.reset()
        experto.declare(sintomas)
        experto.run()
        diagnostico = experto.diagnostico_final or "No se pudo determinar el problema."

        self.resultado_label.configure(text=diagnostico)

        self.ultimo_diagnostico = diagnostico
        self.ultimo_sintomas = sintomas

    def generar_reporte_pdf(self):
        if self.ultimo_diagnostico is None or self.ultimo_sintomas is None:
            self.resultado_label.configure(text="Por favor, primero realice el diagnóstico.")
            return
        try:
            registro_consulta(str(self.ultimo_sintomas), self.ultimo_diagnostico)
        except Exception as e:
            print("Error al registrar consulta:", e)
        try:
            # Detecta código de error y posible solución
            codigo_detectado = self.codigo_var.get()
            codigo_error, solucion_error = "-", None
            if "Error detectado:" in codigo_detectado:
                lines = codigo_detectado.split('\n')
                cod = lines[0].replace("Error detectado:", "").strip()
                codigo_error = cod if cod else "-"
                if len(lines) > 1 and "Solución:" in lines[1]:
                    solucion_error = lines[1].replace("Solución:", "").strip()
            elif codigo_detectado not in ["No detectado", "-", "", None]:
                codigo_error = codigo_detectado.strip()

            generar_reporte(
                self.ultimo_sintomas,
                self.ultimo_diagnostico,
                codigo_error=codigo_error,
                solucion_error=solucion_error
            )
            self.resultado_label.configure(text="Reporte generado exitosamente.")
        except Exception as e:
            self.resultado_label.configure(text=f"Error al generar reporte: {e}")



if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = DiagnoPCApp()
    app.mainloop()