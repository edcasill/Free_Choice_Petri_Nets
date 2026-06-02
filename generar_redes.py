import graphviz

def dibujar_red_petri(pre, post, nombre):
    # Crear el grafo dirigido
    dot = graphviz.Digraph(name=nombre, format='png')
    dot.attr(rankdir='LR') # Dirección de izquierda a derecha
    
    lugares = len(pre)
    transiciones = len(pre[0]) if lugares > 0 else 0
    
    # 1. Dibujar Lugares (P0, P1...) como círculos
    for i in range(lugares):
        dot.node(f'P{i}', f'P{i}', shape='circle', style='filled', fillcolor='white')
        
    # 2. Dibujar Transiciones (T0, T1...) como cajas negras
    for j in range(transiciones):
        dot.node(f'T{j}', f'T{j}', shape='box', style='filled', fillcolor='black', fontcolor='white')
        
    # 3. Dibujar Arcos de Entrada (Matriz Pre: Lugares -> Transiciones)
    for i in range(lugares):
        for j in range(transiciones):
            if pre[i][j] == 1:
                dot.edge(f'P{i}', f'T{j}')
                
    # 4. Dibujar Arcos de Salida (Matriz Post: Transiciones -> Lugares)
    for i in range(lugares):
        for j in range(transiciones):
            if post[i][j] == 1:
                dot.edge(f'T{j}', f'P{i}')
                
    # Guardar y renderizar la imagen
    dot.render(nombre, cleanup=True)
    print(f"Imagen generada con éxito: {nombre}.png")


# ==========================================
# MATRICES DE TUS EJEMPLOS
# ==========================================

# 1. Red Free-Choice
pre_fc = [
    [1, 1, 0, 0], 
    [0, 0, 1, 0], 
    [0, 0, 1, 0], 
    [0, 0, 0, 1], 
    [0, 0, 0, 1], 
    [0, 0, 0, 0]
]
post_fc = [
    [0, 0, 0, 0], 
    [1, 0, 0, 0], 
    [1, 0, 0, 0], 
    [0, 1, 0, 1], 
    [0, 0, 1, 1], 
    [0, 0, 0, 1]
]
dibujar_red_petri(pre_fc, post_fc, 'Ejemplo_FreeChoice')

# 2. Grafo Marcado
pre_mg = [
    [1, 0, 0], 
    [0, 1, 0], 
    [0, 1, 0], 
    [0, 0, 1]
]
post_mg = [
    [0, 0, 1], 
    [1, 0, 0], 
    [1, 0, 0], 
    [0, 1, 0]
]
dibujar_red_petri(pre_mg, post_mg, 'Ejemplo_GrafoMarcado')

# 3. Máquina de Estados
pre_sm = [
    [1, 1, 0, 0], 
    [0, 0, 1, 0], 
    [0, 0, 0, 1], 
    [0, 0, 0, 0]
]
post_sm = [
    [0, 0, 0, 0], 
    [1, 0, 0, 0], 
    [0, 1, 0, 0], 
    [0, 0, 1, 1]
]
dibujar_red_petri(pre_sm, post_sm, 'Ejemplo_MaquinaEstados')