import numpy as np
# Abstract base class for all nodes

# Support data type and node type mapping
DATA_TYPE_MAP = {"NUM": float, "ORD": int, "CAT": str}
class Node():
    def __init__(self, name, type, sample_n):
        """
        :param name: str, the name of the column that is instantiated from the node
        :param type: str, the type of the node
        :param sample_n: int, size of the instantiated samples
        """
        self.name = name
        self.type = type
        self.sample_n = sample_n
        self.value_type = DATA_TYPE_MAP[type]  # the type of values for the node

        # parameters updated by each children node
        self.domain = None # set that stores the range of the possible values for the node. ONLY for CAT and ORD nodea
        self.distribution = None # str, the name of the distribution that the node is sampled from
        self.parameters = None # dict that stores all the necessary parameters for the node distribution. E.g. for GaussianNode, {"miu": 0, "var": 1} and for UniformNode, {"min": 0, "max": 1}

    def instantiate_values(self):
        raise NotImplementedError

    def get_type(self):
        return "Node"

class ParetoNode(Node):
    # TODO: update edges for ParetoNode
    def __init__(self, name, sample_n=2000, shape=1.0, scale=1.0):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param sample_n: int, size of the instantiated samples
        :param shape: float, shape of the Pareto distribution. Must be positive. The parameter a in numpy.random.pareto.
        :param scale: float, scale of the Pareto distribution. Must be positive. The parameter m in numpy.random.pareto.
        """
        Node.__init__(self, name, "NUM", sample_n)
        self.distribution = "Pareto"
        self.parameters = {"shape": shape, "scale": scale}

    def instantiate_values(self):
        return (np.random.pareto(self.parameters["shape"], self.sample_n) + 1) * self.parameters["scale"]



# Classes of different types of Nodes
class GaussianNode(Node):

    def __init__(self, name, sample_n=2000, miu=0, var=1):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param sample_n: int, size of the instantiated samples
        :param miu: float, the mean value of the node's distribution
        :param var: float, the variance value of the node's distribution
        """
        Node.__init__(self, name, "NUM", sample_n)
        self.distribution = "Gaussian"
        self.parameters = {"miu": miu, "var": var}

    def instantiate_values(self):
        return np.random.normal(self.parameters["miu"], np.sqrt(self.parameters["var"]), self.sample_n)



class UniformNode(Node):
    def __init__(self, name, sample_n=2000, min=0, max=1):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param sample_n: int, size of the instantiated samples
        :param min: int, the minimal value of the node
        :param max: int, the maximal value of the node
        """
        Node.__init__(self, name, "NUM", sample_n)
        self.distribution = "Uniform"
        self.parameters = {"min": min, "max": max}

    def instantiate_values(self):
        return np.random.uniform(self.parameters["min"], self.parameters["max"], self.sample_n)

class OrdinalGlobalNode(Node):
    def __init__(self, name, sample_n=2000, min=1, max=100):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param sample_n: int, size of the instantiated samples
        :param min: int, the minimal value of the node
        :param max: int, the maximal value of the node
        """
        Node.__init__(self, name, "ORD", sample_n)
        self.domain = [min, max]
        self.distribution = "OrdinalGlobal"
        self.parameters = {"min": min, "max": max}

    def instantiate_values(self):
        return np.random.randint(self.parameters["min"], self.parameters["max"], size=self.sample_n)


class OrdinalLocalNode(Node):
    def __init__(self, name, parameters, sample_n=2000):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param parameters: dict, {"bound": [1, 45, 100], "probability": [0.5, 0.5]}}
        :param sample_n: int, size of the instantiated samples
        """
        Node.__init__(self, name, "ORD", sample_n)
        self.domain = [min(parameters["bound"]), max(parameters["bound"])]
        self.distribution = "OrdinalLocal"
        self.parameters = parameters

    def instantiate_values(self):
        res = np.random.choice(len(self.parameters["probability"]), self.sample_n, p=self.parameters["probability"])
        res = [(self.parameters['bound'][i], self.parameters['bound'][i+1]) for i in res]
        return np.array([np.random.randint(*i) for i in res])


class CategoricalNode(Node):
    def __init__(self, name, parameters, sample_n=2000):
        """
        :param name: str, the name of the column that is instantiated from this node
        :param parameters: dict, values of the node and its population {"M": 0.5, "F": 0.5}}
        :param sample_n: int, size of the instantiated samples
        """
        Node.__init__(self, name, "CAT", sample_n)
        self.domain = sorted(parameters)
        self.distribution = "Multinomial"
        self.parameters = parameters


    def instantiate_values(self):
        domain_prob = [self.parameters[x] for x in self.domain]
        return np.random.choice(self.domain, self.sample_n, p=domain_prob)

if __name__ == '__main__':
    # node_g = CategoricalNode("G", {"M": 0.5, "F": 0.5}, sample_n=100)
    # res = node_g.instantiate_values()
    # print(len(res), len([x for x in res if x == "M"]), len([x for x in res if x == "F"]))



    # node_x_non_linear = OrdinalLocalNode("X", {"bound": [1, 5, 50], "probability": [0.5, 0.5]}, sample_n=100)
    # res = node_x_non_linear.instantiate_values()
    # print(len(res), len([x for x in res if x < 5]), len([x for x in res if x < 50 and x >=5]))

    # node_x_linear = OrdinalGlobalNode("X", sample_n=100, min=1, max=100)
    # res = node_x_linear.instantiate_values()
    # print(len(res), len([x for x in res if x < 50]), len([x for x in res if x >= 50]))

    # node_y = UniformNode("Y", sample_n=100)
    # res = node_y.instantiate_values()
    # print(len(res), len([x for x in res if x < 0.5]), len([x for x in res if x >= 0.5]))

    # node_z = GaussianNode("Z", sample_n=100, miu=0, var=1)
    # res = node_z.instantiate_values()
    # print(len(res), len([x for x in res if x < 0]), len([x for x in res if x >= 0]))

    node_z = ParetoNode("X", sample_n=100, shape=2.0, scale=1.0)
    res = node_z.instantiate_values()
    # print(res)
    print(len(res), len([x for x in res if x < 1.0]), len([x for x in res if x >= 1.0]))
