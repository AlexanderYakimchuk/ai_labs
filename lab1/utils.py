from collections import namedtuple
import matplotlib.pyplot as plt
import numpy as np

Size = namedtuple('Size', ('len', 'width'))
Position = namedtuple('Position', ('x', 'y'))


class Node:
    def __init__(self, count=1, total_weight=float('inf'), pos=None,
                 from_node=None, visited=False):
        self.count = count
        self.total_weight = total_weight
        self.pos = pos
        self.from_node = from_node
        self.visited = visited

    def show(self):
        print(
            f'count: {self.count} total: {self.total_weight} from: {self.from_node} visited: {self.visited}')


def energy_required(energy):
    def _energy_required(func):
        def inner(*args, **kwargs):
            self = args[0]
            self.used_energy += energy
            return func(*args, **kwargs)

        return inner

    return _energy_required


def show(labels, garbage, energy):
    x = np.arange(len(labels))
    width = 0.45

    fig, ax = plt.subplots()
    ax.bar(x - width / 2, garbage, width, label='garbage')
    ax.bar(x + width / 2, energy, width, label='enegry')

    ax.set_ylabel('Scores')
    ax.set_title('Scores by agents')
    ax.set_xticks(x)
    ax.set_xticklabels(labels)
    ax.legend()

    fig.tight_layout()

    plt.show()
