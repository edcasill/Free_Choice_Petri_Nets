import os
import ast
import petri_nets_types


def read_file(file):
    """
    Read a .txt file and extract the pre and post matrices
    """
    with open(file, 'r') as f:
        data = f.read()

    try:
        pre_str = data.split('pre =')[1].split('post =')[0].strip()
        post_str = data.split('post =')[1].strip()

        # ast.literal_eval transform the string "[[1, 0], [0, 1]]" into a list
        pre = ast.literal_eval(pre_str)
        post = ast.literal_eval(post_str)
        return pre, post

    except Exception as e:
        print(f"Error al procesar el formato del archivo {file}: {e}")
        return None, None


def main():
    archivos = [f for f in os.listdir('.') if f.endswith('.txt')]
    if not archivos:
        print("No se encontraron archivos .txt en el directorio.")
        return

    print("--- Archivos Disponibles ---")
    for i, archivo in enumerate(archivos, start=1):
        print(f"{i}. {archivo}")
    print("----------------------------")

    try:
        option = int(input('Selecciona el número de archivo a analizar: '))

        # Validar que la opción esté dentro del rango
        if 1 <= option <= len(archivos):
            archivo_seleccionado = archivos[option - 1]
            print(f"\nAnalizando el archivo: {archivo_seleccionado}")

            pre, post = read_file(archivo_seleccionado)

            if pre is not None and post is not None:
                pn = petri_nets_types.Petri_Nets(pre, post)
                pn.evaluation()
        else:
            print("El número seleccionado no está en la lista.")

    except ValueError:
        print("Entrada inválida. Por favor ingresa un número entero.")

if __name__ == "__main__":
    main()