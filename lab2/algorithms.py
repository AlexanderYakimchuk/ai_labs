from lab2.states import State
import sys

# sys.setrecursionlimit(2000)


class Algorithm:
    def __init__(self, iters=1):
        self.finish = None
        self.iters = iters

    def find_finish_state(self, init_state):
        raise NotImplementedError

    def run(self):
        for _ in range(self.iters):
            state = State.get_valid_init_state(moves=10)
            self.find_finish_state(state)
            print(self.finish)
            print(self.finish.depth)


class LDFS(Algorithm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

    def find_finish_state(self, init_state, visited=None):
        # print(init_state.__repr__())
        if visited is None:
            visited = set()
        visited.add(tuple(init_state))
        if self.finish:
            return
        if init_state.estimation == 0:
            self.finish = init_state
            return
        if init_state.depth > 50:
            return
        for state in init_state.get_possible_moves():
            if tuple(state) not in visited:
                self.find_finish_state(state)


class RBFS(Algorithm):
    def __init__(self, *args, **kwargs):
        self.best_estimation = float('inf')
        self.best_depth = 0
        super().__init__(*args, **kwargs)

    def find_finish_state(self, init_state):
        self.finish = RBFS_search(init_state, float('inf'))

    def find_finish(self, init_state, visited=None):
        print(init_state.__repr__())
        print(self.best_estimation, self.best_depth)
        if visited is None:
            visited = set()
        visited.add(tuple(init_state))
        if self.finish:
            return
        estimation = init_state.estimation
        if estimation == 0:
            self.finish = init_state
            return
        better_est = estimation <= self.best_estimation
        if better_est or not better_est and init_state.depth < self.best_depth:
            if better_est and init_state.depth >= self.best_depth:
                self.best_depth = init_state.depth
                self.best_estimation = estimation
            for state in init_state.get_possible_moves():
                if tuple(state) not in visited:
                    self.find_finish(state, visited)
        else:
            return


def RBFS_search(state, f_limit):
    print(state.__repr__())
    print(f_limit, state.estimation, state.depth)
    successors = []
    # if state.depth > 50:
    #     return
    if state.h == 0:
        return state
    children = state.get_possible_moves()
    if not children:
        return
    count = 0
    for child in children:
        child.estimation_ = max((child.estimation, state.estimation))
        successors.append(child)
        count += 1

    while successors:
        successors = list(sorted(successors, key=lambda x: x.estimation))
        best_state = successors[0]
        if best_state.estimation > f_limit:
            best_state.update_branch_estimation()
            return
        if len(successors) > 1:
            alternative = successors[1].estimation
        else:
            alternative = float('inf')
        result = RBFS_search(best_state,
                             min(f_limit,
                                 alternative))
        if result is not None:
            return result
