import numpy as np


class components:
    def __init__(self, pre, post):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.total_places = self.pre.shape[0]
        self.total_transitions = self.pre.shape[1]
        self.s_components = []
        self.t_components = []
    
    def search_s_component(self, place):
        S_set = set(place)
        tran_conn = set()

        # obtiene las trnasiciones conexas en la subred
        for s in S_set:
            for t in range(self.total_transitions):
                if self.pre[s, t] > 0 or self.post[s, t] > 0:
                    tran_conn.add(t)

        # valida un solo lugar de entrada y salida (mauina de estados) y reliza poda del arbol
        for t in tran_conn:
            entradas_S = set(self.get_in_places(t)) & S_set  # & para la interseccion
            salidas_S = set(self.get_out_places(t)) & S_set
            if len(entradas_S) > 1 or len(salidas_S) > 1:
                return  # camino invalido, backtrack

        # expandir la busqueda
        complete = True
        for t in tran_conn:
            entradas_S = set(self.get_in_places(t)) & S_set
            salidas_S = set(self.get_out_places(t)) & S_set

            if len(entradas_S) == 0:
                complete = False
                for posible_lugar in self.get_in_places(t):
                    if posible_lugar not in S_set:
                        # ramificacion de nuevo conjunto
                        new_S = list(S_set | {posible_lugar})
                        self.search_s_component(new_S)
                break
            if len(salidas_S) == 0:
                complete = False
                for posible_lugar in self.get_out_places(t):
                    if posible_lugar not in S_set:
                        new_S = list(S_set | {posible_lugar})
                        self.search_s_component(new_S)
                break
        if complete:
            componente_encontrado = sorted(list(S_set))
            if componente_encontrado not in self.s_components:
                self.s_components.append(componente_encontrado)

    def search_t_component(self, transition):
        T_set = set(transition)
        place_conn = set()

        # obtiene las trnasiciones conexas en la subred
        for t in T_set:
            for s in range(self.total_places):
                if self.pre[s, t] > 0 or self.post[s, t] > 0:
                    place_conn.add(s)

        # valida un solo trnasicion de entrada y salida (grafo marcado) y reliza poda del arbol
        for s in place_conn:
            entradas_T = set(self.get_in_tran(s)) & T_set  # & para la interseccion
            salidas_T = set(self.get_out_tran(s)) & T_set
            if len(entradas_T) > 1 or len(salidas_T) > 1:
                return  # camino invalido, backtrack

        # expandir la busqueda
        complete = True
        for s in place_conn:
            entradas_T = set(self.get_in_tran(s)) & T_set
            salidas_T = set(self.get_out_tran(s)) & T_set

            if len(entradas_T) == 0:
                complete = False
                for posible_lugar in self.get_in_tran(s):
                    if posible_lugar not in T_set:
                        # ramificacion de nuevo conjunto
                        new_S = list(T_set | {posible_lugar})
                        self.search_s_component(new_S)
                break
            if len(salidas_T) == 0:
                complete = False
                for posible_lugar in self.get_out_tran(s):
                    if posible_lugar not in T_set:
                        new_S = list(T_set | {posible_lugar})
                        self.search_s_component(new_S)
                break
        if complete:
            componente_encontrado = sorted(list(T_set))
            if componente_encontrado not in self.s_components:
                self.s_components.append(componente_encontrado)

    def get_in_places(self, t):
        in_places = []
        for s in range(self.total_places):
            if self.pre[s, t] > 0:
                in_places.append(s)
        return in_places
    
    def get_in_tran(self, s):
        in_tran = []
        for t in range(self.total_transitions):
            if self.pre_transpose[s, t] > 0:
                in_tran.append(t)
        return in_tran

    def get_out_places(self, t):
        out_places = []
        for s in range(self.total_places):
            if self.post[s, t] > 0:
                out_places.append(s)
        return out_places
    
    def get_out_tran(self, s):
        out_tran = []
        for t in range(self.total_transitions):
            if self.post_transpose[s, t] > 0:
                out_tran.append(t)
        return out_tran
    
    def get_components(self):
        """
        Calculate the S-Components and T-Components

        Returns:
            S_components
            T_components
        """
        self.s_components = []
        self.t_components = []

        for place in range(self.total_places):
            self.search_s_component([place])

        for transition in range(self.total_transitions):
            self.search_t_component([transition])

        return self.s_components, self.t_components