import numpy as np


class Petri_Nets:
    def __init__(self, pre, post):
        self.pre = np.array(pre)
        self.post = np.array(post)
        self.pre_transpose = self.pre.T
        self.post_transpose = self.post.T

    def is_marked_graph(self):
        """
        Each place just have 1 input transition and 1 output transition.
        The summatory of each place on C must be 0.
        """
        flag_me = True
        for row in range(len(self.pre)):
            sum_place_pre = np.sum(self.pre[row])
            sum_place_post = np.sum(self.post[row])

            if sum_place_pre != 1 or sum_place_post != 1:
                print("Is not a marked graph, try state machine and free-choice")
                flag_me = False
                return flag_me
        print("This PN is a MG, place just have 1 input transition and 1 output transition.")
        print("Also, for definition, it is a FC")
        return flag_me

    def is_state_machine(self):
        """
        Each transition just have 1 input place and 1 output place.
        The summatory of each transition on C must be 0.
        """
        flag_se = True
        for row in range(len(self.pre_transpose)):
            sum_transition_pre = np.sum(self.pre_transpose[row])
            sum_transition_post = np.sum(self.post_transpose[row])

            if sum_transition_pre != 1 or sum_transition_post != 1:
                print("Is not a state machine, try free-choice")
                flag_se = False
                return flag_se
        print("This PN is a SM, each transition just have 1 input place and 1 output place.")
        print("Also, for definition, it is a FC")
        return flag_se

    def is_free_choice(self):
        """
        If there are places with more than 1 transition in, each transition of them share the same in
        """
        flag_fc = True
        for row in range(len(self.pre)):
            sum_free_transitions = np.sum(self.pre[row])
            if sum_free_transitions > 1:  # conflict detected
                for column in range(len(self.pre_transpose)):
                    if self.Pre[row][column] == 1:
                        sum_transition_pre = np.sum(self.pre_transpose[column])
                        if sum_transition_pre > 1:
                            print("Is not Free-Choice")
                            flag_fc = False
                            return flag_fc
        print("The net is Free-Choice")
        return flag_fc

    def is_free_choice_clusters(self):
        """
        If there are places with more than 1 transition in, each transition of them share the same in.
        Detects clusters.
        """
        # hi
