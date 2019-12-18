from lab2_3.algorithms import RBFS, LDFS, SA

if __name__ == "__main__":
    iters = 1
    algs = (SA,)
    for alg_cls in algs:
        alg = alg_cls(iters)
        alg.run()

        print(alg_cls.__name__)
        alg.show_statistic()
