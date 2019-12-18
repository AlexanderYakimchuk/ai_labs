from datetime import time
from math import log, exp
from random import random

from lab2_3.states import State
import sys
from time import time


# sys.setrecursionlimit(2000)


class Algorithm:
    def __init__(self, iters=1):
        self.finish = None
        self.iters = iters
        self.total_time = 0
        self.best_time = float('inf')
        self.worth_time = 0
        self.total_steps = 0
        self.best_steps = float('inf')
        self.worth_steps = 0

    def find_finish_state(self, init_state):
        raise NotImplementedError

    def run(self):
        for _ in range(self.iters):
            self.finish = None
            state = State.get_valid_init_state()
            while not self.finish:
                start = time()
                self.find_finish_state(state)
                end = time()
            # print(self.finish)
            self.update_time_statistic(end - start)
            self.update_steps_statistic(self.finish.depth)
            # print('-' * 40)
            # print(self.finish)
            # print(self.finish.depth)

    def get_path(self):
        state = self.finish
        states = []

        while state.prev_state:
            states.append(state)
            state = state.prev_state

        return states[::-1]

    def update_steps_statistic(self, steps):
        self.total_steps += steps
        self.best_steps = min((self.best_steps, steps))
        self.worth_steps = max((self.worth_steps, steps))

    def update_time_statistic(self, time):
        self.total_time += time

        self.best_time = min((self.best_time, time))
        self.worth_time = max((self.worth_time, time))

    def show_statistic(self):
        print('TIME')
        print('-' * 40)
        print(f'Average time: {self.total_time / self.iters}')
        print(f'Best time: {self.best_time}')
        print(f'Worth time: {self.worth_time}')
        print('-' * 40)
        print()
        print('STEPS')
        print('-' * 40)
        print(f'Average steps: {self.total_steps / self.iters}')
        print(f'Best steps: {self.best_steps}')
        print(f'Worth steps: {self.worth_steps}')
        print('-' * 40)


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
        if init_state.h == 0:
            self.finish = init_state
            return
        if init_state.depth > 30:
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
        self.finish = self.search(init_state, float('inf'))

    def search(self, state, f_limit):
        # print(state.__repr__())
        # print(f_limit, state.estimation, state.depth)
        successors = []
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
            result = self.search(best_state,
                                 min(f_limit,
                                     alternative))
            if result is not None:
                return result


class SA(Algorithm):
    def __init__(self, *args, t0=10000, k_max=1000000, **kwargs):
        self.t0 = t0
        self.k_max = k_max
        super().__init__(*args, **kwargs)

    def find_finish_state(self, init_state):
        self.finish = self.search(init_state)

    def temperature(self, k):
        return self.t0 / k # Cauchy
        # return self.t0 / log(1 + k)  # Boltzmann

    @classmethod
    def possibility(cls, de, t):
        # return exp(-1 * de / t)
        return 1 / (1 + exp(de) / t)

    def search(self, init_state):
        depths = {tuple(init_state): 0}
        state = init_state
        k = 1
        while k <= self.k_max:
            # print(state)
            t = self.temperature(k)
            new_state = state.new_state()
            e = state.h
            e_new = new_state.h
            p = self.possibility(e_new - e, t)
            move = False
            if e_new < e:
                move = True
            elif random() < p:
                move = True
            if move:
                s_depth = depths.get(tuple(state))
                ns_depth = depths.get(tuple(new_state), float('inf'))
                if ns_depth > s_depth + 1:
                    depths[tuple(new_state)] = s_depth + 1
                    new_state.depth = s_depth + 1
                state = new_state
            if state.h == 0:
                return state
            k += 1
        # state.depth = depths[tuple(state)]
        # print(state.depth)
        # return state
