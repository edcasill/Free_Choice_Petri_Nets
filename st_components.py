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
        if use_transpose == True:
            C = self.C.T

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