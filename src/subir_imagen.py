def subir_imagen():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    import os
    Tk().withdraw()
    ruta_imagen = askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        initialdir=os.getcwd()
    )