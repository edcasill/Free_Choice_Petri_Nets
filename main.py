import os
import ast
import petri_nets_types
import st_components
import st_comp_raw
from visualizer import PetriVisualizer


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


def analize_net(archivo_seleccionado):
    print(f"\nAnalizando el archivo: {archivo_seleccionado}")
    pre, post = read_file(archivo_seleccionado)

    if pre is not None and post is not None:
        try:
            print("1. Validar si es GM, ME y FC")
            print("2. Encontrar S y T componentes")
            print("3. Encontrar S y T componentes por busqueda")
            option = int(input('Selecciona el analisis a realizar: '))
            if option == 1:
                pn = petri_nets_types.Petri_Nets(pre, post)
                pn.evaluation()
            elif option == 2:
                pn = st_components.components(pre, post)
                s_components, s_cover, t_components, t_cover = pn.get_components()
                vis = PetriVisualizer(pre, post, output_dir="grafos_generados")

                vis.dibujar_red(nombre_archivo="1_Red_Original")
                vis.visualizar_s_componentes(s_components, prefijo="2_S_Comp")
                vis.visualizar_s_componentes(s_cover, prefijo="3_S_Cover")
                vis.visualizar_t_componentes(t_components, prefijo="4_T_Comp")
                vis.visualizar_t_componentes(t_cover, prefijo="5_T_Cover")

                s_components = ajustar_inicio(s_components)
                s_cover = ajustar_inicio(s_cover)
                t_components = ajustar_inicio(t_components)
                t_cover = ajustar_inicio(t_cover)
                print(f"Los S-componentes son {s_components}\nLas S-coverturas son {s_cover}")
                print(f"Los T-componentes son {t_components}\nLas T-coverturas son {t_cover}")
            elif option == 3:
                pn = st_comp_raw.components(pre, post)
                s_components, t_components = pn.get_components()
                print(f"Los S-componentes son {s_components}")
                print(f"Los T-componentes son {t_components}")
        except ValueError:
            print("Entrada inválida. Por favor ingresa un número entero.")


def ajustar_inicio(componente):
    """
    Ajusta el inicio de los nodos a 1 en lugar de 0
    """
    return [[nodo + 1 for nodo in comp] for comp in componente]


def main():
    archivos = [f for f in os.listdir('.') if f.endswith('.txt') and not f.startswith('pseudocode')]
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
            analize_net(archivo_seleccionado)
        else:
            print("El número seleccionado no está en la lista.")

    except ValueError:
        print("Entrada inválida. Por favor ingresa un número entero.")

if __name__ == "__main__":
    main()