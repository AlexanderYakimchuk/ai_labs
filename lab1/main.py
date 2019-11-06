from lab1 import choices
from lab1.agents import RandomAgent, ReflectiveAgent, ModelBasedAgent
from lab1.environment import Environment
from lab1.utils import Position

start_position = Position(1, 1)
iterations = 10000
maps = [choices.MAP1, choices.MAP2, choices.MAP3]
agents = (RandomAgent, ReflectiveAgent, ModelBasedAgent)

if __name__ == "__main__":

    for map in maps:
        print(map)
        for agent_class in agents:
            env = Environment(map)
            agent = agent_class(environment=env, position=start_position)
            # print(agent_class)
            garbage, energy = env.run(agent=agent,
                                      iterations=iterations)
            print(garbage, energy)
