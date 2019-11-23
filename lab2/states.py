import random

from lab2.conf import SIZE


class State(list):
    def __init__(self, *args, prev_state=None, depth=0, **kwargs):
        self.null = SIZE ** 2 // 2
        self.prev_state = prev_state
        self.depth = depth
        super().__init__(*args, **kwargs)

    @classmethod
    def move(cls, init_state, from_pos, to_pos):
        state = cls(init_state)
        state[from_pos], state[to_pos] = state[to_pos], state[from_pos]
        state.prev_state = list(init_state)
        state.null = to_pos
        state.depth = init_state.depth + 1
        return state

    def get_possible_moves(self, with_return=False):
        states = []
        if self.null % SIZE == 0:
            states.append(State.move(self, self.null, self.null + 1))
        elif self.null % SIZE == SIZE - 1:
            states.append(State.move(self, self.null, self.null - 1))
        else:
            states.append(State.move(self, self.null, self.null + 1))
            states.append(State.move(self, self.null, self.null - 1))

        if self.null - SIZE >= 0:
            states.append(State.move(self, self.null, self.null - SIZE))
        if self.null + SIZE < len(self):
            states.append(State.move(self, self.null, self.null + SIZE))

        if with_return:
            return states
        res = []
        for state in states:
            if list(state) != self.prev_state:
                res.append(state)

        return res

    @classmethod
    def get_init_state(cls):
        state = cls()
        items = set(range(1, SIZE ** 2))
        for pos in range(SIZE ** 2):
            if pos == state.null:
                state.append(None)
                continue
            item = random.choice(list(items))
            state.append(item)
            items.remove(item)

        return state

    @classmethod
    def get_valid_init_state(cls, moves=100):
        state = cls([None] * SIZE ** 2)
        for i in range(1, SIZE ** 2):
            state[i] = i
        state.null = 0
        print(state.__repr__())
        for _ in range(moves):
            state = random.choice(state.get_possible_moves(with_return=False))
            print(state.__repr__())
        # state.prev_state = None
        state.depth = 0
        return state


    @property
    def h(self):
        sum_ = 0
        for i in range(SIZE ** 2):
            item = self[i] or 0
            x, y = i // SIZE, i % SIZE
            exp_x, exp_y = item // SIZE, item % SIZE
            sum_ += abs(exp_x - x) + abs(exp_y - y)
        return sum_

    @property
    def estimation(self):
        return self.depth + self.h

    def __repr__(self):
        repr = '\n'
        for i in range(SIZE):
            repr += ' '.join(
                [str(self[SIZE * i + j] or ' ') for j in range(SIZE)]) + '\n'
        return repr


#   1 2
# 3 4 5
# 6 7 8
#
#
# 3 1 2
#   4 5
# 6 7 8
#
#
# 3 1 2
# 6 4 5
#   7 8
#
#
# 3 1 2
# 6 4 5
# 7   8
#
#
# 3 1 2
# 6   5
# 7 4 8
#
#
# 3 1 2
#   6 5
# 7 4 8
#
#
#   1 2
# 3 6 5
# 7 4 8
#
#
# 1   2
# 3 6 5
# 7 4 8
#
#
# 1 6 2
# 3   5
# 7 4 8
#
#
# 1 6 2
#   3 5
# 7 4 8
#
#
# 1 6 2
# 7 3 5
#   4 8