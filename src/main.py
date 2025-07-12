import customtkinter as ctk
from PIL import Image
from diagnostico_experto import DiagnosticoPC, Sintomas
from analizar_imagen import analizar_imagen
from generar_reporte import generar_reporte
from subir_imagen import subir_imagen

class DiagnoPCApp(ctk.CTk):
    def __init__(self):
        super().__init__()
        self.title("DiagnoPC - Sistema Experto")
        self.geometry("750x650")
        self.resizable(False, False)
        self.setup_tabs()
        self.setup_tab_imagen()
        self.setup_tab_preguntas()

    def setup_tabs(self):
        self.tabs = ctk.CTkTabview(self, width=730, height=460)
        self.tabs.pack(padx=10, pady=10, expand=True)
        self.tab_img = self.tabs.add("Análisis de Imagen")
        self.tab_preg = self.tabs.add("Fase de Preguntas")

    def setup_tab_imagen(self):
        self.imagen_ruta = ""
        self.nombre_imagen = ctk.StringVar(value="Ninguna imagen seleccionada")
        self.codigo_var = ctk.StringVar(value="No detectado")
        self.codigo_pdf = ""
        self.diagnostico_img = ""

        ctk.CTkLabel(self.tab_img, text="Sube una imagen del equipo (opcional):", font=("Arial", 14)).pack(pady=(38,8))
        ctk.CTkButton(self.tab_img, text="Subir imagen", command=self.subir_imagen_ui).pack()
        ctk.CTkLabel(self.tab_img, textvariable=self.nombre_imagen).pack(pady=(6, 0))
        self.img_preview_label = ctk.CTkLabel(self.tab_img, text="")
        self.img_preview_label.pack(pady=(8, 0))
        ctk.CTkLabel(self.tab_img, text="Código de error detectado:", font=("Arial", 13)).pack(pady=(25,0))
        ctk.CTkLabel(self.tab_img, textvariable=self.codigo_var, font=("Arial", 13, "bold")).pack()
        self.diagnostico_img_label = ctk.CTkLabel(self.tab_img, text="", font=("Arial", 12))
        self.diagnostico_img_label.pack(pady=(3, 0))
        self.btn_reporte_imagen = ctk.CTkButton(
            self.tab_img, text="Generar Reporte de Imagen",
            command=self.generar_reporte_imagen, width=200
        )
        self.btn_reporte_imagen.pack(pady=(20, 0))
        self.btn_reporte_imagen.configure(state="disabled")
        self.img_msg_label = None

    def setup_tab_preguntas(self):
        frame = ctk.CTkFrame(self.tab_preg)
        frame.pack(expand=True, pady=15, padx=0)
        preguntas_frame = ctk.CTkFrame(frame, fg_color="transparent")
        preguntas_frame.pack(expand=True)

        # Configura el grid de preguntas
        for i in range(3):
            preguntas_frame.grid_rowconfigure(i, weight=1)
        preguntas_frame.grid_columnconfigure(0, weight=1)
        preguntas_frame.grid_columnconfigure(1, weight=1)

        # Preguntas principales
        self.enciende_var = ctk.StringVar(value="no")
        self.pitidos_var = ctk.StringVar(value="no")
        self.pantalla_var = ctk.StringVar(value="no")
        self.se_apaga_var = ctk.StringVar(value="no")

        self.add_pregunta_radio(preguntas_frame, "¿La computadora enciende?", self.enciende_var, 0, 0)
        self.add_pregunta_radio(preguntas_frame, "¿Emite pitidos al arrancar?", self.pitidos_var, 1, 0, self.toggle_pitido_tipo)
        self.add_pregunta_radio(preguntas_frame, "¿La pantalla muestra algo?", self.pantalla_var, 0, 1)
        self.add_pregunta_radio(preguntas_frame, "¿La computadora se apaga sola después de encender?", self.se_apaga_var, 1, 1)

        # Tipo de pitido (oculto por defecto)
        self.pitido_tipo_frame = ctk.CTkFrame(preguntas_frame, fg_color="transparent")
        self.pitido_tipo_label = ctk.CTkLabel(self.pitido_tipo_frame, text="¿Qué tipo de pitido se escucha?", font=("Arial", 13))
        self.pitido_tipo_select = ctk.CTkOptionMenu(self.pitido_tipo_frame, values=["Corto", "Largo", "Continuo"], width=180)
        self.pitido_tipo_frame.grid_remove()

        # Botones y resultado
        ctk.CTkButton(frame, text="Diagnosticar", command=self.diagnosticar, width=170).pack(pady=(20, 5))
        ctk.CTkButton(frame, text="Generar Reporte de Preguntas", command=self.generar_reporte_preguntas, width=200).pack(pady=(0, 15))
        self.resultado_label = ctk.CTkLabel(frame, text="", font=("Arial", 14, "bold"), wraplength=640, anchor="center", justify="center")
        self.resultado_label.pack(pady=(7, 0))
        self.img_tk = None
        self.ultimo_diagnostico = None
        self.ultimo_sintomas = None

    def add_pregunta_radio(self, parent, texto, variable, row, col, cmd=None):
        frame = ctk.CTkFrame(parent, fg_color="transparent")
        ctk.CTkLabel(frame, text=texto, font=("Arial", 13), wraplength=320, justify="left").pack(anchor="w")
        fila = ctk.CTkFrame(frame, fg_color="transparent")
        fila.pack(anchor="w", pady=(0, 10))
        ctk.CTkRadioButton(fila, text="Sí", variable=variable, value="si", command=cmd).pack(side="left", padx=(0,15))
        ctk.CTkRadioButton(fila, text="No", variable=variable, value="no", command=cmd).pack(side="left")
        frame.grid(row=row, column=col, sticky="ew", padx=30, pady=(0, 0))

    # --- UI Methods ---
    def reset_tab_imagen(self):
        self.nombre_imagen.set("Ninguna imagen seleccionada")
        self.codigo_var.set("No detectado")
        self.img_preview_label.configure(image=None, text="")
        self.btn_reporte_imagen.configure(state="disabled")
        self.codigo_pdf = ""
        self.diagnostico_img = ""
        self.diagnostico_img_label.configure(text="")

    def subir_imagen_ui(self):
        ruta = subir_imagen()
        if not ruta:
            self.reset_tab_imagen()
            return

        import cv2
        imagen = cv2.imread(ruta)
        mensaje, datos = analizar_imagen(imagen)
        self.imagen_ruta = ruta
        nombre = ruta.split("/")[-1] if "/" in ruta else ruta.split("\\")[-1]
        self.nombre_imagen.set(nombre)
        self.codigo_pdf = ""
        self.diagnostico_img = ""

        if "|" in datos:
            codigo, diagnostico = datos.split("|", 1)
            self.codigo_var.set(f"Error detectado: {codigo.strip()}")
            self.codigo_pdf = codigo.strip()
            self.diagnostico_img = diagnostico.strip()
        else:
            self.codigo_var.set(mensaje)
            self.codigo_pdf = mensaje.strip()
            self.diagnostico_img = ""

        img_pil = Image.open(ruta)
        img_pil.thumbnail((200, 200))
        self.img_tk = ctk.CTkImage(light_image=img_pil, dark_image=img_pil, size=img_pil.size)
        self.img_preview_label.configure(image=self.img_tk, text="")

        # Mostrar diagnóstico debajo del código de error
        self.diagnostico_img_label.configure(text=f"Diagnóstico: {self.diagnostico_img}" if self.diagnostico_img else "")

        # Activar/desactivar botón según resultado
        if "Error detectado:" in self.codigo_var.get() or "Pantalla azul" in self.codigo_var.get():
            self.btn_reporte_imagen.configure(state="normal")
        else:
            self.btn_reporte_imagen.configure(state="disabled")

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
        self.resultado_label.configure(
            text=f"Diagnóstico:\n{diagnostico}",
            font=("Arial", 14, "bold"),
            anchor="center",
            justify="center"
        )
        self.ultimo_diagnostico = diagnostico
        self.ultimo_sintomas = sintomas

    def generar_reporte_imagen(self):
        nombre = self.nombre_imagen.get()
        codigo_error = self.codigo_pdf or "-"
        diagnostico = self.diagnostico_img or "No se detectó diagnóstico."
        sintomas_img = {"nombre imagen": nombre, "codigo error": codigo_error}
        try:
            generar_reporte(
                sintomas_img,
                f"Diagnóstico basado en imagen: {diagnostico}"
            )
            if hasattr(self, 'img_msg_label') and self.img_msg_label:
                self.img_msg_label.destroy()
            self.img_msg_label = ctk.CTkLabel(self.tab_img, text="Reporte generado exitosamente.", text_color="green", font=("Arial", 12))
            self.img_msg_label.pack()
        except Exception as e:
            if hasattr(self, 'img_msg_label') and self.img_msg_label:
                self.img_msg_label.destroy()
            self.img_msg_label = ctk.CTkLabel(self.tab_img, text=f"Error al generar reporte: {e}", text_color="red", font=("Arial", 12))
            self.img_msg_label.pack()

    def generar_reporte_preguntas(self):
        if self.ultimo_diagnostico is None or self.ultimo_sintomas is None:
            self.resultado_label.configure(text="Por favor, primero realice el diagnóstico.")
            return
        try:
            sintomas_dict = dict(self.ultimo_sintomas)
            generar_reporte(
                sintomas_dict,
                self.ultimo_diagnostico
            )
            self.resultado_label.configure(text="Reporte generado exitosamente.", text_color="green")
        except Exception as e:
            self.resultado_label.configure(text=f"Error al generar reporte: {e}", text_color="red")

if __name__ == "__main__":
    ctk.set_appearance_mode("dark")
    app = DiagnoPCApp()
    app.mainloop()
