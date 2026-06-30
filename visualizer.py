import graphviz
import numpy as np
import os

class PetriVisualizer:
    def __init__(self, pre, post, output_dir="output_grafos"):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.num_lugares, self.num_transiciones = self.pre.shape
        self.output_dir = output_dir
        
        # Crear la carpeta de salida si no existe
        if not os.path.exists(self.output_dir):
            os.makedirs(self.output_dir)

    def dibujar_red(self, lugares_resaltados=None, trans_resaltadas=None, nombre_archivo="red_base"):
        """
        Dibuja la red de Petri. Si se pasan listas de lugares y transiciones, los resalta.
        """
        lugares_resaltados = lugares_resaltados or []
        trans_resaltadas = trans_resaltadas or []

        # Configuración del grafo (LR = Left to Right)
        dot = graphviz.Digraph(comment=nombre_archivo, format='png', engine='neato')
        dot.attr(splines='line', overlap='false', size='10,8')
        '''dot.attr(rankdir='TB',
                 splines='line',
                 nodesep='0.4',
                 ranksep='0.6',
                 size='10,8')
        '''
        # 1. Dibujar Lugares (Círculos)
        for i in range(self.num_lugares):
            # Sumamos 1 para que visualmente empiece en P1, T1
            nombre_nodo = f'p{i+1}'
            if i in lugares_resaltados:
                dot.node(nombre_nodo, shape='circle', style='filled', fillcolor='lightblue', color='blue', penwidth='2')
            else:
                dot.node(nombre_nodo, shape='circle')

        # 2. Dibujar Transiciones (Cajas)
        for j in range(self.num_transiciones):
            nombre_nodo = f't{j+1}'
            if j in trans_resaltadas:
                dot.node(nombre_nodo, shape='box', style='filled', fillcolor='lightgreen', color='darkgreen', penwidth='2')
            else:
                dot.node(nombre_nodo, shape='box', style='filled', fillcolor='black', fontcolor='white')

        # 3. Dibujar Arcos (Pre y Post)
        for i in range(self.num_lugares):
            for j in range(self.num_transiciones):
                # Arcos de Lugar a Transición (Pre)
                peso_pre = self.pre[i, j]
                if peso_pre > 0:
                    label = str(peso_pre) if peso_pre > 1 else ""
                    # Si ambos nodos están resaltados, resaltamos la flecha
                    if i in lugares_resaltados and j in trans_resaltadas:
                        dot.edge(f'p{i+1}', f't{j+1}', label=label, color='red', penwidth='2')
                    else:
                        dot.edge(f'p{i+1}', f't{j+1}', label=label)

                # Arcos de Transición a Lugar (Post)
                peso_post = self.post[i, j]
                if peso_post > 0:
                    label = str(peso_post) if peso_post > 1 else ""
                    if i in lugares_resaltados and j in trans_resaltadas:
                        dot.edge(f't{j+1}', f'p{i+1}', label=label, color='red', penwidth='2')
                    else:
                        dot.edge(f't{j+1}', f'p{i+1}', label=label)

        # Guardar y renderizar
        ruta_salida = os.path.join(self.output_dir, nombre_archivo)
        dot.render(ruta_salida, view=False, cleanup=True)
        print(f"Grafo generado: {ruta_salida}.png")

    def visualizar_s_componentes(self, s_componentes, prefijo="S_Comp"):
        """Calcula las transiciones conectadas a cada S-Componente y los dibuja."""
        for idx, lugares in enumerate(s_componentes):
            # Encontrar transiciones conectadas (las que tienen arcos con estos lugares)
            pre_rows = self.pre[lugares, :]
            post_rows = self.post[lugares, :]
            conexiones = (pre_rows > 0) | (post_rows > 0)
            transiciones_conectadas = np.where(np.any(conexiones, axis=0))[0].tolist()
            
            self.dibujar_red(lugares_resaltados=lugares, 
                             trans_resaltadas=transiciones_conectadas, 
                             nombre_archivo=f"{prefijo}_{idx+1}")

    def visualizar_t_componentes(self, t_componentes, prefijo="T_Comp"):
        """Calcula los lugares conectados a cada T-Componente y los dibuja."""
        for idx, transiciones in enumerate(t_componentes):
            # Encontrar lugares conectados a estas transiciones
            pre_cols = self.pre[:, transiciones]
            post_cols = self.post[:, transiciones]
            conexiones = (pre_cols > 0) | (post_cols > 0)
            lugares_conectados = np.where(np.any(conexiones, axis=1))[0].tolist()
            
            self.dibujar_red(lugares_resaltados=lugares_conectados, 
                             trans_resaltadas=transiciones, 
                             nombre_archivo=f"{prefijo}_{idx+1}")