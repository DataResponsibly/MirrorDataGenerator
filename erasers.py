import numpy as np

class Eraser:
    def __init__(self, columns, fraction, replace_values):
        """
        :param columns: list of str, names of the columns to be considered
        :param fraction: float, ratio of the data to be erased
        :param replace_values: dict, key is str, representing the name of a column, same as in columns. value is str, representing the value to be put in for the column.
        """
        if not columns:
            print('columns need to be non-empty.')
            raise ValueError
        if not fraction or type(fraction) != float:
            print('fraction need to be non-empty and float.')
            raise ValueError
        elif fraction > 1 or fraction <= 0:
            print('fraction need in the range (0, 1].')
            raise ValueError
        if not replace_values:
            print('replace_values need to be non-empty.')
            raise ValueError
        elif len(set(columns).difference(replace_values.keys())) > 0:
            print('replace_values need to have the key set as columns.')
            raise ValueError
        self.columns = columns
        self.fraction = fraction
        self.replace_values = replace_values

    def transform(self, data):
        raise NotImplementedError


class MCAR_eraser(Eraser):

    def __init__(self, columns, fraction, replace_values, seed=0):
        Eraser.__init__(self, columns, fraction, replace_values)
        self.pattern = 'MCAR'
        self.seed = seed
    def transform(self, data):
        np.random.seed(self.seed)
        corrupted_data = data.copy(deep=True)
        missing_indices = np.random.rand(len(data)) < self.fraction

        for coli in self.columns: # record the original value
            corrupted_data['orig_' + coli] = corrupted_data[coli]
            corrupted_data.loc[missing_indices, [coli]] = self.replace_values[coli]

        corrupted_data['perturb_index'] = missing_indices

        return corrupted_data


class MAR_eraser():
    def __init__(self, columns, fraction, replace_values, depends_on_cols, depends_on_orders=None, seed=0):
        Eraser.__init__(self, columns, fraction, replace_values)
        if len(columns) != len(depends_on_cols):
            print('depends_on_cols need to have the same length as columns.')
            raise ValueError
        if depends_on_orders:
            if set(depends_on_orders.keys()).difference(depends_on_cols):
                print('depends_on_orders need to have the key set same as depends_on_cols.')
                raise ValueError
        self.depends_on_cols = depends_on_cols
        self.depends_on_orders = depends_on_orders
        self.pattern = 'MAR'
        self.seed = seed

    def transform(self, data):
        np.random.seed(self.seed)
        corrupted_data = data.copy(deep=True)
        n_values_to_discard = int(len(data) * min(self.fraction, 1.0))
        if n_values_to_discard == len(data):
            perc_lower_start = 0
        else:
            perc_lower_start = np.random.randint(0, len(data) - n_values_to_discard)
        perc_idx = range(perc_lower_start, perc_lower_start + n_values_to_discard)

        if self.depends_on_orders: # auto-fill zero for the non-specified categories
            for coli, value_dicti in self.depends_on_orders.items():
                if type(value_dicti) == dict:
                    for vi in set(corrupted_data[coli].unique()).difference(value_dicti.keys()):
                        self.depends_on_orders[coli].update({vi: 0})
                    corrupted_data[coli + '_ordered'] = corrupted_data[coli].apply(lambda x: self.depends_on_orders[coli][x])
                else:
                    corrupted_data[coli + '_ordered'] = corrupted_data[coli].apply(lambda x: x * self.depends_on_orders[coli])

        missing_indices = corrupted_data.sort_values(by=[x+'_ordered' if x in self.depends_on_orders else x for x in self.depends_on_cols], ascending=False).iloc[perc_idx].index
        corrupted_data.drop(columns=[x+'_ordered' for x in self.depends_on_orders], inplace=True)

        for coli in self.columns: # record the original value
            corrupted_data["orig_" + coli] = corrupted_data[coli]
            corrupted_data.loc[missing_indices, [coli]] = self.replace_values[coli]

        corrupted_data["perturb_index"] = False
        corrupted_data.loc[missing_indices, ["perturb_index"]] = True

        return corrupted_data



class NMAR_eraser():
    def __init__(self, columns, fraction, replace_values, depends_on_orders=None, seed=0):
        Eraser.__init__(self, columns, fraction, replace_values)
        if depends_on_orders:
            if len(depends_on_orders) > len(columns):
                if sum([x not in depends_on_orders for x in columns]) > 0:
                    print('depends_on_orders need to have the key set same as columns.')
                    raise ValueError
        self.depends_on_orders = depends_on_orders
        self.pattern = 'NMAR'
        self.seed = seed

    def transform(self, data):
        np.random.seed(self.seed)
        corrupted_data = data.copy(deep=True)
        n_values_to_discard = int(len(data) * min(self.fraction, 1.0))
        if n_values_to_discard == len(data):
            perc_lower_start = 0
        else:
            perc_lower_start = np.random.randint(0, len(data) - n_values_to_discard)
        perc_idx = range(perc_lower_start, perc_lower_start + n_values_to_discard)

        if self.depends_on_orders: # auto-fill zero for the non-specified categories
            for coli, value_dicti in self.depends_on_orders.items():
                if type(value_dicti) == dict:
                    for vi in set(corrupted_data[coli].unique()).difference(value_dicti.keys()):
                        self.depends_on_orders[coli].update({vi: 0})
                    corrupted_data[coli + '_ordered'] = corrupted_data[coli].apply(lambda x: self.depends_on_orders[coli][x])
                else:
                    corrupted_data[coli + '_ordered'] = corrupted_data[coli].apply(lambda x: x*self.depends_on_orders[coli])

        missing_indices = corrupted_data.sort_values(by=[x+'_ordered' if x in self.depends_on_orders else x for x in self.columns], ascending=False).iloc[perc_idx].index
        corrupted_data.drop(columns=[x+'_ordered' for x in self.depends_on_orders], inplace=True)

        for coli in self.columns:  # record the original value
            corrupted_data["orig_" + coli] = corrupted_data[coli]
            corrupted_data.loc[missing_indices, [coli]] = self.replace_values[coli]

        corrupted_data["perturb_index"] = False
        corrupted_data.loc[missing_indices, ["perturb_index"]] = True

        return corrupted_data