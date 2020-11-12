import pandas as pd
import numpy as np
from bisect import bisect
from mirror.nodes import CategoricalNode
from mirror.nodes import GaussianNode


# Abstract base class for all nodes
class Edge():
    def __init__(self, parent_name, child_name):

        self.parent_name = parent_name
        self.child_name = child_name
        # self.weight = weight
        self.type = None
        self.relation = None

    def instantiate_values(self, input_df):
        raise NotImplementedError

    def get_type(self):
        return "Edge"

class NtoNLinear(Edge):
    def __init__(self, parent_name, child_name):
        Edge.__init__(self, parent_name, child_name)
        self.type = "NtoN"
        self.relation = "linear"

    def instantiate_values(self, input_df):
        if input_df.shape[0] > 0: # use the values of its parent nodes to generate the values
            return np.array(input_df[self.parent_name])
        else: # no parent data exits
            print("No parent data exits!")
            raise ValueError

class NtoNNonLinear(Edge):
    def __init__(self, parent_name, child_name, threshold):
        Edge.__init__(self, parent_name, child_name)
        self.type = "NtoN"
        self.relation = "nonlinear"
        self.threshold = threshold

    def instantiate_values(self, input_df): # TODO: update
        raise NotImplementedError


class NtoC(Edge):
    def __init__(self, parent_name, child_name, bounds, probabilities):
        """
        :param parent_name:
        :param child_name:
        :param bounds: sorted list of numbers, the values specify the boundary of each range.
                E.g. [20, 45, 65] defines 4 ranges: [-, 20), [20, 45), [45, 65), [65, -)
        :param probabilities: list of dict, the order of the dict maps to the orders in the bounds.
                              The dict stores the probabilities of each category for the child node when the value of the parent node is within the range.
                E.g. [{"Y": 0.2, "N": 0.8}, {"Y": 0.7, "N": 0.3}, {"Y": 0.6, "N": 0.4}, {"Y": 0.3, "N": 0.7}]
        """
        Edge.__init__(self, parent_name, child_name)
        self.type = "NtoC"
        self.relation = "sample"
        self.bounds = bounds
        self.probabilities = probabilities
        self.probability_table = {str(x): probabilities[x] for x in np.arange(len(probabilities))}

    def instantiate_values(self, input_df):
        if input_df.shape[0] > 0:
            input_df[self.child_name] = input_df[self.parent_name].apply(lambda x: np.random.choice(list(self.probabilities[bisect(self.bounds, x)].keys()), p=list(self.probabilities[bisect(self.bounds, x)].values())))
            return np.array(input_df[self.child_name])
        else: # no parent data exits
            print("No parent data exits!")
            raise ValueError


class CtoC(Edge):
    def __init__(self, parent_name, child_name, probability_table):
        """
        :param parent_name:
        :param child_name:
        :param probability_table: dict, key is the categories from the child node, value is the set of the probability of its parent.
                E.g. {"M": {"Y": 0.7, "N": 0.3}, "F": {"Y": 0.3, "N": 0.7}}
        """
        Edge.__init__(self, parent_name, child_name)
        self.type = "CtoC"
        self.relation = "sample"
        self.probability_table = probability_table

    def instantiate_values(self, input_df):
        if input_df.shape[0] > 0:
            input_df[self.child_name] = input_df[self.parent_name].apply(lambda x: np.random.choice(list(self.probability_table[x].keys()), p=list(self.probability_table[x].values())))
            return np.array(input_df[self.child_name])
        else: # no parent data exits
            print("No parent data exits!")
            raise ValueError


class CtoN(Edge):
    def __init__(self, parent_name, child_name, category_distribution):
        """
        :param parent_name: str, the name of the parent node
        :param child_name: str, the name of the node to be generated
        :param category_distribution: dict, {"M": ["Gaussian", 0, 1], "F": ["Gaussian", -1, 1]}
        """

        Edge.__init__(self, parent_name, child_name)
        self.type = "CtoN"
        self.relation = "sample"
        self.category_distribution = category_distribution

    def sample_x(self, x):
        if self.category_distribution[x][0] == "Gaussian": # NUM
            return np.random.normal(self.category_distribution[x][1], np.sqrt(self.category_distribution[x][2]))
        elif self.category_distribution[x][0] == "Uniform": # NUM
            return np.random.uniform(self.category_distribution[x][1], self.category_distribution[x][2])
        else: # ORD
            return np.random.randint(self.category_distribution[x][1], self.category_distribution[x][2])

    def instantiate_values(self, input_df):
        """
        :param input_df: dataframe, the column with name self.parent_name stores the values of the parent code to be used in the generation
        :return: dataframe, the edge is instantiated by adding the column with name self.child_name
        """
        if input_df.shape[0] > 0: # use the values of its parent nodes to generate the values
            input_df[self.child_name] = input_df[self.parent_name].apply(lambda x: self.sample_x(x))
            return np.array(input_df[self.child_name])
        else: # no parent data exits
            print("No parent data exits!")
            raise ValueError

if __name__ == '__main__':
    node_g = CategoricalNode("G", {"M": 0.5, "F": 0.5}, sample_n=1000)

    # node_g_m = GaussianNode("M_X", miu=0, var=1)
    # node_g_f = GaussianNode("F_X", miu=0, var=1)

    df = pd.DataFrame()
    df["G"] = node_g.instantiate_values()

    df["tmp"] = [1 for _ in range(df.shape[0])]
    df["A"] = np.random.randint(1, 80, size=1000)

    # print(df[df["G"]=="M"].shape[0], df[df["G"]=="F"].shape[0])
    # edge_g_x = CtoN("G", "X", 0.5, {"M": ["Gaussian", 0, 1], "F": ["Gaussian", -1, 1]})
    # df["X"] = edge_g_x.instantiate_values(df)
    # print(len(df), np.mean(df["X"]), np.var(df["X"]))
    # m_df = df[df["G"] == "M"]
    # f_df = df[df["G"] == "F"]
    # print("M", len(m_df), np.mean(m_df["X"]), np.var(m_df["X"]))
    # print("F", len(f_df), np.mean(f_df["X"]), np.var(f_df["X"]))

    # edge_g_d = CtoC("G", "D", {"M": {"Y": 0.7, "N": 0.3}, "F": {"Y": 0.3, "N": 0.7}})
    # df["D"] = edge_g_d.instantiate_values(df)
    # print(df.groupby(by=["G","D"]).count()/500)

    edge_g_d = NtoC("A", "D", [25, 45, 65], [{"Y": 0.2, "N": 0.8}, {"Y": 0.7, "N": 0.3}, {"Y": 0.6, "N": 0.4}, {"Y": 0.3, "N": 0.7}])
    # print(edge_g_d.probability_table)
    # df["D"] = edge_g_d.instantiate_values(df)
    #
    # for range_i in [[1, 25], [25, 45], [45, 65], [65, 100]]:
    #     cur_df = df[(df["A"] < range_i[1]) & (df["A"] >= range_i[0])]
    #     print(range_i)
    #     print(cur_df[["D", "tmp"]].groupby(by=["D"]).count()/cur_df.shape[0])
    #     print("\n\n")

    print(edge_g_d.get_type())

