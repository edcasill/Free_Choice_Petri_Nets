import numpy as np
import itertools


class components:
    def __init__(self, pre, post):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.pre_transpose = self.pre.T
        self.post_transpose = self.post.T

    def _filter_minimal(self, A, n_rows):
        """
        Elimina las filas cuyo soporte en la submatriz D es un superconjunto 
        estricto de otra fila, garantizando invariantes mínimos.
        """
        D = A[:, :n_rows]
        S = (D != 0)  # Matriz booleana de soportes (True donde hay valores > 0)
        keep = []

        for i in range(len(S)):
            is_minimal = True
            for j in range(len(S)):
                if i == j:
                    continue

                # S[j] es subconjunto de S[i] si todos los True en S[j] también son True en S[i]
                if np.all(S[j] <= S[i]):
                    # Si tienen exactamente el mismo soporte, conservamos solo el primero
                    if np.array_equal(S[i], S[j]):
                        if j < i:
                            is_minimal = False
                            break
                    else:
                        # S[j] es un subconjunto estricto de S[i], por lo tanto i no es mínimo
                        is_minimal = False
                        break

            if is_minimal:
                keep.append(i)

        return A[keep]

    def calculate_invariants(self, use_transpose=False):
        """
        Calculate S-invariants and P invariants
        """
        C = self.post - self.pre
        if use_transpose:
            C = C.T

        n_rows, m_cols = C.shape  # size the matrix
        D = np.eye(n_rows, dtype=int)  # identity matrix
        A = np.hstack((D,C)).astype(int)  # augmented matrix [D|C]

        for i in range(m_cols):
            col_index = n_rows + i
            # filtering
            A_zero = A[A[:, col_index] == 0]  # rows that are null on the column
            A_pos = A[A[:, col_index] > 0]  # positive rows
            A_neg = A[A[:, col_index] < 0]  # negative rows

            new_rows = []

            # lineal combinations
            # anulate column using positive and negative rows
            for row_p in A_pos:
                for row_n in A_neg:
                    pos_val = row_p[col_index]
                    neg_val = abs(row_n[col_index])

                    # MCD
                    gcd_val = np.gcd(pos_val, neg_val)
                    mult_p = neg_val // gcd_val
                    mult_n = pos_val // gcd_val

                    # new null row
                    new_row = (mult_p * row_p) + (mult_n * row_n)
                    non_zero_elements = new_row[new_row != 0]
                    if len(non_zero_elements) > 0:
                        row_gcd = np.gcd.reduce(non_zero_elements)
                        if row_gcd > 1:
                            new_row = new_row // row_gcd
                    new_rows.append(new_row)

            # update matrix
            # 0 rows + new rows
            if new_rows:
                A = np.vstack((A_zero, np.array(new_rows)))
            elif len(A_zero) > 0:
                A = A_zero
            else:
                break
            A = self._filter_minimal(A, n_rows)

        # slicing to get all columns from D
        invariants = A[:, :n_rows]
        invariants = invariants[~np.all(invariants == 0, axis=1)]
        print(f"The invariant is {invariants}")

        return invariants

    def s_components_filter(self, S_invariants):
        """
        Filter the s_invariants and calculate the S_components
        """
        s_comp = []

        for Is in S_invariants:
            # aislar filas
            s_index = np.where(Is >= 1)[0]
            if len(s_index) == 0:
                continue

            pre_rows = self.pre[s_index, :]
            post_rows = self.post[s_index, :]

            conections = (pre_rows > 0) | (post_rows > 0)
            T_index = np.where(np.any(conections, axis=0))[0]

            if len(T_index) == 0:
                continue

            pre_sub = self.pre[np.ix_(s_index, T_index)]
            post_sub = self.post[np.ix_(s_index, T_index)]

            sum_trans_pre = np.sum(pre_sub, axis=0)
            sum_trans_post = np.sum(post_sub, axis=0)

            if np.all(sum_trans_pre == 1) and np.all(sum_trans_post == 1):
                s_comp.append(s_index.tolist())
        return s_comp
        

    def t_components_filter(self, T_invariants):
        """
        Filter the t_invariants and calculate the T_components
        """
        t_comp = []

        for It in T_invariants:
            t_index = np.where(It >= 1)[0]
            if len(t_index) == 0:
                continue

            pre_rows = self.pre_transpose[t_index, :]
            post_rows = self.post_transpose[t_index, :]

            conections = (pre_rows > 0) | (post_rows > 0)
            s_index = np.where(np.any(conections, axis=0))[0]

            if len(s_index) == 0:
                continue

            pre_sub = self.pre_transpose[np.ix_(t_index, s_index)]
            post_sub = self.post_transpose[np.ix_(t_index, s_index)]

            sum_place_pre = np.sum(pre_sub, axis=0)
            sum_place_post = np.sum(post_sub, axis=0)

            if np.all(sum_place_pre == 1) and np.all(sum_place_post == 1):
                t_comp.append(t_index.tolist())
        return t_comp
    
    def _get_cover(self, components, total_elements):
        """
        Extrae un recubrimiento mínimo (Cover) a partir de una lista de componentes.
        Retorna el conjunto mínimo de componentes que cubren la red (lugares o transiciones).
        """
        required_items = set(range(total_elements))

        # Buscamos la combinación más pequeña: de tamaño 1 hasta el total de componentes
        for r in range(1, len(components) + 1):
            for combo in itertools.combinations(components, r):
                # Unimos todos los elementos de la combinación actual
                covered = set(item for comp in combo for item in comp)
                
                # Si esta combinación cubre todos los elementos necesarios, ¡es la mínima!
                if covered.issuperset(required_items):
                    # Convertimos la tupla de itertools de regreso a una lista
                    return list(combo)

        return components

    def get_components(self):
        S_invariants = self.calculate_invariants(use_transpose=False)
        T_invariants = self.calculate_invariants(use_transpose=True)

        S_components = self.s_components_filter(S_invariants)
        T_components = self.t_components_filter(T_invariants)

        # 3. Extraemos el recubrimiento mínimo
        # Para S-components, debemos cubrir todos los lugares (shape[0])
        total_places = self.pre.shape[0]
        S_cover = self._get_cover(S_components, total_places)
        
        # Para T-components, debemos cubrir todas las transiciones (shape[1])
        total_transitions = self.pre.shape[1]
        T_cover = self._get_cover(T_components, total_transitions)
        return S_components,S_cover, T_components, T_cover