def registro_consulta(consulta, respuesta):

    with open("registro_consultas.txt", "a") as file:
        file.write(f"Consulta: {consulta}\n")
        file.write(f"Respuesta: {respuesta}\n")
        file.write("-" * 40 + "\n")  # Separador entre consultas
        def leer_registro():
            with open("registro_consultas.txt", "r") as file:
                contenido = file.read()
            return contenido

