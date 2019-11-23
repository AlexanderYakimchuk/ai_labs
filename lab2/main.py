from lab2.algorithms import RBFS, LDFS
from lab2.states import State

if __name__ == "__main__":
    iters = 20
    algs = (RBFS, LDFS)
    for alg_cls in algs:
        alg = alg_cls(iters)
        alg.run()
        print(alg_cls.__name__)
        alg.show_statistic()
