def registro_consulta(consulta, respuesta):
    with open("registro_consultas.txt", "a", encoding="utf-8") as file:
        file.write(f"Consulta: {consulta}\n")
        file.write(f"Respuesta: {respuesta}\n")
        file.write("-" * 40 + "\n")  # Separador entre consultas

def leer_registro():
    try:
        with open("registro_consultas.txt", "r", encoding="utf-8") as file:
            contenido = file.read()
        return contenido
    except FileNotFoundError:
        return "No hay consultas registradas todavía."
