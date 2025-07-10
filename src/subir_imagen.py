def subir_imagen():
    from tkinter import Tk
    from tkinter.filedialog import askopenfilename
    import os

    root = Tk()
    root.withdraw()  # Oculta la ventana principal

    ruta_imagen = askopenfilename(
        title="Selecciona una imagen",
        filetypes=[("Imágenes", "*.png;*.jpg;*.jpeg;*.bmp;*.gif")],
        initialdir=os.getcwd()
    )

    root.destroy()  # Cierra la instancia de Tk
    return ruta_imagen if ruta_imagen else None
