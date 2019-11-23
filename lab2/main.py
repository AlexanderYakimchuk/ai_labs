from lab2.algorithms import RBFS, RBFS_search
from lab2.states import State

if __name__ == "__main__":
    s = State([1, None, 2, 3, 6, 5, 7, 4, 8])
    s.null = 1
    RBFS_search(s, float('inf'))
