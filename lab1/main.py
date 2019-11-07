from lab1 import choices
from lab1.agents import RandomAgent, ReflectiveAgent, ModelBasedAgent
from lab1.environment import Environment
from lab1.utils import Position, show

start_position = Position(1, 1)
iterations = 2000
maps = [choices.MAP3]
agents = (RandomAgent, ReflectiveAgent, ModelBasedAgent)

if __name__ == "__main__":

    for map in maps:
        agent_names = ('random', 'reflective', 'model based')
        garbage_list = []
        energy_list = []
        print(map)
        for agent_class in agents:
            env = Environment(map)
            agent = agent_class(environment=env, position=start_position)
            # print(agent_class)
            garbage, energy = env.run(agent=agent,
                                      iterations=iterations)
            print(garbage, energy)
            garbage_list.append(garbage)
            energy_list.append(energy)
        show(agent_names, garbage_list, energy_list)
