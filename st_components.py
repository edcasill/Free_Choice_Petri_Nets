import numpy as np


class components:
    def __init__(self, pre, post):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.pre_transpose = self.pre.T
        self.post_transpose = self.post.T

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
                    new_rows.append(new_row)

                    # update matrix
                    # o rows + new rows
                    if new_rows:
                        A = np.vstack((A_zero, np.array(new_rows)))
                    elif len(A_zero) > 0:
                        A = A_zero
                    else:
                        break

        invariants = A[:, n_rows]
        invariants = invariants[~np.all(invariants == 0, axis=1)]

        return invariants

    def s_components_filter(self, S_invariants):
        """
        Filter the s_invariants and calculate the S_components
        """

    def t_components_filter(self, T_invariants):
        """
        Filter the t_invariants and calculate the T_components
        """

    def get_components(self):
        S_invariants = self.calculate_invariants(use_transpose=False)
        T_invariants = self.calculate_invariants(use_transpose=True)
        S_components = self.s_components_filter(S_invariants)
        T_components = self.t_components_filter(T_invariants)
        return S_components, T_components