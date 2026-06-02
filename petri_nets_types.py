import numpy as np


class Petri_Nets:
    def __init__(self, pre, post):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.C = self.post - self.pre

    def is_state_machine(self):
        """
        Each transition just have 1 input place and 1 output place.
        The summatory of each transition on C must be 0.
        """
        c_transpose = self.C.T
        for row in c_transpose:
            row_counter = np.sum(row)
            if row_counter != 0:
                print("This PN is not a SM, checking if it is a GM or FC")
                break
        print("This PN is a SM, each transition just have 1 input place and 1 output place.")
        print("Also, for definition, it is a FC")

    def is_marked_graph(self):
        """
        Each place just have 1 input transition and 1 output transition.
        The summatory of each place on C must be 0.
        """

    def is_free_choice(self):
        """_summary_
        """