from lab4.agent import Agent
from lab4.choices import VIY, LADY
from lab4.map import Map

if __name__ == "__main__":
    map = Map()
    agent = Agent(map)
    agent.go(200)
