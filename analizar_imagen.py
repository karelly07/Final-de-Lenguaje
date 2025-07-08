import cv2

def analizar_imagen(ruta_imagen):
    try:
        imagen = cv2.imread(ruta_imagen)
        if imagen is None:
            print("No se pudo cargar la imagen:", ruta_imagen)
            return "desconocido"

        imagen = cv2.resize(imagen, (200, 200))
        hsv = cv2.cvtColor(imagen, cv2.COLOR_BGR2HSV)
        promedio = cv2.mean(hsv)[:3]
        h, s, v = promedio

        print(f"Color promedio HSV: H={h:.2f}, S={s:.2f}, V={v:.2f}")

        if v < 50:
            return "negra"
        elif 90 < h < 130 and s > 50:
            return "azul"
        else:
            return "otra"

    except Exception as e:
        print(f"Error analizando imagen: {e}")
        return "desconocido"
